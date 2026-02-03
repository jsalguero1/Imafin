from ocr import extract_text
import re

def parse_text(ocr_text):
    text = re.sub(r"\s+", " ", ocr_text)

    print(text)
    return text