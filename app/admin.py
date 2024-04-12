from django.contrib import admin
from .models import Category, User, House, Post, Comment


class HouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_date', 'updated_date']
    search_fields = ['description']
    list_filter = ['id', 'created_date']


admin.site.register(House, HouseAdmin)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
