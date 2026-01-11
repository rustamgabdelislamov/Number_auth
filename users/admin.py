from django.contrib import admin
from users.models import CustomUser, InviteRegistration


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "id")
    list_filter = ("phone_number",)
    search_fields = ("phone_number",)

# @admin.register(InviteRegistration)
# class InviteRegistrationAdmin(admin.ModelAdmin):
#     list_display = ("phone_number", "id")
#     list_filter = ("phone_number",)
#     search_fields = ("phone_number",)