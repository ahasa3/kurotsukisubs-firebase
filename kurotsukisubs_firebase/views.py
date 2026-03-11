"""
Views for Kurotsukisubs — Nogizaka46 Fansub Website.

All data is fetched from Firebase Firestore via fansub.firebase_service.
The views convert raw dicts to dataclass instances (fansub.models) so that
Django templates can use dot-notation exactly as they would with ORM objects.
"""

import logging
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from django.conf import settings

from . import firebase_service as fs
from fansub.models import post_from_dict, member_from_dict

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _paginate(items: list, per_page: int, page_number):
    """Paginate a plain Python list and return a Django Page object."""
    paginator = Paginator(items, per_page)
    return paginator.get_page(page_number)


# ─────────────────────────────────────────────────────────────────────────────
# HOME VIEW
# ─────────────────────────────────────────────────────────────────────────────

def home(request):
    """
    Home page — shows the latest posts with pagination and a sidebar.

    Context variables (match what the index.html template expects):
      posts           — Page object (iterable of Post dataclasses)
      page_obj        — same Page object (for pagination controls)
      recent_posts    — list of 5 most recent Post dataclasses (sidebar)
      members         — list of Member dataclasses (sidebar widget)
      total_posts     — int
      total_members   — int
      total_downloads — int
    """
    per_page = getattr(settings, 'POSTS_PER_PAGE', 5)
    recent_count = getattr(settings, 'RECENT_POSTS_COUNT', 5)

    try:
        # Fetch all posts (ordered by created_at desc)
        raw_posts, total_posts = fs.get_posts()
        posts_objs = [post_from_dict(p) for p in raw_posts]

        # Paginate
        page_number = request.GET.get('page', 1)
        page_obj = _paginate(posts_objs, per_page, page_number)

        # Sidebar data
        recent_posts = posts_objs[:recent_count]

        raw_members = fs.get_all_members()
        members = [member_from_dict(m) for m in raw_members]

        # Stats
        total_members = len(raw_members)
        stats = fs.get_site_stats()
        total_downloads = stats.get('total_downloads', 0)

    except Exception as exc:
        logger.exception("Error fetching home page data from Firestore: %s", exc)
        page_obj = _paginate([], per_page, 1)
        recent_posts = []
        members = []
        total_posts = 0
        total_members = 0
        total_downloads = 0

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'members': members,
        'total_posts': total_posts,
        'total_members': total_members,
        'total_downloads': total_downloads,
    }
    return render(request, 'index.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# MEMBER POSTS VIEW
# ─────────────────────────────────────────────────────────────────────────────

def member_posts(request):
    """
    Member posts page — filterable by member or tag.

    Context variables (match what the member_posts.html template expects):
      posts         — Page object (iterable of Post dataclasses)
      page_obj      — same Page object
      members       — list of Member dataclasses (filter bar)
      active_member — Member dataclass or None
    """
    per_page = getattr(settings, 'MEMBER_POSTS_PER_PAGE', 12)
    member_id = request.GET.get('member', '')
    tag_slug = request.GET.get('tag', '')
    page_number = request.GET.get('page', 1)

    active_member = None

    try:
        raw_members = fs.get_all_members()
        members = [member_from_dict(m) for m in raw_members]

        if member_id:
            raw_active = fs.get_member_by_id(member_id)
            if raw_active:
                active_member = member_from_dict(raw_active)

        raw_posts, _ = fs.get_posts(
            member_id=member_id or None,
            tag_slug=tag_slug or None,
        )
        posts_objs = [post_from_dict(p) for p in raw_posts]
        page_obj = _paginate(posts_objs, per_page, page_number)

    except Exception as exc:
        logger.exception("Error fetching member posts from Firestore: %s", exc)
        page_obj = _paginate([], per_page, 1)
        members = []

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'members': members,
        'active_member': active_member,
    }
    return render(request, 'member_posts.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# POST DETAIL VIEW
# ─────────────────────────────────────────────────────────────────────────────

def post_detail(request, pk: str):
    """
    Individual post detail page.

    Context variables (match what the post_detail.html template expects):
      post          — Post dataclass
      related_posts — list of Post dataclasses
      prev_post     — Post dataclass or None
      next_post     — Post dataclass or None
    """
    try:
        raw_post = fs.get_post_by_id(pk)
    except Exception as exc:
        logger.exception("Error fetching post %s from Firestore: %s", pk, exc)
        raise Http404("Post not found")

    if not raw_post:
        raise Http404("Post not found")

    post = post_from_dict(raw_post)

    try:
        raw_related = fs.get_related_posts(raw_post, limit=3)
        related_posts = [post_from_dict(p) for p in raw_related]

        raw_prev, raw_next = fs.get_adjacent_posts(raw_post)
        prev_post = post_from_dict(raw_prev) if raw_prev else None
        next_post = post_from_dict(raw_next) if raw_next else None
    except Exception as exc:
        logger.exception("Error fetching related/adjacent posts: %s", exc)
        related_posts = []
        prev_post = None
        next_post = None

    context = {
        'post': post,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'post_detail.html', context)
