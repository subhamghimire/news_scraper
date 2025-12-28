from datetime import datetime
from typing import Optional, Tuple

import nepali_datetime
from dateutil import parser

from app.services.language_detector import detect_language


def parse_date(date_str: str, language_hint: Optional[str] = None) -> Tuple[Optional[datetime], str]:
    if not date_str:
        return None, ""

    lang = language_hint or detect_language(date_str)

    if lang == "ne":
        try:
            nd = nepali_datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return nd.to_datetime(), date_str
        except Exception:
            return None, date_str

    try:
        return parser.parse(date_str), date_str
    except Exception:
        return None, date_str

