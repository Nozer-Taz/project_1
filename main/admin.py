from django.contrib import admin

from main.models import *


# admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Rating)
admin.site.register(Bookmark)
admin.site.register(Images)


class ImageInLine(admin.TabularInline):
    model = Images
    max_num = 10
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]
