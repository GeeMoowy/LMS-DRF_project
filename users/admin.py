from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Payment


class CustomUserAdmin(UserAdmin):
    """Кастомный класс для отображения пользователей (User) в админке"""
    list_display = ('email', 'id', 'phone_number', 'city', 'is_staff')
    list_filter = ('is_staff', 'city')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('avatar', 'phone_number', 'city')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'phone_number')
    ordering = ('email',)


class PaymentAdmin(admin.ModelAdmin):
    """Кастомный класс для отображения платежей (Payment) в админке"""
    list_display = ('user', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'course', 'lesson')
    search_fields = ('user__email', 'amount')

# Регистрация моделей
admin.site.register(User, CustomUserAdmin)
admin.site.register(Payment, PaymentAdmin)