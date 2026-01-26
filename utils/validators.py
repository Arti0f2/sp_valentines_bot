# utils/validators.py
import re

def validate_username(username: str) -> bool:
    if not username:
        return False
    
    clean_username = username.lstrip('@').lower()
    
    if len(clean_username) < 5 or len(clean_username) > 32:
        return False
    
    pattern = r'^[a-z0-9_]+$'
    return bool(re.match(pattern, clean_username))

def validate_age(age: int) -> bool:
    from config.constants import MIN_AGE, MAX_AGE
    return MIN_AGE <= age <= MAX_AGE

def validate_valentine_text(text: str) -> bool:
    from config.constants import MAX_VALENTINE_TEXT_LENGTH
    return 1 <= len(text.strip()) <= MAX_VALENTINE_TEXT_LENGTH