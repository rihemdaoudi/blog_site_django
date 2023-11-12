#from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.shortcuts import render
from .models import Post


# Create your views here.

def post_list(request):
    posts=Post.published.all()
    return render(request, 'blog/post/list.html', {'posts' :posts})

def post_detail(request,id):
    try:
        post=Post.published.get(id=id)
        
    except Post.DoesNotExist:
        raise Http404('no Post found')
    
    return render(request, 'blog/post/detail.html',{'post' :post})

# def post_detail(request,id):
#     post=get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
#     return render(request,'blog/post.detail.html', {'post':post})