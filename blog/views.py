from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.template.defaultfilters import title
from django.views import generic
from  blog.models import Post, Comment


def home(request):
    template_name= "blog/home.html"
    posts=Post.objects.all()
    for i in posts:
        i.content=i.content[0:100] +"..."
    context = {'object_list':posts}
    return render(request,template_name,context)

def add_post(request):
    if request.method=="POST":
        title=request.POST['title']
        content =request.POST['content']
        img=request.FILES['img']
        is_published=request.POST['is_published']
        user=User.objects.get(username=request.user.username)
        new_post=Post(title=title,content=content,img=img,is_published=is_published,user=user)
        new_post.save()
        return redirect('post',new_post.id)
    else:
        template_name='blog/add_post.html'
        context={}
        return render(request,template_name,context)

def edit_post(request,no):
    post=Post.objects.get(id=int(no))
    if request.user.username !=post.user.username:
        raise PermissionDenied
    if request.method =="GET":
        template_name='blog/post_edit.html'
        context={"post":post}
        return render(request,template_name,context)

    else:
        post:title=request.POST('title')
        post.content=request.POST('content')
        if 'img' in request.FILES:
            post.img = request.FILES['img']
        if 'is_published' in request.POST:
            post.is_published = request.POST('is_published')
        post.save()
        return redirect('post',post.id)
def delete_post(request, id):
    if Post.objects.get(id=id) is not None:
        Post.objects.get(id=id).delete()
        if Post.user.username ==request.user.username:
            Post.delete()
            return redirect('home')
    raise PermissionDenied

class DeletePostView(generic.DeleteView):
    model=Post
    success_url='/'

def signup(request):
    template='registration/signup.html'
    context={}
    if request.method =='POST':
        firstname = request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        print(User.objects.check(a))
        if len(user)!=0:
            context['errors']='Email is already taken'
            redirect(request,template,context)
        user=User.objects.get(username=username)
        if len(user)!=0:
            context['errors']="Username is already used"
            redirect(request,template,context)

        if password1==password2:
            user=User(firstname=firstname,lastname=lastname,email=email,username=username,password1=password1,password2=password2)
            user.set_password(password1)
            user.save()
            return redirect('login')
    return render(request,template,context)



def post_detail(request,no):
    post =Post.objects.get(id=int(no))
    print(post)
    template_name="blog/post.html"
    comments =Comment.objects.filter(post=post)
    context={'post':post,'comments':comments}
    return render(request,template_name,context)

#def EditPost(generic.UpdateView)
 #   model=post_detail
  #  template_name="blog/post_edit.html"
   # fields=['title']
   # fields=['title']

