import re

def mask_text(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'\b\d{11}\b' 
    name_regex = r'\b([А-ЯЁ][а-яё]+)\b'
    surname_regex = r'\b([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)\b'
    codes_regex = r'\b\d{9}\b' 
    month_regex = r'\b(январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь|қаңтарда|ақпанда|наурызда|сәуірде|мамырда|маусымда|шілде|тамызда|қыркүйекте|қазанда|қарашада|желтоқсанда)\b'
    def mask(match):
        return '*' * len(match.group(0))

    masked_text = re.sub(email_regex, mask, text)
    masked_text = re.sub(phone_regex, mask, masked_text)
    masked_text = re.sub(name_regex, mask, masked_text)
    masked_text = re.sub(surname_regex, mask, masked_text)
    masked_text = re.sub(month_regex, mask, masked_text)
    masked_text = re.sub(codes_regex, mask, masked_text)

    return masked_text
