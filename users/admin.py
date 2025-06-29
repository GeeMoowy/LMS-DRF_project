from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User, Payment


admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    """Кастомный класс для отображения групп (Group) в админке, который заменяет базовый класс групп"""
    list_display = ('name', 'display_users')

    def display_users(self, obj):
        return ", ".join([user.email for user in obj.user_set.all()[:3]])
    display_users.short_description = 'Пользователи'


class CustomUserAdmin(UserAdmin):
    """Кастомный класс для отображения пользователей (User) в админке"""
    list_display = ('email', 'id', 'phone_number', 'city', 'is_staff', 'display_groups')
    list_filter = ('is_staff', 'city', 'groups')  # Фильтр по группам
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('avatar', 'phone_number', 'city')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups'),
        }),
    )
    search_fields = ('email', 'phone_number')
    ordering = ('email',)

    def display_groups(self, obj):
        """Отображение групп в списке пользователей"""
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = 'Группы'


class PaymentAdmin(admin.ModelAdmin):
    """Кастомный класс для отображения платежей (Payment) в админке"""
    list_display = ('user', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'course', 'lesson')
    search_fields = ('user__email', 'amount')


# Регистрация моделей
admin.site.register(User, CustomUserAdmin)
admin.site.register(Payment, PaymentAdmin)
