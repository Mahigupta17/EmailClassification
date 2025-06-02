import re

ENTITY_PATTERNS = {
    "full_name": r"My name is\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_number": r"(?:\+91[-\s]?)?[6-9]\d{9}",
    "dob": r"\b\d{4}-\d{2}-\d{2}\b",
    "aadhar_num": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])/\d{2}\b",
}

def mask_email(text):
    masked_entities = []
    for label, pattern in ENTITY_PATTERNS.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            original = match.group()
            text = text[:start] + f"[{label}]" + text[end:]
            masked_entities.append({
                "entity": original,
                "classification": label,
                "position": [start, start + len(f"[{label}]")]
            })
    return text, masked_entities
