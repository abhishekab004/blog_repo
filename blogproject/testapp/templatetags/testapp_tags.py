from testapp.models import Post
from django import template
register= template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

# @register.inclusion_tag('testapp/latest_posts123.html')
# def show_latest_post():
#     latest_post = Post.objects.order_by('-publish')[:3]
#     return {'latest_post':latest_post}

              #OR  yaha count value pass kr rhe hai kitna latest post chaheye

@register.inclusion_tag('testapp/latest_posts123.html')
def show_latest_post(count=4):
    latest_post = Post.objects.order_by('-publish')[:count]
    return {'latest_post':latest_post}

# from django.db.models import Count
# @register.simple_tag
# def get_most_commented_post(count=5):
#     return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]     depreciated in newer vrsion after 2.0  ye wala kaam simple_tag se ho skta hai isliye

# from django.db.models import Count
# comments=Count('comments')
# @register.simple_tag
# def get_most_commented_post(count=5):
#     return Post.objects.order_by('-comments')[:count]
from django.db.models import Count
@register.simple_tag
def get_most_commented_post(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count] 