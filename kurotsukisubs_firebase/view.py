from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from posts.models import Post, Member

POSTS_PER_PAGE = 5  # Home page shows 5 per page

def home(request):
    posts_qs = Post.objects.select_related('member').prefetch_related('tags').all()
    paginator = Paginator(posts_qs, POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'recent_posts': posts_qs[:5],
        'members': Member.objects.all(),
        'total_posts': posts_qs.count(),
        'total_members': Member.objects.count(),
        'total_downloads': 0,  # calculate as needed
    }
    return render(request, 'index.html', context)

def member_posts(request):
    member_id = request.GET.get('member')
    tag_slug = request.GET.get('tag')

    posts_qs = Post.objects.select_related('member').prefetch_related('tags').all()
    active_member = None

    if member_id:
        active_member = get_object_or_404(Member, pk=member_id)
        posts_qs = posts_qs.filter(member=active_member)

    if tag_slug:
        posts_qs = posts_qs.filter(tags__slug=tag_slug)

    paginator = Paginator(posts_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'members': Member.objects.all(),
        'active_member': active_member,
    }
    return render(request, 'posts/member_posts.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('member').prefetch_related('tags', 'downloads'),
        pk=pk
    )

    # Related posts (same member or same category)
    related_posts = Post.objects.filter(
        member=post.member
    ).exclude(pk=post.pk)[:3] if post.member else Post.objects.exclude(pk=post.pk)[:3]

    # Prev / Next navigation
    prev_post = Post.objects.filter(created_at__lt=post.created_at).first()
    next_post = Post.objects.filter(created_at__gt=post.created_at).last()

    context = {
        'post': post,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'posts/post_detail.html', context)