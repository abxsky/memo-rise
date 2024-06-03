from store.models import Book
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import BookAdmin, BookImageInline
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )



class CustomBookAdmin(BookAdmin):
    inlines = [BookImageInline]


admin.site.unregister(Book)
admin.site.register(Book, CustomBookAdmin)