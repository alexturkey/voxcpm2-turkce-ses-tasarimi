"""Türkçe okunuş hazırlığı: tırnak temizliği, okunuş sözlüğü, satır ve durak ayrıştırma, metin denetimi.

Turkish text preparation: quote stripping, pronunciation dictionary, line/pause parsing, validation.
Kural: rakam ve tırnak motora gitmez (rakamı yazıyla yaz: "iki bin yirmi altı"). / Digits and quotes are rejected.
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
    return re.sub(r"\s{2,}", " ", QUOTE_MARKS.sub("", text)).strip()


def spoken(text: str) -> str:
    """Motora gidecek hali. / Final form sent to the engine."""
    return strip_quotes(apply_dictionary(text))


def problems(text: str, where: str = "metin") -> list:
    found = []
    marks = sorted(set(UNSPOKEN.findall(text)))
    if marks:
        found.append(f"{where}: okunamayan işaret {marks}; tırnak ve kesme işaretini kaldır, rakamı yazıyla yaz")
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
