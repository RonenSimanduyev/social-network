from django.urls import path
from .import views

urlpatterns =[
    path('',views.main),
    path('feed/<str:username>',views.home,name='home'),
    path('login',views.login_user,name='login'),
    path('signup',views.Signup_user,name='signup'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('profile/<str:username>/edit',views.Edit_Profile,name='EditProfile'),
    path('profile/<str:username>/remove',views.Remove_Profile ,name='RemoveProfile'),
    path('newPost/<str:username>',views.New_Post,name='NewPost'),
    path('post/<str:id>/edit',views.Edit_Post,name='EditPost'),
    path('post/<str:id>/<str:username>/remove',views.Remove_Post,name='PostRemove'),
    path('comment/<str:username>/<str:id>/remove',views.Remove_Comment,name='CommentRemove'),
    path('like/<str:username>/<str:id>',views.like,name='like'),
    path('comment/<str:username>/<str:id>/',views.new_comment,name='Comment'),
    path('comment/<str:username>/<str:id>/edit',views.edit_comment,name='EditComment'),
    path('friend/<str:username>',views.toggle_friend,name='friend'),
    path('logout',views.logout_user, name='logout'),
    path('search',views.search,name='search'),



]