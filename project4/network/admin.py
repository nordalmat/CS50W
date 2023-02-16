from django.contrib import admin
from .models import Post, User, Follow, Like


class PostAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


class FollowAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)

