import re

def generate_baggage_tag(user_input):
    pattern = r"^([A-F]{4})-(\d{4})-([A-Z]+)$"
    match = re.match(pattern, user_input)
    
    if not match:
        print("Неверный формат. Используйте: ABCD-1111-BOSCALI")
        return None
    
    letters_part = match.group(1)
    digits_part = match.group(2)
    country_part = match.group(3)
    
    hex_value = int(letters_part, 16)
    multiplied = hex_value * int(digits_part)
    hex_result = format(multiplied, 'X')
    
    result = f"{hex_result}-{country_part.upper()}"
    return result

user_input = input("Введите номер билета: ")
tag = generate_baggage_tag(user_input)
if tag:
    print(f"Талончик багажа: {tag}")