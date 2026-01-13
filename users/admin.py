from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "id")
    list_filter = ("phone_number",)
    search_fields = ("phone_number",)
