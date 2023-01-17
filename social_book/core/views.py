from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from rest_framework import viewsets
from datetime import datetime
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from datetime import datetime,timedelta
# Create your views here.

class LikePostViewSet(viewsets.ModelViewSet):
    queryset = LikePost.objects.all().order_by('post_id')
    serializer_class = LikePostSerializer


class CustomUserFilterApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()

        # Custom Filters Parameters

        check_active_users = self.request.query_params.get('check_active_users', None)
        check_superusers = self.request.query_params.get('check_superusers', None)
        check_login = self.request.query_params.get('check_login', None)
        check_date_joined = self.request.query_params.get('check_date_joined', None)

        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)

        if check_active_users:  # check if key is not None
            queryset = queryset.filter(is_active=check_active_users)

        if check_superusers:  # check if key is not None
            queryset = queryset.filter(is_superuser=check_superusers)

        # Date Filters

        if from_date and to_date:  # check if key is not None
            date_format = '%d-%m-%Y'
            from_date = datetime.strptime(from_date, date_format)  # Convert string into date format
            to_date = datetime.strptime(to_date, date_format)
            to_date = to_date + timedelta(days=1)  # add extra day in date search
            queryset = queryset.filter(date_joined__range=[from_date, to_date])

        if check_login and (from_date and to_date):
            queryset = queryset.filter(last_login__range=[from_date, to_date])

        if check_date_joined and (from_date and to_date):
            queryset = queryset.filter(date_joined__range=[from_date, to_date])



        serializer = CustomUserFilterSerializer(queryset, many=True)

        return Response(serializer.data)




class LikePostFilterApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = LikePost.objects.all()

        # Custom Filters Parameters

        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)

        # Date Filters

        if from_date and to_date:  # check if key is not None

            from_date = datetime.fromisoformat(from_date)  # Convert string into date format
            to_date = datetime.fromisoformat(to_date)
            to_date = to_date + timedelta(days=1)  # add extra day in date search
            queryset = queryset.filter(liked_at__range=[from_date, to_date])

        serializer = LikePostSerializer(queryset, many=True)

        return Response(serializer.data)



@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username= user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile':user_profile, 'posts': feed_list, 'suggestions_username_profile_list':suggestions_username_profile_list[:10]})

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
           username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_posts_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user,image=image, caption=caption)
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')
    return HttpResponse('<h1>Upload View</h1>')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
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
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        if not(username) :
            messages.info(request, 'Empty username')
            return redirect('signup')
        email = request.POST['email']
        if not(username) :
            messages.info(request, 'Empty email')
            return redirect('signup')
        password = request.POST['password']
        password2 = request.POST['password2']
        if not(password) or not(password2) :
            messages.info(request, 'Empty password')
            return redirect('signup')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # log user in and redirect to settings page
                user_login= auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

def logout(request):
    userprfl = Profile.objects.get(user=request.user)
    userprfl.last_activity = datetime.now()
    userprfl.save()

    auth.logout(request)
    return redirect('signin')













