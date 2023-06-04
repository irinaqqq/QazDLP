import re


def generate_shift(keyword):
    # Generate the shift amount based on the letters of the keyword
    # For example, if the keyword is "secret", the shift would be 18-4-2-17-4-19 = -10
    shift = sum(ord(char) - 97 for char in keyword.lower())
    return shift

keyword = "secret123"
shift = generate_shift(keyword)
dshift = - shift


email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'\b\d{11}\b'
name_regex = r'\b([А-ЯЁ][а-яё]+)\b'
surname_regex = r'\b([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)\b'
codes_regex = r'\b\d{9}\b' 

def mask_text(text):
    def mask(match):
        plaintext = match.group(0)
        if re.match(email_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isalpha():
                    shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else:
                    shifted_char = char
                ciphertext += shifted_char
        elif re.match(phone_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isdigit():
                    shifted_digit = str((int(char) + shift) % 10)
                else:
                    shifted_digit = char
                ciphertext += shifted_digit
        elif re.match(name_regex, plaintext):
            plaintext = plaintext.lower()
            ciphertext = ''
            for i, char in enumerate(plaintext):
                if char.isalpha():
                    shifted_char = chr((ord(char) - ord('а') + shift) % 26 + ord('а'))
                    if i == 0:
                        ciphertext += shifted_char.upper()
                    else:
                        ciphertext += shifted_char
                else:
                    ciphertext += char
        elif re.match(codes_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isdigit():
                    shifted_digit = str((int(char) + shift) % 10)
                else:
                    shifted_digit = char
                ciphertext += shifted_digit
        else:
            ciphertext = '*' * len(plaintext)
        return ciphertext

    masked_text = re.sub(email_regex, mask, text)
    masked_text = re.sub(phone_regex, mask, masked_text)
    masked_text = re.sub(name_regex, mask, masked_text)
    masked_text = re.sub(surname_regex, mask, masked_text)
    masked_text = re.sub(codes_regex, mask, masked_text)

    return masked_text



def unmask_text(text):
    def mask(match):
        plaintext = match.group(0)
        if re.match(email_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isalpha():
                    shifted_char = chr((ord(char) - ord('a') + dshift) % 26 + ord('a'))
                else:
                    shifted_char = char
                ciphertext += shifted_char
                continue
        elif re.match(phone_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isdigit():
                    shifted_digit = str((int(char) + dshift) % 10)
                else:
                    shifted_digit = char
                ciphertext += shifted_digit
        elif re.match(name_regex, plaintext):
            ciphertext = ''
            plaintext = plaintext.lower()
            for i, char in enumerate(plaintext):
                if char.isalpha():
                    shifted_char = chr((ord(char) - ord('а') + dshift) % 26 + ord('а'))
                    if i == 0:
                        ciphertext += shifted_char.upper()
                    else:
                        ciphertext += shifted_char
                else:
                    ciphertext += char
        elif re.match(codes_regex, plaintext):
            ciphertext = ''
            for char in plaintext:
                if char.isdigit():
                    shifted_digit = str((int(char) + dshift) % 10)
                else:
                    shifted_digit = char
                ciphertext += shifted_digit
        else:
            ciphertext = '*' * len(plaintext)
        return ciphertext

    masked_text = re.sub(email_regex, mask, text)
    masked_text = re.sub(phone_regex, mask, masked_text)
    masked_text = re.sub(name_regex, mask, masked_text)
    masked_text = re.sub(surname_regex, mask, masked_text)
    masked_text = re.sub(codes_regex, mask, masked_text)

    return masked_text