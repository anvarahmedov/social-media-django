
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from core.models import Post, Profile

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
    context = {
        'user_profile': user_profile, 'posts': posts
    }
    return render(request, 'index.html', context=context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            else:
                User.objects.create_user(username=username, email=email, password=password)

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')


    return render(request, 'setting.html', {
        'user_profile': user_profile
    })

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

def delete(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        #return HttpResponse(post.user)
        post.delete()
        return redirect('/')
    else:
        return redirect('/')

@login_required
def like_post(request, post_id):

    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            Profile.objects.get(user=request.user).likes.remove(post)
        else:
            post.likes.add(request.user)
            request.user.profile.likes.add(post)
            Profile.objects.get(user=request.user).likes.add(post)
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(id=pk)
    user_post = Post.objects.filter(user=user_object.username)
    user_post_length = len(user_post)
    user_followers = len(Profile.objects.get(user=user_object).followers.all())
    user_following = Profile.objects.get(user=user_object).following.count()
    context = {
        'user_profile': Profile.objects.get(user=user_object), 'user_object': user_object, 'user_post': user_post,
        'user_post_length': user_post_length, 'user_followers': user_followers, 'user_following': user_following
    }
    return render(request, 'profile.html', context=context)
