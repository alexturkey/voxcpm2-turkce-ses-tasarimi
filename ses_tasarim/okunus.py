"""Türkçe okunuş hazırlığı: tırnak temizliği, okunuş sözlüğü, satır ve durak ayrıştırma, metin denetimi.

Turkish text preparation: quote stripping, pronunciation dictionary, line/pause parsing, validation.
Kural: rakam ve tırnak motora gitmez (rakamı yazıyla yaz: "iki bin yirmi altı"). / Digits and quotes are rejected.

Çok dilli / multilingual: dil "tr" dışındaysa Türkçe okunuş sözlüğü ve Türkçe küçük harf kuralları UYGULANMAZ, kesme
işareti (l'eau, don't) metinde kalır; yalnız çift tırnak atılır ve rakam reddedilir (sayıyı o dilde yazıyla yaz).
For languages other than "tr" the Turkish dictionary is skipped and apostrophes are kept; only double quotes are removed.
"""
import re
from functools import lru_cache
from pathlib import Path

DICTIONARY = Path(__file__).resolve().parents[1] / "ayarlar" / "okunus_sozlugu.tsv"
WORD_EDGE = r"(?<![\wçğıöşüÇĞİÖŞÜ])"
WORD_END = r"(?![\wçğıöşüÇĞİÖŞÜ])"
QUOTE_MARKS = re.compile("[\"“”„«»‘’‚‹›`´']")
UNSPOKEN = re.compile("[\"“”„«»‘’‚‹›`´'\\d]")
MAX_LINE_CHARS = 2000          # motor metin bütçesi 2048 kod noktası / engine text budget
GAP_SECONDS = 0.35             # satırlar arası varsayılan sessizlik / default gap between lines
PAUSES = {"bagli": 0.25, "normal": 0.5, "paragraf": 1.0, "agir": 1.5}  # "metin || paragraf"
# kendi makinemizde uçtan uca denenen diller (2026-10-24); model başka dilleri de okuyabilir, onları ölçmedik
# languages we tested end to end on our own machine; the model may read others, not measured by us
LANGUAGES = {"tr": "Türkçe / Turkish", "en": "English", "fr": "Français", "de": "Deutsch", "es": "Español",
             "ru": "Русский", "zh": "中文 (普通话)", "ja": "日本語"}
DEFAULT_LANGUAGE = "tr"
DOUBLE_QUOTES = re.compile("[\"“”„«»‹›`´]")
UNSPOKEN_FOREIGN = re.compile("[\"“”„`´\\d]")


def language(code) -> str:
    """Dil kodunu doğrular ("tr", "en", ...); boşsa "tr". Listede olmayan kod da kabul edilir (ölçülmemiş).
    Normalizes a language code; empty means "tr". Codes outside LANGUAGES are allowed but untested."""
    code = str(code or DEFAULT_LANGUAGE).strip().lower()
    if not re.fullmatch(r"[a-z]{2,3}(-[a-z0-9]{2,8})?", code):
        raise ValueError(f"dil kodu tanınmadı / bad language code: {code!r} (ör. tr, en, fr, de, es, ru, zh, ja)")
    return code


def turkish_lower(text: str) -> str:
    return text.replace("I", "ı").replace("İ", "i").lower()


@lru_cache(maxsize=4)
def load_rules(path: Path = DICTIONARY) -> tuple:
    if not path.exists():
        return ()
    rules, seen = [], {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            raise ValueError(f"{path.name}:{number}: beklenen biçim 'yazılış<TAB>okunuş'")
        written, spoken = (part.strip() for part in line.split("\t", 1))
        key = turkish_lower(written)
        if key in seen:
            raise ValueError(f"{path.name}:{number}: '{written}' zaten {seen[key]}. satırda")
        seen[key] = number
        rules.append((written, spoken))
    rules.sort(key=lambda rule: len(rule[0]), reverse=True)
    return tuple(rules)


def apply_dictionary(text: str, rules: tuple = None) -> str:
    rules = load_rules() if rules is None else rules
    if not rules:
        return text
    lowered = turkish_lower(text)
    pattern = re.compile("|".join(WORD_EDGE + re.escape(turkish_lower(w)) + WORD_END for w, _ in rules))
    lookup = {turkish_lower(w): s for w, s in rules}
    pieces, cursor = [], 0
    for match in pattern.finditer(lowered):
        pieces.append(text[cursor:match.start()])
        pieces.append(lookup[match.group(0)])
        cursor = match.end()
    pieces.append(text[cursor:])
    return "".join(pieces)


def strip_quotes(text: str) -> str:
    """Tırnakları atar, boşlukları sadeleştirir; satır sonu (boş satır dahil) cümle sınırı olarak kalır.

    Removes quotes, collapses spaces; line breaks (blank lines too) stay as sentence boundaries.
    """
    text = re.sub(r"[^\S\n]*\n[^\S\n]*", "\n", QUOTE_MARKS.sub("", text))  # satır sonundaki boşluk ve \r gider
    return re.sub(r"[^\S\n]{2,}", " ", text).strip()


def strip_double_quotes(text: str) -> str:
    """Tr dışı diller: yalnız çift tırnak atılır, kesme işareti kalır. / Non-Turkish: keep apostrophes."""
    text = re.sub(r"[^\S\n]*\n[^\S\n]*", "\n", DOUBLE_QUOTES.sub("", text))
    return re.sub(r"[^\S\n]{2,}", " ", text).strip()


def spoken(text: str, dil: str = DEFAULT_LANGUAGE) -> str:
    """Motora gidecek hali. / Final form sent to the engine."""
    if language(dil) != "tr":
        return strip_double_quotes(text)  # Türkçe sözlük yabancı metni bozar / the Turkish dictionary would damage it
    return strip_quotes(apply_dictionary(text))


def problems(text: str, where: str = "metin", dil: str = DEFAULT_LANGUAGE) -> list:
    found = []
    try:
        turkish = language(dil) == "tr"
    except ValueError as error:
        return [str(error)]
    marks = sorted(set((UNSPOKEN if turkish else UNSPOKEN_FOREIGN).findall(text)))
    if marks and turkish:
        found.append(f"{where}: okunamayan işaret {marks}; tırnak ve kesme işaretini kaldır, rakamı yazıyla yaz")
    elif marks:
        found.append(f"{where}: okunamayan işaret {marks}; rakamı o dilde yazıyla yaz / write numbers as words")
    for number, (line, _) in enumerate(lines(text), 1):
        if len(line) > MAX_LINE_CHARS:
            found.append(f"{where}: {number}. satır {len(line)} karakter > {MAX_LINE_CHARS}; satırı böl")
    if not text.strip():
        found.append(f"{where}: boş")
    return found


def split_pause(line: str) -> tuple:
    """'metin || paragraf' → (metin, saniye). / Trailing pause marker."""
    if "||" in line:
        text, name = line.rsplit("||", 1)
        name = name.strip()
        if name not in PAUSES:
            raise ValueError(f"bilinmeyen durak '{name}'; seçenekler: {', '.join(PAUSES)}")
        return text.strip(), PAUSES[name]
    return line.strip(), GAP_SECONDS


def lines(text: str) -> list:
    """Her satır bir cümle; sonundaki durak süresiyle. / One sentence per line with its pause."""
    return [split_pause(line) for line in text.splitlines() if line.strip()]
