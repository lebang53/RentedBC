from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from .models import Category, User, House, Post, Comment
from .views import UserStatsViewSet


class HouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_date', 'updated_date']
    search_fields = ['description']
    list_filter = ['id', 'created_date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["queryset"] = User.objects.filter(role=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class UserAdmin(admin.ModelAdmin):
#     change_form_template = 'admin/user_stats_change_form.html'
#
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('stats/', self.admin_site.admin_view(self.stats_view)),
#         ]
#         return custom_urls + urls
#
#     def stats_view(self, request):
#         # Gọi API viewset để lấy dữ liệu thống kê
#         viewset = UserStatsViewSet()
#         role_stats = viewset.list(request).data
#
#         return JsonResponse(role_stats)


admin.site.register(User)
admin.site.register(House, HouseAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
