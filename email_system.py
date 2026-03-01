import datetime
from datetime import date


#Нормализация email адресов
def normalize_addresses(value: str) -> str:
    return value.strip().lower()

#Сокращенная версия тела письма
def add_short_body(email: dict) -> dict:
    email['short_body'] = email['body'][0:10] + '...'
    return email

#Очистка текста письма
def clean_body_text(body: str) -> str:
    return body.replace('\t', ' ').replace('\n', ' ')

#Формирование итогового текста письма
def build_sent_text(email: dict) -> str:
    return f"""Кому: {email['recipient']}, от {email['sender']}, 
Тема: {email['subject']}, дата {email['date']} 
{email['body']}
"""

#Проверка пустоты темы и тела
def check_empty_fields(subject: str, body:str) -> tuple[bool, bool]:
    is_subject_empty = not bool(subject.strip())
    is_body_empty = not bool(body.strip())
    return is_subject_empty, is_body_empty

#Маска email отправителя
def mask_sender_email(login: str, domain: str) -> str:
    return login[:2] + "***@" + domain

#Корректность email адресов
test_emails = [
    "user@gmail.com",
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    "default@study.com",
    " hello@corp.ru  ",
    "user@site.NET",
    "user@domain.coM",
    "user.name@domain.ru",
    "usergmail.com",
    "user@domain",
    "user@domain.org",
    "@mail.ru",
    "name@.com",
    "name@domain.comm",
    "",
    "   ",
]
def get_correct_email(email_list: list[str]) -> list[str]:
    allowed_domains = ('.com', '.ru', '.net')
    correct = []

    for email in email_list:
        e = email.strip()
        if not e:
            continue

        if "@" not in e:
            continue

        if not e.lower().endswith(allowed_domains):
            continue

        correct.append(e)
    return correct

#Создание словаря письма
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    email = {
        'sender': sender,
        'recipient': recipient,
        'subject': subject,
        'body': body,
    }
    return email

#Добавление даты отправки
def add_send_date(email: dict) -> dict:
    now = datetime.datetime.now()
    send_date = now.strftime('%Y-%m-%d')
    email['date'] = send_date
    return email

#Получение логина и домена
def extract_login_domain(address: str) -> tuple[str, str]:
    login, domain = address.split('@')
    return login, domain

#Часть В. Отправка письма
#Функция отправки письма с базовой валидацией адресов и логикой выбора отправителя recipient
def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:

#Проверить, что список получателей не пустой
    if not recipient_list:
        print('Ошибка: список получателей пуст.')
        return []

#Проверить корректность email адресов
    valid_recipients = get_correct_email(recipient_list)
    if not valid_recipients:
        print('Ошибка: нет корректных адресов получателей.')
        return []

#Проверить заполненность темы и тела письма
    is_subject_empty, is_body_empty = check_empty_fields(subject, message)

    if is_subject_empty:
        print('Ошибка: тема письма пустая.')
        return []

    if is_body_empty:
        print('Ошибка: тело письма пустое.')
        return []

#Исключить отправку самому себе
    for recipient in valid_recipients:
        if recipient == sender:
            valid_recipients.remove(recipient)
        print('Отправитель совпадает с отправителем, этот адрес удалён.')

#Нормализовать все текстовые данные
    clean_subject = clean_body_text(subject)
    clean_message = clean_body_text(message)
    sender = normalize_addresses(sender)
    new_recipients = []
    for email in valid_recipients:
        clean_email_recipients = normalize_addresses(email)
        new_recipients.append(clean_email_recipients)
        valid_recipients = new_recipients
#Создать письмо для каждого получателя
    sent_emails = []
    for recipient in valid_recipients:
        email = create_email(
            sender=sender,
            recipient=recipient,
            subject=clean_subject,
            body=clean_message
        )

#Добавить дату отправки
        email = add_send_date(email)

#Замаскировать email отправителя
        login, domain = extract_login_domain(sender)
        email["masked_sender"] = mask_sender_email(login, domain)

#Создать короткую версию тела письма
        email = add_short_body(email)

#Сформировать итоговый текст письма
        email["sent_text"] = build_sent_text(email)

        sent_emails.append(email)
    return sent_emails