# / login /
#
# phone_number = .....
#
# code = PhoneNumberCodes.objects.create()
#
# send_verifyed_code(code.code) - --
#
# self.request.sesssion['phone_number'] = 792208765431
#
# self.request.cookies.set('phone_number', '792208765431')
#
# redirect('/login/confirm/?phone_number=792208765431')
#
#
# class PhoneNumberCodes:
#     phone_number = 792208765431
#     code = 123123132
#
#
# GET / login / confirm /
#
# phone_number = self.request.sesssion.get('phone_number')
# if not phone_number:
#     return redirect('/login/')
#
# code: 123123132
#
# PhoneNumberCodes.objects.exists()
#
# PhoneNumberCodes.delete()
#
# user = User.objects.filter(phone=792208765431).first()
# if not user:
#     User.objects.create(phone=792208765431, your_invite=generate_invite_code())
#
# login()
#
# / invite_code / activate /
#
#
# class CustomUser(AbstractUser):
#     username = None
#     phone_number = models.CharField(
#         unique=True,
#         max_length=15,
#         verbose_name="Телефон",
#         help_text="Обязательное поле. Введите номер телефона",
#     )
#     your_invite = models.CharField(
#         max_length=6,
#         unique - True,
#         verbose_name="Свой инвайт код"
#     )
#     someone_invite = models.CharField(
#         max_length=6,
#         verbose_name="Чужой инвайт код",
#         blank=True,
#         null=True,
#     )
#
#     USERNAME_FIELD = "phone_number"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.phone_number
#
#     class Meta:
#         verbose_name = "пользователь"
#         verbose_name_plural = "пользователи"
#
#
# class PhoneNumberCodes:
#     phone_number = 792208765431
#     code = 123123132
#     is_active = True / False
#
#
# def generate_invite_code(length=6):
#     invite_base = []
#     characters = string.ascii_letters + string.digits  # Символы: буквы и цифры
#     invite_code = ''.join(random.choice(characters) for _ in range(length))
#     invite_base.append(invite_code)
#     return invite_code
#
#
# # Пример использования
# invite_code_ = generate_invite_code()
# print(invite_code_)
# from django.test import TestCase
#
# # Create your tests here.
# / login /
#
# phone_number = .....
#
# code = PhoneNumberCodes.objects.create()
#
# send_verifyed_code(code.code) - --
#
# self.request.sesssion['phone_number'] = 792208765431
#
# redirect('/login/confirm/')
#
#
# class PhoneNumberCodes:
#     phone_number = 792208765431
#     code = 123123132
#
#
# GET / login / confirm /
#
# POST / api / login / confirm /
#
# {phone_number: ..., code: ...}
#
# phone_number = self.request.sesssion.get('phone_number')
# if not phone_number:
#     return redirect('/login/')
#
# code: 123123132
#
# PhoneNumberCodes.objects.exists()
#
# PhoneNumberCodes.delete()
#
# user = User.objects.filter(phone=792208765431).first()
# if not user:
#     User.objects.create(phone=792208765431, your_invite=generate_invite_code())
#
# login()
#
# / invite_code / activate /
#
#
# class CustomUser(AbstractUser):
#     username = None
#     phone_number = models.CharField(
#         unique=True,
#         max_length=15,
#         verbose_name="Телефон",
#         help_text="Обязательное поле. Введите номер телефона",
#     )
#     your_invite = models.CharField(
#         max_length=6,
#         unique - True,
#         verbose_name="Свой инвайт код"
#     )
#     someone_invite = models.CharField(
#         max_length=6,
#         verbose_name="Чужой инвайт код",
#         blank=True,
#         null=True,
#     )
#
#     USERNAME_FIELD = "phone_number"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.phone_number
#
#     class Meta:
#         verbose_name = "пользователь"
#         verbose_name_plural = "пользователи"
#
#
# class PhoneNumberCodes:
#     phone_number = 792208765431
#     code = 123123132
#     is_active = True / False
#
#
# def generate_invite_code(length=6):
#     invite_base = []
#     characters = string.ascii_letters + string.digits  # Символы: буквы и цифры
#     invite_code = ''.join(random.choice(characters) for _ in range(length))
#     invite_base.append(invite_code)
#     return invite_code
#
#
# # Пример использования
# invite_code_ = generate_invite_code()
# print(invite_code_)
#
#
