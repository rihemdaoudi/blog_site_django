from django.shortcuts import get_object_or_404, render

from blog.forms import CommentForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

# Create your views here.

def post_list(request):
    post_list=Post.published.all()
    #Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    
    try:
        posts=paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'posts' :posts})#posts=type c le manager queryset=lazy

# def post_detail(request,id):
#     try:
#         post=Post.published.get(id=id)
        
#     except Post.DoesNotExist:
#         raise Http404('no Post found')
    
#     return render(request, 'blog/post/detail.html',{'post' :post})

def post_detail(request, year, month, day, post):
    post=get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    #List of active comments for this post
    comments = post.comment.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,'blog/post/detail.html', {'post':post,
                                                    'comments': comments,
                                                    'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted 
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #create a comment object without saving it to the database
        comment = form.save(commit=False)
        #Assign the post to the comment 
        comment.post = post
        #Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post':post,
                            'form': form,
                            'comment': comment})