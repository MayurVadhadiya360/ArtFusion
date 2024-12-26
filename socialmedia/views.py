from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from django.http import JsonResponse, HttpRequest
from django.urls import reverse
from .models import UserProfile, UserPost, Comments, UserFollower, PostLike
import json
import traceback
import uuid
import os

# Create your views here.
def home(request:HttpRequest):
    # data for navbar
    user_data = {
        'is_loggedin': False
    }

    # All post for showing on home page
    postsData = list(UserPost.objects.all().order_by('-created_at'))

    user_email = request.session.get('user_email')
    if user_email:
        current_user = UserProfile.objects.get(email=user_email)
        # user profile data to render
        user_data['post_count'] = UserPost.objects.filter(username=current_user).count()
        user_data['followers_count'] = UserFollower.objects.filter(user=current_user).count()
        user_data['following_count'] = UserFollower.objects.filter(follower=current_user).count()
        user_data['username'] = current_user.username
        user_data['user_email'] = current_user.email
        user_data['user_profession'] = current_user.profession
        user_data['user_profile_pic'] = current_user.profile_photo
        user_data['is_loggedin'] = True

        # Retrieve followers
        followers = UserFollower.objects.filter(user=current_user)
        tempFollowers = []
        for fellow in followers:
            tempFollower = {
                'username': fellow.follower.username,
                'email': fellow.follower.email,
                'profession': fellow.follower.profession,
                'profile_photo': fellow.follower.profile_photo,
                'is_following': UserFollower.objects.filter(user=fellow.follower, follower=current_user).exists(),
            }
            tempFollowers.append(tempFollower)
        followers = tempFollowers

        # Retrieve following
        following = UserFollower.objects.filter(follower=current_user)
        tempFollowing = []
        for fellow in following:
            tempFollow = {
                'username': fellow.user.username,
                'email': fellow.user.email,
                'profession': fellow.user.profession,
                'profile_photo': fellow.user.profile_photo,
                'is_following': True,
            }
            tempFollowing.append(tempFollow)
        following = tempFollowing

        user_data['followers'] = followers
        user_data['following'] = following

        # Processing Posts to ckeck whether user has liked it or not
        tempUserPosts = []
        for post in postsData:
            tempPostData = {
                'postData': post,
                'is_liked': PostLike.objects.filter(username=current_user, post=post).exists()
            }
            tempUserPosts.append(tempPostData)
        postsData = tempUserPosts
    else:
        # Processing Posts to ckeck whether user has liked it or not
        tempUserPosts = []
        for post in postsData:
            tempPostData = {
                'postData': post,
                'is_liked': False
            }
            tempUserPosts.append(tempPostData)
        postsData = tempUserPosts

    context = {
        "postsData": postsData,
        "user_data": user_data,
    }
    return render(request, 'home.html', context=context)

# Gives register page and take user data to register a user
def register(request:HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            try:
                # Create the user
                UserProfile.objects.create(username=username, email=email, password=password)
                send_mail(
                    subject="Registration Done!",
                    message="Congratulations for completing registration and joining ArtFusion!",
                    from_email="vadhadiya.mayur@gmail.com",
                    recipient_list=[email],
                    fail_silently=True
                )
                # Message For successful registration
                messages.success(request, f"Registered successfully!!")
                return redirect('login')  # Redirect to login page after successful registration
            except Exception as e:
                print(traceback.format_exc())
                messages.error(request, f"registration Failed!\n Details: {e}")
        else:
            messages.error(request, "Passwords do not match!")
    return render(request, 'register.html')


# Gives login page and take user data to login user
def user_login(request:HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email, password)
        try:
            user = UserProfile.objects.get(email=email)
            if user:
                if user.password == password:
                    request.session['user_email'] = user.email
                    messages.success(request, "Login Successfully!")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid Password!")
            else:
                messages.error(request, "Invalid Email!")
        except UserProfile.DoesNotExist as e:
            print(traceback.format_exc())
            messages.error(request, "User Not Found!")
        except Exception as e:
            print(traceback.format_exc())
            messages.error(request, f"Login failed!\nDetails: {e}")
    return render(request, 'login.html')

# Renders profile page
def profile(request:HttpRequest, user:str):
    try:
        userData = UserProfile.objects.get(username=user)
    except UserProfile.DoesNotExist as e:
        messages.error(request, "User not found!")
        return redirect('home')
    
    userPosts = UserPost.objects.filter(username=userData).order_by('-created_at')

    user_email = request.session.get("user_email")
    is_own_profile = True if userData.email == user_email else False
    is_currentuser_follower = False

    user_data = {
        'is_loggedin': False
    }

    if user_email:
        current_user = UserProfile.objects.get(email=user_email)
        user_data['is_loggedin'] = True
        user_data['username'] = current_user.username
    
        if not is_own_profile and current_user:
            is_currentuser_follower = UserFollower.objects.filter(user=userData, follower=current_user).exists()
    
        # Processing Posts to ckeck whether user has liked it or not
        tempUserPosts = []
        for post in userPosts:
            tempPostData = {
                'postData': post,
                'is_liked': PostLike.objects.filter(username=current_user, post=post).exists()
            }
            tempUserPosts.append(tempPostData)
        userPosts = tempUserPosts

        # Retrieve followers
        followers = UserFollower.objects.filter(user=userData)
        tempFollowers = []
        for fellow in followers:
            tempFollower = {
                'username': fellow.follower.username,
                'email': fellow.follower.email,
                'profession': fellow.follower.profession,
                'profile_photo': fellow.follower.profile_photo,
                'is_following': UserFollower.objects.filter(user=fellow.follower, follower=current_user).exists(),
            }
            tempFollowers.append(tempFollower)
        followers = tempFollowers

        # Retrieve following
        following = UserFollower.objects.filter(follower=userData)
        tempFollowing = []
        for fellow in following:
            tempFollow = {
                'username': fellow.user.username,
                'email': fellow.user.email,
                'profession': fellow.user.profession,
                'profile_photo': fellow.user.profile_photo,
                'is_following': UserFollower.objects.filter(user=fellow.user, follower=current_user).exists(),
            }
            tempFollowing.append(tempFollow)
        following = tempFollowing
    else:
        # Processing Posts to ckeck whether user has liked it or not
        tempUserPosts = []
        for post in userPosts:
            temp = {
                'postData': post,
                'is_liked': False
            }
            tempUserPosts.append(temp)
        userPosts = tempUserPosts
    
        # Retrieve followers
        followers = UserFollower.objects.filter(user=userData)
        tempFollowers = []
        for fellow in followers:
            tempFollower = {
                'username': fellow.follower.username,
                'email': fellow.follower.email,
                'profession': fellow.follower.profession,
                'profile_photo': fellow.follower.profile_photo,
                'is_following': False
            }
            tempFollowers.append(tempFollower)
        followers = tempFollowers

        # Retrieve following
        following = UserFollower.objects.filter(follower=userData)
        tempFollowing = []
        for fellow in following:
            tempFollow = {
                'username': fellow.user.username,
                'email': fellow.user.email,
                'profession': fellow.user.profession,
                'profile_photo': fellow.user.profile_photo,
                'is_following': False
            }
            tempFollowing.append(tempFollow)
        following = tempFollowing

    profile_data = {
        'is_own_profile': is_own_profile,
        'is_currentuser_follower': is_currentuser_follower,
        'username': userData.username,
        'email': userData.email,
        'profession': userData.profession,
        'about_user': userData.about_user,
        'profile_photo': userData.profile_photo,
        'post_count': len(userPosts),
        'followers_count': UserFollower.objects.filter(user=userData).count(),
        'following_count': UserFollower.objects.filter(follower=userData).count(),
        'posts': userPosts,
        'followers': followers,
        'following': following,
    }

    return render(request, 'profile.html', context={"profile_data":profile_data, "user_data":user_data})


# To update the profile: renders update_profile page and takes data to update profile
class profile_update(View):
    def get(self, request:HttpRequest, user:str):
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Please login to update your profile!")
            return redirect('login')
        
        current_user = UserProfile.objects.get(email=user_email)
        if user != current_user.username:
            messages.warning(request, "Please update your own profile!")
            return redirect('home')

        user_data = {
            'is_loggedin': True,
            'username': current_user.username,
            'email': current_user.email,
            'profession': current_user.profession,
            'about_user': current_user.about_user,
            'profile_photo': current_user.profile_photo,
            'post_count': UserPost.objects.filter(username=current_user).count(),
            'followers_count': UserFollower.objects.filter(user=current_user).count(),
            'following_count': UserFollower.objects.filter(follower=current_user).count(),
        }
        return render(request, 'profile_edit.html', context={'user_data': user_data})
        
    def post(self, request:HttpRequest, user:str):
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Please login to update your profile!")
            return redirect('login')
        
        current_user = UserProfile.objects.get(email=user_email)
        if user != current_user.username:
            messages.warning(request, "Please update your own profile!")
            return redirect('home')

        new_profession = request.POST.get('profession')
        new_about_user = request.POST.get('about_user')
        if request.FILES.get('profile_pic'):
            image_file = request.FILES['profile_pic']
            image_file.name = f"{uuid.uuid4().hex}{os.path.splitext(image_file.name)[1]}"
            current_user.profile_photo = image_file
        current_user.profession = new_profession
        current_user.about_user = new_about_user
        current_user.save()
        messages.success(request, "Successfully updated profile!")
        return redirect(reverse('profile', kwargs={'user': user}))

# To load upload_post page and upload post
class upload_post(View):
    def post(self, request:HttpRequest):
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Please login to send posts!")
            return redirect('login')
        
        current_user = UserProfile.objects.get(email=user_email)

        # Collecting the post data
        post_data = {
            "username": current_user,
            "post_title": request.POST.get("title"),
            "post_content": request.POST.get("desc"),
        }
        # Adding the image if provided
        if request.FILES.get('image'):
            image_file = request.FILES['image']
            image_file.name = f"{uuid.uuid4().hex}{os.path.splitext(image_file.name)[1]}"
            post_data["post_image"] = image_file
        
        # Creating the post instance
        post_instance = UserPost(**post_data)
        post_instance.save()

        send_mail(
            subject="Your Post is submitted at the ArtFusion!",
            message=f"Congratulations for posting on ArtFusion!\n\n"
                    f"Post Detail:\nTitle:{post_instance.post_title}\n"
                    f"Content:{post_instance.post_content}",
            from_email="vadhadiya.mayur@gmail.com",
            recipient_list=[current_user.email],
            fail_silently=True
        )
        messages.success(request, "Successfully uploaded post!") 
        return self.get(request)

    def get(self, request:HttpRequest):
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Please login to create posts!")
            return redirect('login')
        
        current_user = UserProfile.objects.get(email=user_email)
        user_data = {}
        user_data['is_loggedin'] = True
        user_data['username'] = current_user.username

        return render(request, 'upload_post.html', context={"user_data": user_data})

# Handles request of 'follow' and 'unfollow'
def follow_user(request:HttpRequest):
    if request.method == 'POST':
        response_data = { 'success': False }

        user_email = request.session.get("user_email")
        if not user_email:
            response_data['success'] = False
            response_data['msg'] = "Please login to follow users!"
            return JsonResponse(response_data)

        request_data = json.loads(request.body)
        sec_username = request_data.get('username')
        action = request_data.get('action')

        try:
            current_user = UserProfile.objects.get(email=user_email)
            sec_user = UserProfile.objects.get(username=sec_username)

            if action == 'follow':
                UserFollower.objects.create(user=sec_user, follower=current_user)
            elif action == 'unfollow':
                UserFollower.objects.filter(user=sec_user, follower=current_user).delete()

            response_data['success'] = True
        except UserProfile.DoesNotExist:
            response_data['success'] = False
            response_data['msg'] = "User not found!"
        except Exception as e:
            response_data['success'] = False
            response_data['msg'] = f"Failed to {action} user: {str(e)}"
        return JsonResponse(response_data)

# Process the event of some user liking/un-liking some post
def like_post(request:HttpRequest):
    if request.method == "POST":
        response_data = { 'success': False }
        user_email = request.session.get("user_email")
        if not user_email:
            response_data['success'] = False
            response_data['msg'] = "Please login to like posts."
            return JsonResponse(response_data)
        
        request_data = json.loads(request.body)
        post_pk = request_data.get('post_pk')
        action = request_data.get('action')

        try:
            current_user = UserProfile.objects.get(email=user_email)
            post = UserPost.objects.get(pk=post_pk)

            if action == 'like':
                PostLike.objects.create(username=current_user, post=post)
                post.like_count = post.like_count + 1
            else:
                PostLike.objects.filter(username=current_user, post=post).delete()
                post.like_count = post.like_count - 1
            
            post.save()
            response_data['success'] = True
        except UserPost.DoesNotExist:
            response_data['success'] = False
            response_data['msg'] = "Post doesn't exist or has been deleted!"
        except UserProfile.DoesNotExist:
            response_data['success'] = False
            response_data['msg'] = "User not found!"
        return JsonResponse(response_data)

# Load complete post with comments
def view_post(request:HttpRequest, pk:int):
    try:
        post = UserPost.objects.get(pk=pk)
        comments = list(Comments.objects.filter(post=post))
        postdata = {
            'postData': post,
            'comments': comments,
            'is_liked': False,
        }

        user_data = {
            'is_loggedin': False,
            'username': None,
        }

        user_email = request.session.get("user_email")
        if user_email:
            current_user = UserProfile.objects.get(email=user_email)
            user_data['is_loggedin'] = True
            user_data['username'] = current_user.username
            
            postdata["is_liked"] = PostLike.objects.filter(username=current_user, post=post).exists()

        return render(request, 'post_with_comments.html', context={"postdata": postdata, "user_data": user_data})
    except UserPost.DoesNotExist:
        messages.error(request, "Post doesn't exist or has been deleted!")
    except UserProfile.DoesNotExist:
        messages.error(request, "User not found!")
    return redirect('home')

# Delete post
def delete_post(request:HttpRequest, pk:int):
    if request.method == "POST":
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Login for delete post functionality!")
            return redirect('login')
        
        try:
            current_user = UserProfile.objects.get(email=user_email)
            post = UserPost.objects.get(pk=pk)
            if current_user.pk == post.username.pk:
                post.delete()
                messages.success(request, "Post deleted successfully!")
                return redirect('profile', user=current_user.username)
            else:
                messages.error(request, "You don't have permission to delete this post!")
                return redirect('profile', user=post.username.username)
        except UserPost.DoesNotExist:
            messages.error(request, "Post doesn't exist or has been deleted!")
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found!")
        return redirect('home')


# Adds a comment to particular post
def add_comment(request:HttpRequest):
    if request.method == "POST":
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "You need to login to comment on post!")
            return redirect('login')
        
        comment = request.POST.get('comment')
        post_pk = request.POST.get('pk')
        
        try:
            current_user = UserProfile.objects.get(email=user_email)
            post = UserPost.objects.get(pk=post_pk)

            Comments.objects.create(username=current_user, post=post, comment=comment)
            post.comment_count = post.comment_count + 1
            post.save()
            return redirect('view_post', pk=post_pk)
        except UserPost.DoesNotExist:
            messages.error(request, "Post doesn't exist or has been deleted!")
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found!")
        return redirect('home')

def delete_comment(request:HttpRequest, comment_pk:int, post_pk:int):
    if request.method == "POST":
        user_email = request.session.get("user_email")
        if not user_email:
            messages.warning(request, "Login for delete post functionality!")
            return redirect('login')
        
        try:
            current_user = UserProfile.objects.get(email=user_email)
            post = UserPost.objects.get(pk=post_pk)
            comment = Comments.objects.get(pk=comment_pk)
            if comment.username.pk == current_user.pk and comment.post.pk == post.pk:
                comment.delete()
                post.comment_count = post.comment_count - 1
                post.save()
                return redirect('view_post', pk=post_pk)
            else:
                messages.error(request, "You can't delete other user's comment!")
                return redirect('view_post', pk=post_pk)
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect('home')
        except UserPost.DoesNotExist:
            messages.error(request, "Post doesn't exist or has been deleted!")
            return redirect('home')
        except Comments.DoesNotExist:
            messages.error(request, "Comment doesn't exist or has been deleted!")
            return redirect('view_post', pk=post_pk)


def user_logout(request:HttpRequest):
    # Redirect to a page after successful logout
    request.session.flush()
    messages.success(request, "Successfully logged out!")
    return redirect('home')
