def is_nepali(text: str) -> bool:
    return any("\u0900" <= c <= "\u097F" for c in text)


def detect_language(text: str) -> str:
    return "ne" if is_nepali(text or "") else "en"

