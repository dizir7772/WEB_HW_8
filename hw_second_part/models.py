"""
Використовуючи ODM Mongoengine, створіть модель для контакту.
Модель обов'язково повинна включати поля:
повне ім'я,
email
та логічне поле, яке має значення False за замовчуванням.
Воно означає, що повідомлення контакту не надіслано і має стати True, коли буде відправлено.
Інші поля для інформаційного навантаження можете придумати самі.


Додаткове завдання
Введіть у моделі додаткове поле телефонний номер.
Також додайте поле, що відповідає за кращий спосіб надсилання повідомлень — SMS по телефону або email.
"""

from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contacts(Document):
    fullname = StringField()
    email = StringField()
    is_delivered = BooleanField(default=False)
    phone = StringField()
    prefer_way = StringField()
