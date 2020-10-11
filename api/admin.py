from django.contrib import admin
from .models import Category, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class UserAdmin(admin.ModelAdmin):
    list_display = ("role",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
