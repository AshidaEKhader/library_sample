from django.contrib import admin
from .models import User, Book, Author
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User


class BookAdmin(admin.ModelAdmin):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    model = Author


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)