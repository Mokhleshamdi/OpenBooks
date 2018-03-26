from django.contrib import admin
from .models import BookInstance
from .models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name","first_name","date_of_birth","date_of_death")
    fields = ["first_name","last_name",("date_of_birth","date_of_death")]

class InlineBookInstanceAdmin(admin.TabularInline):
     model = BookInstance
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author","D_Genre","image")
    search_fields=["title"]
    list_filter = ["title", "author"]
    inlines = [InlineBookInstanceAdmin]
class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('book', 'id')}), ('Availibility', {'fields': ('status', 'due_back')}),)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

from .models import Author, Genre,Book, BookInstance,Language
admin.site.register(Book,BookAdmin)

admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Language)


