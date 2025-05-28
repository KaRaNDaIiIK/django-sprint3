from django.contrib import admin

from .models import Category, Location, Post


admin.site.empty_value_display = 'Планета Земля'


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )
    list_editable = (
        'is_published',
        'category',
        'location'
    )
    search_fields = ('title',)
    list_filter = ('category', 'location',)
    list_display_links = ('title',)
