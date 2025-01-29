from django.contrib import admin, messages
from django.db.models import F

from library.models import Book, Author


# # Register your models here.
# admin.site.register(Book) # ==>> مدل معمولی برای نمایش
# admin.site.register(Author) # ==>> مدل معمولی برای نمایش
class BookInline(admin.StackedInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'birth_date', 'country']
    sortable_by = ['first_name', 'last_name']
    list_filter = ['country']
    list_editable = ['country']
    search_fields = ['first_name']
    inlines = [BookInline]
    fields = [('first_name', 'last_name'), 'country']
    readonly_fields = ['birth_date']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publish_date', 'pages_count']
    fieldsets = (  # 1
        ('General Info', {
            'fields': ('title', 'publish_date')
        }),
        ('Details', {
            'classes': ('collapse',),  # ==>> مخفی کردن اون بخش
            'fields': ('pages_count', 'author')
        }),
    )
    #########################################################################
    # هر چند وقت، تعداد صفحه‌های تعدادی کتاب‌ را به اندازه ۲ واحد افزایش دهیم
    #########################################################################
    actions = ['add_pages']

    def add_pages(self, request, queryset):
        updated = queryset.update(pages_count=F('pages_count') + 2)
        self.message_user(
            request, f"{updated} books pages added with two", messages.SUCCESS
        )

    add_pages.short_description = 'Add two page to selected books'
    #########################################################################
