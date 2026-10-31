"""Türkçe okunuş hazırlığı: tırnak temizliği, okunuş sözlüğü, satır ve durak ayrıştırma, metin denetimi.

Turkish text preparation: quote stripping, pronunciation dictionary, line/pause parsing, validation.
Kural: rakam ve tırnak motora gitmez (rakamı yazıyla yaz: "iki bin yirmi altı"). / Digits and quotes are rejected.

Dil metinden otomatik tanınır (detect). Çok dilli / multilingual: dil "tr" dışındaysa Türkçe okunuş sözlüğü ve Türkçe küçük harf kuralları UYGULANMAZ, kesme
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
MAX_PAUSE_SECONDS = 5.0        # özel durak üst sınırı ("metin || 0,8") / custom pause limit
PAUSE_MARK = re.compile(r"\|\|[^\n]*$", re.M)  # satır sonu durak işareti, okunmaz / trailing pause marker, not spoken
# kendi makinemizde uçtan uca denenen diller (2026-10-24); model başka dilleri de okuyabilir, onları ölçmedik
# languages we tested end to end on our own machine; the model may read others, not measured by us
LANGUAGES = {"tr": "Türkçe / Turkish", "en": "English", "fr": "Français", "de": "Deutsch", "es": "Español",
             "ru": "Русский", "zh": "中文 (普通话)", "ja": "日本語"}
DEFAULT_LANGUAGE = "tr"
DOUBLE_QUOTES = re.compile("[\"“”„«»‹›`´]")
UNSPOKEN_FOREIGN = re.compile("[\"“”„`´\\d]")


class Sorun(str):
    """Düz metin sorun (komut satırı için) + arayüzün kendi dilinde yazması için kod ve değerler.
    A plain-text problem (for the CLI) plus a code and values so the web UI can phrase it in its own language."""

    def __new__(cls, text: str, kod: str, **veri):
        problem = super().__new__(cls, text)
        problem.kod, problem.veri = kod, veri
        return problem

    def sozluk(self) -> dict:
        return {"kod": self.kod, "veri": self.veri, "metin": str(self)}


def language(code) -> str:
    """Dil kodunu doğrular ("tr", "en", ...); boşsa "tr". Listede olmayan kod da kabul edilir (ölçülmemiş).
    Normalizes a language code; empty means "tr". Codes outside LANGUAGES are allowed but untested."""
    code = str(code or DEFAULT_LANGUAGE).strip().lower()
    if not re.fullmatch(r"[a-z]{2,3}(-[a-z0-9]{2,8})?", code):
        raise ValueError(f"dil kodu tanınmadı / bad language code: {code!r} (ör. tr, en, fr, de, es, ru, zh, ja)")
    return code


# Metinden dil tanıma: ek paket yok, küçük kural kümesi. / Language detection from text: no extra packages, small rules.
_SCRIPTS = (("ja", re.compile("[぀-ヿ]")), ("zh", re.compile("[一-鿿]")),
            ("ru", re.compile("[Ѐ-ӿ]")))
_TR_ONLY = re.compile("[ğşıİĞŞ]")
_STOPWORDS = {
    "tr": "ve bir bu da de için ile çok gibi daha ne ama var yok mı mi ben sen o biz siz her en kadar sonra olarak"
          " değil çünkü kapadokya merhaba",
    "en": "the and of to is in it that for with as was on are this be at by an or from you not have but one",
    "fr": "le la les des est une un et en du de que qui dans pour pas sur au avec ce il elle nous vous sont l'un",
    "de": "der die das und ist ein eine nicht mit von zu den dem auf für auch sich es im wie ich sie so",
    "es": "el la los las es un una y en de que por con para no se su al lo como más pero uno esos esas",
}
_STOP_SETS = {code: set(words.split()) for code, words in _STOPWORDS.items()}
_CHAR_HINTS = {"es": "ñ¿¡áíóú", "fr": "èêàâôîœëùû", "de": "äß"}


def detect(text: str, fallback: str = None) -> str:
    """Metinden dili tanır: Türkçeye özgü harf (ğ ş ı İ) → tr; kana → ja; Han → zh; Kiril → ru; Latin ve Türkçe harf
    yoksa kısa sözcük/harf ipuçlarıyla en/fr/de/es/tr. İpucu yoksa fallback (kart ya da örnek dili), o da yoksa "tr".
    Detects the language from text. Turkish-only letters → tr; kana → ja; Han → zh; Cyrillic → ru; otherwise
    stopword/letter hints; no hint → fallback (voice card / example language), else "tr"."""
    text = text or ""
    counts = {code: len(rx.findall(text)) for code, rx in _SCRIPTS}
    if counts["ja"]:
        return "ja"  # kana varsa Han da Japonca olabilir / kanji mixes with kana in Japanese
    if counts["zh"]:
        return "zh"
    if counts["ru"]:
        return "ru"
    if _TR_ONLY.search(text):
        return "tr"
    words = re.findall(r"[\w']+", text.lower())
    scores = {code: sum(word in stops for word in words) for code, stops in _STOP_SETS.items()}
    lowered = text.lower()
    for code, chars in _CHAR_HINTS.items():
        scores[code] += 2 * sum(lowered.count(ch) for ch in chars)
    best = max(scores.values())
    leaders = [code for code, score in scores.items() if score == best]
    if best > 0 and len(leaders) == 1:
        return leaders[0]
    try:
        return language(fallback) if fallback else DEFAULT_LANGUAGE
    except ValueError:
        return DEFAULT_LANGUAGE


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
    marks = sorted(set((UNSPOKEN if turkish else UNSPOKEN_FOREIGN).findall(PAUSE_MARK.sub("", text))))
    if marks and turkish:
        found.append(Sorun(f"{where}: okunamayan işaret {marks}; tırnak ve kesme işaretini kaldır, rakamı yazıyla yaz",
                           "isaret_tr", isaretler=" ".join(marks)))
    elif marks:
        found.append(Sorun(f"{where}: okunamayan işaret {marks}; rakamı o dilde yazıyla yaz / write numbers as words",
                           "isaret", isaretler=" ".join(marks)))
    # Numara metin kutusundaki fiziksel satırdır (boş satırlar dahil), arayüzdeki satır numarasıyla aynı.
    # The number is the physical line (blank lines included), matching the UI's line numbers.
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        line, _ = split_pause(raw)
        if len(line) > MAX_LINE_CHARS:
            found.append(Sorun(f"{where}: {number}. satır {len(line)} karakter > {MAX_LINE_CHARS}; satırı böl",
                               "uzun_satir", satir=number, uzunluk=len(line), sinir=MAX_LINE_CHARS))
    if not text.strip():
        found.append(Sorun(f"{where}: boş", "bos"))
    return found


def pause_seconds(name: str) -> float:
    """Durak adı ya da özel saniye ('0,8', '1.2s'; 0-5 sn). / Named pause or custom seconds."""
    if name in PAUSES:
        return PAUSES[name]
    custom = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*s?", name)
    if custom and float(custom.group(1).replace(",", ".")) <= MAX_PAUSE_SECONDS:
        return float(custom.group(1).replace(",", "."))
    options = f"{', '.join(PAUSES)}, 0-{MAX_PAUSE_SECONDS:g} s"
    raise ValueError(Sorun(f"bilinmeyen durak '{name}'; seçenekler: {options}", "durak", durak=name, secenekler=options))


def split_pause(line: str) -> tuple:
    """'metin || paragraf' ya da 'metin || 0,8' → (metin, saniye). / Trailing pause marker."""
    if "||" in line:
        text, name = line.rsplit("||", 1)
        return text.strip(), pause_seconds(name.strip())
    return line.strip(), GAP_SECONDS


def lines(text: str) -> list:
    """Her satır bir cümle; sonundaki durak süresiyle. Boş satır önceki cümleye paragraf durağı verir
    (açık '||' işareti önce gelir). / One sentence per line with its pause; a blank line means a paragraph pause."""
    parsed, marked = [], False
    for line in text.splitlines():
        if not line.strip():
            if parsed and not marked:
                parsed[-1] = (parsed[-1][0], PAUSES["paragraf"])
            continue
        marked = "||" in line
        parsed.append(split_pause(line))
    return parsed
