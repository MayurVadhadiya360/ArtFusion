from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, UserPost, Comments
import json
import traceback
# from .forms import RegistrationForm, LoginForm

# Create your views here.

def home(request):
    # data for navbar
    user_profile = {}
    user_profile["nav_active"] = {
        "home": "active",
        "profile": "",
        "post": "",
        "about": ""
    }
    temp = request.session.get('logged_in', False)
    if temp is False:
        request.session['logged_in'] = False
        request.session['UserName'] = None
    if request.session['logged_in'] == True:
        userTemp = UserProfile.objects.get(username=request.session.get('UserName'))
        # user profile data to render
        user_profile['no_posts'] = len(UserPost.objects.filter(username=userTemp))
        user_profile['no_followers'] = len(userTemp.followers['followers'])
        user_profile['no_following'] = len(userTemp.following['following'])
        user_profile['profession'] = userTemp.profession
        user_profile['profile_photo'] = userTemp.profile_photo

        # Retrieving and processing followers data to be shown in home page
        followers_user_data = []
        for user in list(userTemp.followers['followers']):
            user_pr = UserProfile.objects.get(username=user)

            # To define whether button shound show 'Follow' or 'Following'
            if user in userTemp.following['following']:
                my_follow_status = "Following"
            else:
                my_follow_status = "Follow"

            temp = {
                'name': user_pr.username,
                'profile_photo': user_pr.profile_photo,
                'my_follow_status': my_follow_status
            }
            followers_user_data.append(temp)

        # Retrieving data of users that userX is following
        # following_user_data = []
        # for user in userTemp.following['following']:
        #     user_pr = UserProfile.objects.get(username=user)
        #     temp = {
        #         'name': user_pr.username,
        #         'profile_photo': user_pr.profile_photo,
        #         'my_follow_status': "Following"
        #     }
        #     following_user_data.append(temp)
 
        
        user_profile['followers'] = followers_user_data
        # user_profile['following'] = following_user_data
        
    user_profile['logged_in'] = request.session.get('logged_in')
    user_profile['userName'] = request.session.get('UserName')

    # All post for showing on home page
    postDatas = list(UserPost.objects.all())
    postDatas.reverse()

    # Processing Posts to ckeck whether user has liked it or not
    tempUserPosts = []
    username = None
    if request.session.get('logged_in'):
        username = request.session.get('UserName')
    for post in postDatas:
        temp = {
            'postData': post,
            'is_liked': False
        }
        if username in post.likes['likes']:
            temp["is_liked"] = True
        tempUserPosts.append(temp)
    postDatas = tempUserPosts


    context = {
        "user_profile": user_profile,
        "postDatas": postDatas
    }
    return render(request, 'home.html', context=context)

# Gives register page and take user data to register a user
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            # Create the user
            try:
                UserProfile.objects.create(username=username, email=email, password=password)
                send_mail(
                    subject="Registration Done!",
                    message="Congratulations for completing registration and joining ArtFusion!",
                    from_email="vadhadiya.mayur@gmail.com",
                    recipient_list=[email],
                    # fail_silently=True
                )
                # Message For successful registration
                messages.success(request, f"Registered Successfully with username: {username} and email: {email}!")
                return redirect('login')  # Redirect to login page after successful registration
            except Exception as e:
                print(traceback.format_exc())
                messages.error(request, f"registration Failed!\n Details: {e}")
    return render(request, 'register.html')


# Gives login page and take user data to login user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email, password)
        try:
            user = UserProfile.objects.get(email=email, password=password)
            if user:
                request.session['logged_in'] = True
                request.session['UserName'] = user.username
                messages.success(request, "Login Successfully!")
                return redirect('home')
            
        except UserProfile.DoesNotExist as e:
            print(traceback.format_exc())
            messages.error(request, "Login failed!\nDetails: {e}")
        except Exception as e:
            print(traceback.format_exc())
            messages.error(request, "Login failed!\nDetails: {e}")

    return render(request, 'login.html')


# Renders profile page
def profile(request, user):
    userData = UserProfile.objects.get(username=user)
    userPosts = UserPost.objects.filter(username=userData)
    
    # Checking if user is viewing his own profile or not
    if user == request.session.get('UserName', None):
        user_s_profile = True
    else:
        user_s_profile = False
        # If user user is viewing other's profile then checking if he is follower or not
        followers = userData.followers['followers']
        if request.session.get('UserName', None) in followers:
            user_is_follower = True
        else:
            user_is_follower = False

    # Processing Posts to ckeck whether user has liked it or not
    tempUserPosts = []
    username = None
    if request.session.get('logged_in'):
        username = request.session.get('UserName')
    for post in userPosts:
        temp = {
            'postData': post,
            'is_liked': False
        }
        if username in post.likes['likes']:
            temp["is_liked"] = True
        tempUserPosts.append(temp)
    userPosts = tempUserPosts

    profile_data = {
        'user_s_profile': user_s_profile,
        'userName': user,
        'posts': userPosts,
        'followers': userData.followers['followers'],
        'following': userData.following['following'],
    }

    if not user_s_profile:
        profile_data["user_is_follower"] = user_is_follower
    profile_data['about_user'] = userData.about_user
    profile_data['profession'] = userData.profession
    profile_data['profile_photo'] = userData.profile_photo

    user_profile = {
        'logged_in': request.session.get('logged_in', False),
        'userName': userData.username
    }
    user_profile["nav_active"] = {
        "home": "",
        "profile": "active",
        "post": "",
        "about": ""
    }

    return render(request, 'profile.html', context={"profile_data":profile_data, "user_profile":user_profile})


# To update the profile: renders update_profile page and takes data to update profile
class profile_update(View):
    def get(self, request, user):
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        if user_profile['logged_in'] and user_profile['userName'] == user:
            userTemp = UserProfile.objects.get(username=user_profile['userName'])
            userPosts = UserPost.objects.filter(username=userTemp)
            user_profile['no_post'] = len(userPosts)
            user_profile['no_followers'] = len(userTemp.followers['followers'])
            user_profile['no_following'] = len(userTemp.following['following'])
            user_profile['about_user'] = userTemp.about_user
            user_profile['profession'] = userTemp.profession
            user_profile['profile_photo'] = userTemp.profile_photo
            user_profile["nav_active"] = {
                "home": "",
                "profile": "active",
                "post": "",
                "about": ""
            }
            return render(request, 'profile_edit.html', context={'user_profile': user_profile})
        else:
            return redirect('home')
    
    def post(self, request, user):
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')

        if user_profile['logged_in'] and user_profile['userName'] == user:
            user_instance = UserProfile.objects.get(username=user_profile['userName'])
            # if request.POST.get('edit_profession'):
            new_profession = request.POST.get('edit_profession')
            new_about = request.POST.get('edit_about')
            if request.FILES.get('edit_profile_pic'):
                new_profile_pic = request.FILES['edit_profile_pic']
                user_instance.profile_photo = new_profile_pic
                user_instance.save()
            user_instance.profession = new_profession
            user_instance.about_user = new_about
            user_instance.save()
            messages.success(request, "Successfully updated profile!")
            # return redirect(f'/profile/{user}/')
            return redirect(reverse('profile', kwargs={'user': user}))
        else:
            return redirect('home')


# To load upload_post page and upload post
class upload_post(View):
    def post(self, request):
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        try:
            if user_profile['logged_in']:
                user = user_profile['userName']
                title = request.POST.get("title")
                content = request.POST.get("desc")
                userName = UserProfile.objects.get(username=user)
                is_img = False
                if request.FILES.get('image'):
                    is_img = True
                    image = request.FILES['image']
                    post_instance = UserPost(username=userName, post_title=title, post_content=content, post_image=image)
                    post_instance.save()
                else:
                    post_instance = UserPost(username=userName, post_title=title, post_content=content)
                    post_instance.save()

                send_mail(
                    subject="Your Post is submitted at the ArtFusion!",
                    message=f"Congratulations for posting on ArtFusion!\n\nPost Detail:\nTitle:{title}\nContent:{content}\nContains Image:{str(is_img)}",
                    from_email="vadhadiya.mayur@gmail.com",
                    recipient_list=[userName.email],
                    # fail_silently=True
                )
                messages.success(request, "Successfully Posted a post!")
                return redirect('home')
            else:
                messages.warning(request, "Please login to send posts!")
        except Exception as e:
            print(traceback.format_exc())
            messages.error(request, "Failed posting!\nDatails: {e}")
        return self.get(request)

        
    def get(self, request):
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        user_profile["nav_active"] = {
            "home": "",
            "profile": "",
            "post": "active",
            "about": ""
        }
        context = {
            "user_profile": user_profile,
        }
        return render(request, 'upload_post.html', context=context)


# Handles request of 'follow' and 'unfollow'
def follow_unfollow(request):
    if request.method == 'POST':
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        if user_profile['logged_in']:
            data = {
                'success': False
            }
            try:
                fData = json.loads(request.body)
                # print(fData)
                pri_user = user_profile['userName']
                sec_user = fData['some_user']
                primary_user = UserProfile.objects.get(username=pri_user)
                secondary_user = UserProfile.objects.get(username=sec_user)

                set_sec_followers = set(secondary_user.followers['followers'])
                set_pri_following = set(primary_user.following['following'])

                if fData['action_decider'] == 'Follow':
                    set_sec_followers.add(pri_user)
                    set_pri_following.add(sec_user)
                    data["follow_status_text"] = "Following"

                elif fData['action_decider'] == 'Following':
                    set_sec_followers.discard(pri_user)
                    set_pri_following.discard(sec_user)
                    data["follow_status_text"] = "Follow"

                
                secondary_user.followers['followers'] = list(set_sec_followers)
                primary_user.following['following'] = list(set_pri_following)

                secondary_user.save()
                primary_user.save()
                data["success"] = True

            except Exception as e:
                print(traceback.format_exc())
                data["success"] = False
            return JsonResponse(data)
        else:
            return redirect('login')


# To retrieve data of followers or following
def load_followers_following(request):
    if request.method == "POST":
        data = {
            'success': False
        }
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        # if user_profile['logged_in']:
        try:
            load_data = json.loads(request.body)
            if load_data['user']:
                userTemp = UserProfile.objects.get(username=load_data['user'])
            elif user_profile['logged_in']:
                userTemp = UserProfile.objects.get(username=user_profile['userName'])

            users_data = []
            if load_data['what_to_load'] == 'following':
                for user in list(userTemp.following['following']):
                    user_pr = UserProfile.objects.get(username=user)
                    temp = {
                        'name': user_pr.username,
                        'my_follow_status': "Following",
                    }
                    if not user_profile['logged_in']:
                        temp["my_follow_status"] = "Follow"
                    
                    if user_pr.profile_photo:
                        temp["profile_photo_url"] = user_pr.profile_photo.url

                    users_data.append(temp)

            elif load_data['what_to_load'] == 'followers':
                for user in list(userTemp.followers['followers']):
                    user_pr = UserProfile.objects.get(username=user)

                    # To define whether button shound show 'Follow' or 'Following'
                    if user_profile['logged_in'] and  user in userTemp.following['following']:
                        my_follow_status = "Following"
                    else:
                        my_follow_status = "Follow"

                    temp = {
                        'name': user_pr.username,
                        'my_follow_status': my_follow_status,
                    }
                    
                    if user_pr.profile_photo:
                        temp["profile_photo_url"] = user_pr.profile_photo.url

                    users_data.append(temp)

            data['users_data'] = users_data
            data["success"] = True
        except Exception as e:
            print(traceback.format_exc())
            data["success"] = False
        
        return JsonResponse(data)


# To load posts of given User
def load_posts(request):
    if request.method == "POST":
        data = {
            'success': False
        }
        # global user_profile
        user_profile = {}
        user_profile['logged_in'] = request.session.get('logged_in')
        user_profile['userName'] = request.session.get('UserName')
        try:
            load_data = json.loads(request.body)
            user = load_data['user']
            User = UserProfile.objects.get(username=user)
            posts = UserPost.objects.filter(username=User)
            postDatas = []
            for post in posts:
                temp = {
                    'username': User.username,
                    'pk': post.pk,
                    'post_title': post.post_title,
                    'post_content': post.post_content,
                    'created_at': post.created_at,
                    'likes': len(post.likes['likes']),
                    'is_liked': False
                }
                if post.post_image:
                    temp['post_image'] = post.post_image.url

                if user_profile['logged_in']:
                    UserTemp = UserProfile.objects.get(username=user_profile['userName'])
                    if UserTemp.username in post.likes['likes']:
                        temp["is_liked"] = True

                postDatas.append(temp)

            data["posts"] = postDatas
            data["success"] = True
        except Exception as e:
            print(traceback.format_exc())
            data["success"] = False
        return JsonResponse(data)

# Process the evet of some user liking/disliking some post
def like_post(request):
    if request.method == "POST":
        data = {
            'success': False
        }
        try:
            load_data = json.loads(request.body)
            user_profile = {}
            user_profile['logged_in'] = request.session.get('logged_in')
            user_profile['userName'] = request.session.get('UserName')
            if user_profile['logged_in']:
                post_pk = load_data['post_pk']
                like_action = load_data['like']
                User = UserProfile.objects.get(username=user_profile['userName'])
                Post = UserPost.objects.get(pk=post_pk)
                like_list = set(Post.likes['likes'])
                if like_action:
                    like_list.add(User.username)
                else:
                    like_list.discard(User.username)
                Post.likes['likes'] = list(like_list)
                Post.save()
                data["success"] = True
            else:
                data['not_logged_in'] = True
                return redirect('login')
        except Exception as e:
            print(traceback.format_exc())
            data["success"] = False
        return JsonResponse(data)

# Load whole post with comments
def load_whole_post(request, pk):
    try:
        post = UserPost.objects.get(pk=pk)
        comments = Comments.objects.filter(post=post)
        postData = {
            'postData': post,
            'comments': comments,
            'is_liked': False,
            'logged_in': False
        }

        if request.session.get('logged_in'):
            postData['logged_in'] = True
            username = request.session.get('UserName')
            if username in post.likes['likes']:
                postData["is_liked"] = True

        return render(request, 'post_with_msg.html', context={"postData": postData})
    except Exception as e:
        print(traceback.format_exc())
    return redirect('home')

# Adds a comment to particular post
def add_comment(request):
    if request.method == "POST":
        try:
            logged_in = request.session.get('logged_in')
            UserName = request.session.get('UserName')
            if logged_in:
                comment = request.POST.get('add_comment')
                post_pk = request.POST.get('pk')

                post = UserPost.objects.get(pk=post_pk)
                username = UserProfile.objects.get(username=UserName)
                Comments.objects.create(username=username, post=post, comment=comment)
                
                return redirect('load_whole_post', pk=post_pk)
        except Exception as e:
            print(traceback.format_exc())
    return redirect('login')

def user_logout(request):
    # Redirect to a page after successful logout
    request.session.flush()
    global user_profile
    user_profile = {
        'logged_in': False
    }
    messages.success(request, "Successfully logged out!")
    return redirect('home')
