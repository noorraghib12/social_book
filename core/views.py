from django.shortcuts import render,redirect
from .models import Profile,Post,LikePost,Comment,FollowedCount
from django.contrib.auth.models import User,auth
from django.contrib.auth import get_user
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.
@login_required(login_url='signin')
def index(request):
   user_object = User.objects.get(username=request.user.username)
   user_profile = Profile.objects.get(user=user_object)
   
   followed_usrnames=FollowedCount.objects.filter(user=user_object.username).values_list('following',flat=True)
   follower_usrnames=FollowedCount.objects.filter(following=user_object.username).values_list('user',flat=True)


   followings=list(chain(User.objects.filter(username__in=followed_usrnames).all(),[user_object]))
   posts=Post.objects.filter(user__in=followings).all().order_by('created_at')
   
   
   suggested_followers=FollowedCount.objects.filter(user__in=list(chain(follower_usrnames,followed_usrnames))).exclude(Q(following__in=followings))
   suggestions=FollowedCount.objects.filter(following__in=suggested_followers.values_list('following',flat=True)).values_list('following').annotate(followers=Count('user'))
   suggested_users=[(User.objects.get(username=username).profile.first(),n_followers) for (username,n_followers) in suggestions]
   print(suggested_users)
   return render(request,'index.html',{'user_profile':user_profile,'posts':posts,'user_suggestions':suggested_users})

def signup(request):
   if request.method=='POST':
      username=request.POST['username']
      email=request.POST['email']
      password1=request.POST['password1']
      password2=request.POST['password2']
      if (password1!=(None or '')) and password1==password2:
         if User.objects.filter(email=email).exists():
            messages.info(request, "User already exists, please use different email address")
            redirect('signup')
         elif User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            redirect('signup')
         else:
            user=User.objects.create_user(username=username,email=email,password=password1)
            user.save()


            #log user in and redirect to settings page
            user_login = auth.authenticate(username=username,password=password1)
            auth.login(request,user_login)
            #create Profile object for the new user
            
            user_model=User.objects.get(username=username)
            new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.save()
            return redirect('settings')
      else:
         messages.info(request, "Passwords dont match")
         return redirect('signup')
   return render(request,'signup.html')


def signin(request):
   if request.method=='POST':
      username=request.POST['username']
      password=request.POST['password']
      user = auth.authenticate(username=username,password=password)
      if user is not None:
         auth.login(request,user)
         return redirect('index')
      else:
         messages.info(request, 'Sorry, Wrong Credentials!')
         redirect('signin')
   return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
   auth.logout(request)
   return redirect('signin')


@login_required(login_url='signin')
def settings(request):
   user_profile=Profile.objects.get(user=request.user)
   if request.method=='POST': 
      if request.FILES.get('profileimg')==None:
         image=user_profile.profileimg 
      else:
         image=request.FILES.get('profileimg')
      usr_bio=request.POST['bio']
      usr_location=request.POST['location']

      user_profile.profileimg=image
      user_profile.bio=usr_bio
      user_profile.location=usr_location
      user_profile.save()

      redirect('settings')

   return render(request, 'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
   if request.method=='POST':
      user=request.user
      post_content=request.POST['caption']
      post_image=request.FILES.get('post_image')
      post=Post.objects.create(user=user,caption=post_content,image=post_image)
      post.save()

      return redirect('/')
   else:
      return redirect('/')

@login_required(login_url='signin')
def like_post(request):
   username=request.user.username
   post_id=request.GET.get('post_id')
   
   post_obj=Post.objects.get(id=post_id)

   like_filter = LikePost.objects.filter(username=username,post_id=post_id).first()
   if like_filter==None:
      new_like=LikePost.objects.create(username=username,post_id=post_id)
      new_like.save()
      post_obj.no_of_likes+=1
      post_obj.save()
      return redirect('/')

   else:
      like_filter.delete()
      post_obj.no_of_likes-=1
      post_obj.save()
      return redirect('/')


@login_required(login_url='signin')
def comment(request):
   if request.method=='POST':
      user=request.user
      user_profile=Profile.objects.get(user=user)
      post_id=request.POST['post_id']
      post=Post.objects.get(id=post_id)
      comment=request.POST['comment']
      print(comment,post_id)
      new_comment=Comment.objects.create(post=post,profile=user_profile,usr_comment=comment)
      new_comment.save()
      return redirect('/')
   else:
      return redirect('/')
   
@login_required(login_url='signin')
def profile(request,pk):
   user=User.objects.get(username=pk)
   profile=Profile.objects.get(user=user)

   posts=user.posts.all()
   box_text='Follow'
   if FollowedCount.objects.filter(following=pk,user=request.user.username).exists():
      box_text='Unfollow'
   user_followers=len(FollowedCount.objects.filter(following=pk))
   user_followings=len(FollowedCount.objects.filter(user=pk))
   context={
      'profile':profile,
      'posts':posts,
      'post_length':len(posts),
      'button_text':box_text,
      'user_followers':user_followers,
      'user_followings':user_followings,
   }
   return render(request,'profile.html',context=context)

@login_required(login_url='signin')
def follow(request):
   user=request.user
   
   if request.method=='POST':
      following_name=request.POST['followed_user']
      follow_user=User.objects.get(username=following_name)
      follow_filter=FollowedCount.objects.filter(user=user.username,following=follow_user.username).first()

      if user.username==follow_user.username:
         messages.info(request, "Cannot follow one's own profile")
         redirect(f'/profile/{user.username}')
      elif follow_filter==None:
         new_follow=FollowedCount.objects.create(user=user.username,following=follow_user.username)
         new_follow.save()
      else:
         follow_filter.delete()      
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))