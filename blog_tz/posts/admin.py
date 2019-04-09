from django.contrib import admin
from .models import Post, Comments

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',)
    search_fields = ['author', 'title']
    list_filter = ('date_posted',)
    date_hierarchy = ('date_posted')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post,PostAdmin)
admin.site.register(Comments)