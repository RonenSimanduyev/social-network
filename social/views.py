from operator import attrgetter
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Post,Profile,Comment
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from operator import attrgetter
import traceback

# Create your views here.



def login_user(request):
    error=''
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        try:
            user=User.objects.get(username=username)

        except:
            error='Username not found'

        user=authenticate(request,username=username ,password=password)

        if user is not None:
            login(request,user)
            return redirect('home',user.username)
            
        else:
            error='Username or password incorrect'
    return render(request,'social/login.html',{"error":error})



def Signup_user(request):
    form=UserCreationForm()
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST['username']
            password=request.POST['password1']
            try:
                user=authenticate(username=username ,password=password)
                Profile.objects.create(
                    user=user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    city=request.POST['city'],
                    dob=request.POST['dob'],
                    profile_img=request.POST['profile_img'],
                    background_img=request.POST['background_img'],
                )

                login(request,user)
                return redirect('home',user.username)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                return render(request,'social/signup.html',{'error':'error creating user'})

    return render(request,'social/signup.html',dict({'form':form}))


def logout_user(request):
    logout (request)
    return redirect('login')

@login_required(login_url='login')
def profile(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    posts =Post.objects.filter(user=profile).order_by('-created')

    is_friend = False

    if request.user.id != user.id:
        my_profile=Profile.objects.get(user=request.user)
        friends=my_profile.friends.all()
        
        if user in friends:
            is_friend = True
    else:
        friends=profile.friends.all()

    for post in posts:
        post.liked = False
        if profile in post.likes.all():
            post.liked = True
        
        comments=Comment.objects.filter(post=post)
        post.comments=comments

    friend_list3=[[]]
    for friend in friends:
        if len(friend_list3[-1])>2:
             friend_list3.append([])
        friend_profile=Profile.objects.get(user=friend)
        friend_list3[-1].append(friend_profile)

    return render(request,'social/profile.html',{
        'profile':profile,
        'posts':posts,
        'user':user, 
        'is_friend': is_friend,
        'friend_list3':friend_list3,
        })



@login_required(login_url='login')
def Edit_Profile(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    if request.method=='POST':
        profile.city=request.POST['city']
        profile.profile_img=request.POST['profile_img']
        profile.background_img=request.POST['background_img'] 
        profile.relationship= request.POST['relationship']== 'on'

        profile.save()

        return redirect('profile',user.username)
    return render(request,'social/EditProfile.html',{'profile':profile ,'user':user })



@login_required(login_url='login')
def Remove_Profile(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    if request.method=='POST':
        profile.delete()
        logout (request)
        return redirect('login')
    return render(request,'social/RemoveProfile.html',{'profile':profile ,'user':user})



@login_required(login_url='login')
def home(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    friends_user=profile.friends.all()
    my_posts=list(Post.objects.filter(user=profile))
    friends=[]
    for friend_user in friends_user:
        friend=Profile.objects.get(user=friend_user)
        friends.append(friend)
    friends_posts=[]
    for friend in friends:
        friend_posts=Post.objects.filter(user=friend)
        friends_posts.extend(friend_posts)
    all_posts=friends_posts + my_posts
    posts=sorted(all_posts, key=attrgetter('created'), reverse=True)
    
    for post in posts:
        comments=Comment.objects.filter(post=post)
        post.comments=comments

    try:
        for post in posts:
            post.liked = False
        if profile in post.likes.all():
            post.liked = True
    except:
        None
  
    return render(request,'social/home.html',{'profile':profile,'posts':posts,'user':user ,'username':username})




@login_required(login_url='login')
def like(request,id,username):
    if request.method == 'POST':
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        post =Post.objects.get(id=id)

        if profile in post.likes.all():
            post.likes.remove(profile)
        else:
            post.likes.add(profile)

    next=request.POST.get('next','/')
    return HttpResponseRedirect(next)




@login_required(login_url='login')
def new_comment(request,username,id):
    if request.method == 'POST':
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        post =Post.objects.get(id=id)

        Comment.objects.create(
            user=profile,
            post=post,
            body=request.POST['body']

        )
    next=request.POST.get('next','/')
    return HttpResponseRedirect(next)



@login_required(login_url='login')
def edit_comment(request,username,id):
    user=User.objects.get(username=username)
    comment=Comment.objects.get(id=id)
    if request.method=='POST':
        comment.body=request.POST['body']
        comment.save()
        
    
        return redirect('home',user.username)
    return render(request,'social/EditComment.html',{'comment':comment ,'user':user})
    


@login_required(login_url='login')
def show_profile(request):
    profile=Profile.objects.all
    return render(request,'social/profile.html',{'profile':profile})
    


@login_required(login_url='login')
def New_Post(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    if request.method == 'POST':
        Post.objects.create(
        user=profile,
        body=request.POST['body'],
        post_img=request.POST['post_img']
    )
    next=request.POST.get('next','/')
    return HttpResponseRedirect(next)



@login_required(login_url='login')
def Edit_Post(request,id):
    user=User.objects.get(username=request.user.username)
    profile=Profile.objects.get(user=user)
    post=Post.objects.get(id=id)
    if request.method=='POST':
        post.body=request.POST['body']
        post.post_img=request.POST['post_img']
        post.save()

        next=request.POST.get('next','/')
        return HttpResponseRedirect(next)
    
    next=request.GET.get('next','/')
    return render(request,'social/EditPost.html',{'post':post,'profile':profile, 'next': next})



@login_required(login_url='login')
def Remove_Comment(request,username,id):
    user=User.objects.get(username=username)
    comment=Comment.objects.get(id=id)
    if request.method=='POST':
        comment.delete()
        return redirect('home',user.username)
    return render(request,'social/RemoveComment.html',{'comment':comment ,'user':user})





@login_required(login_url='login')
def Remove_Post(request,id,username):
    post=Post.objects.filter(id=id)
    user=User.objects.get(username=username)
    if request.method=='POST':
        post.delete()
        return redirect('home', user.username)
    return render(request,'social/RemovePost.html')



@login_required(login_url='login')
def toggle_friend(request,username):
    if request.method=='POST':
        my_profile=Profile.objects.get(user=request.user)
        friend_user=User.objects.get(username=username)

        if friend_user in my_profile.friends.all():
            my_profile.friends.remove(friend_user)
        else:
           my_profile.friends.add(friend_user)

    next=request.POST.get('next','/')
    return HttpResponseRedirect(next)



def search(request):
    q = request.GET['search'] if request.GET['search'] != None else ''
    all_profiles = Profile.objects.filter(
    Q(first_name__icontains=q)

    )
    return render(request,'social/home.html',{'all_profiles':all_profiles})


def main(request):
    return redirect('login')
    