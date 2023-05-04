from django.shortcuts import render,get_object_or_404
from testapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag

# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list = Post.objects.all()
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator =Paginator(post_list,2)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'testapp/post_list.html',{'post_list':post_list,'tag':tag})

from testapp.forms import CommentForm
# from django.views.generic import ListView
# class PostListView(ListView):
#     model = Post
#     paginate_by =1

def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method=="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form =CommentForm()
    return render(request,"testapp/post_detail.html",{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

from django.core.mail import send_mail
from testapp.forms import EmailSendForm

def mail_send_view(request,id):
    post= get_object_or_404(Post,id=id,status='published')
    send= False
    if request.method=="POST":
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comments = form.cleaned_data['comments']
            subject = f'{name} ({email}) reccomends you to read "{post.title}" '
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = f'Read Post at : \n {post_url}  \n\n {name}\'s comments \n {comments}'
            send_mail(subject,message,'abhi@blog.com',[cd['to']])
            send=True
    else:
        form =EmailSendForm()
    return render(request,'testapp/sharebymail.html',{'form':form,'post':post,'send':send})
