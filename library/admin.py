from django.contrib import admin

from library.models import Book, Author


# # Register your models here.
# admin.site.register(Book) # ==>> مدل معمولی برای نمایش
# admin.site.register(Author) # ==>> مدل معمولی برای نمایش

class BookInline(admin.StackedInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'birth_date', 'country']
    sortable_by = ['first_name', 'last_name']  # 1
    list_filter = ['country']  # 2
    list_editable = ['country']  # 3
    search_fields = ['first_name']  # 4
    inlines = [BookInline]  # 5
    fields = [('first_name', 'last_name'), 'country']  # 6
    readonly_fields = ['birth_date']  # 7


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publish_date', 'pages_count']
