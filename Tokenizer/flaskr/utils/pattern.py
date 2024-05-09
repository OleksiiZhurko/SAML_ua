import re

from flaskr.consts.patterns import *


def _aligner(text: str, symbols: list[str], replace: str) -> str:
    for s in symbols:
        text = text.replace(s, replace)
    return text


def align_symbols(text) -> str:
    text = _aligner(text, ["“", "”", "„", "«", "»"], '"')
    text = _aligner(text, ["’", "‘", "´", "`"], "'")
    return text


def clean_unused_symbols(text: str) -> str:
    updated = text.lower()
    updated = re.sub(emailPattern, '', updated)
    updated = re.sub(urlPattern, '', updated)
    updated = re.sub(phonePattern, '', updated)
    updated = re.sub(userPattern, '', updated)
    updated = re.sub(hashtagPattern, '', updated)
    updated = re.sub(sequencePattern, seqReplacePattern, updated)
    updated = re.sub(tabPattern, ' ', updated)
    updated = re.sub(rPattern, '', updated)
    updated = re.sub(newLinePattern, ' ', updated)
    # text = text.replace(" <", "<").replace(" >", ">")
    updated = updated.replace("'", "")
    updated = re.sub(alphaPattern, '', updated)
    updated = re.sub(spacePattern, ' ', updated)
    return updated.strip()
