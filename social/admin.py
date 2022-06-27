from lib2to3.pgen2.token import COMMENT
from django.contrib import admin
from .models import Profile,Post,Group,User,Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)