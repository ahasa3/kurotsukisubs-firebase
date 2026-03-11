"""
Firebase / Firestore service layer for Kurotsukisubs.

This module initialises the Firebase Admin SDK once (singleton pattern) and
exposes helper functions that the Django views use to read/write data.

Firestore collections
─────────────────────
  members/
    {id}  name, avatar_url, created_at

  posts/
    {id}  title, excerpt, content, thumbnail_url, category,
          member_id, member_name, tag_ids[], created_at, updated_at

  tags/
    {id}  name, slug

  downloads/   (sub-collection of posts)
    {id}  label, url, host, file_size
"""

import os
import logging
from datetime import datetime, timezone
from typing import Optional
from django.utils.text import slugify

import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
from google.cloud.firestore_v1.base_query import FieldFilter

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# SDK INITIALISATION (singleton)
# ─────────────────────────────────────────────────────────────────────────────

def _init_firebase() -> None:
    """Initialise Firebase Admin SDK if not already done."""
    if firebase_admin._apps:
        return  # already initialised

    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', '')
    project_id = getattr(settings, 'FIREBASE_PROJECT_ID', '')

    if cred_path and os.path.isfile(cred_path):
        # Option A: service account JSON file
        cred = credentials.Certificate(cred_path)
        logger.info("Firebase: initialised from credentials file: %s", cred_path)
    elif project_id and getattr(settings, 'FIREBASE_PRIVATE_KEY', ''):
        # Option B: individual environment variables
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": getattr(settings, 'FIREBASE_PRIVATE_KEY_ID', ''),
            "private_key": getattr(settings, 'FIREBASE_PRIVATE_KEY', ''),
            "client_email": getattr(settings, 'FIREBASE_CLIENT_EMAIL', ''),
            "client_id": getattr(settings, 'FIREBASE_CLIENT_ID', ''),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": getattr(settings, 'FIREBASE_CLIENT_CERT_URL', ''),
        })
        logger.info("Firebase: initialised from environment variables (project: %s)", project_id)
    else:
        # Fallback: Application Default Credentials (useful on GCP / Cloud Run)
        cred = credentials.ApplicationDefault()
        logger.info("Firebase: initialised with Application Default Credentials")

    storage_bucket = getattr(settings, 'FIREBASE_STORAGE_BUCKET', None) or None
    firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket} if storage_bucket else {})


def get_db() -> firestore.Client:
    """Return a Firestore client, initialising Firebase if needed."""
    _init_firebase()
    return firestore.client()


# ─────────────────────────────────────────────────────────────────────────────
# COLLECTION NAMES (from settings)
# ─────────────────────────────────────────────────────────────────────────────

def _col(name: str) -> str:
    return getattr(settings, f'FIRESTORE_COLLECTION_{name.upper()}', name.lower())


# ─────────────────────────────────────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _ts_to_dt(ts) -> Optional[datetime]:
    """Convert a Firestore Timestamp (or None) to a Python datetime."""
    if ts is None:
        return None
    if hasattr(ts, 'ToDatetime'):
        return ts.ToDatetime(tzinfo=timezone.utc)
    if isinstance(ts, datetime):
        return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    return None


def _doc_to_member(doc) -> dict:
    """Convert a Firestore member document to a plain dict."""
    data = doc.to_dict() or {}
    return {
        'id': doc.id,
        'name': data.get('name', ''),
        'avatar_url': data.get('avatar_url', ''),
        'created_at': _ts_to_dt(data.get('created_at')),
        # post_count is computed separately
        'post_count': data.get('post_count', 0),
    }


def _doc_to_post(doc, member_map: dict = None) -> dict:
    """Convert a Firestore post document to a plain dict."""
    data = doc.to_dict() or {}
    member_id = data.get('member_id', '')
    member_name = data.get('member_name', '')

    # Resolve member from map if provided
    member = None
    if member_map and member_id and member_id in member_map:
        member = member_map[member_id]
    elif member_id:
        member = {'id': member_id, 'name': member_name, 'avatar_url': '', 'post_count': 0}

    return {
        'id': doc.id,
        'pk': doc.id,   # alias so templates can use post.pk
        'slug': data.get('slug',''),
        'title': data.get('title', ''),
        'excerpt': data.get('excerpt', ''),
        'content': data.get('content', ''),
        'thumbnail_url': data.get('thumbnail_url', ''),
        'category': data.get('category', 'General'),
        'member': member,
        'tag_ids': data.get('tag_ids', []),
        'tags': [],   # populated separately if needed
        'created_at': _ts_to_dt(data.get('created_at')),
        'updated_at': _ts_to_dt(data.get('updated_at')),
        'downloads': data.get('downloads', []),
    }


# ─────────────────────────────────────────────────────────────────────────────
# MEMBER QUERIES
# ─────────────────────────────────────────────────────────────────────────────

def get_all_members() -> list[dict]:
    """Return all members ordered by name."""
    db = get_db()
    docs = db.collection(_col('members')).order_by('name').stream()
    return [_doc_to_member(d) for d in docs]


def get_member_by_id(member_id: str) -> Optional[dict]:
    """Return a single member dict or None."""
    db = get_db()
    doc = db.collection(_col('members')).document(member_id).get()
    if doc.exists:
        return _doc_to_member(doc)
    return None


def create_member(name: str, avatar_url: str = '') -> str:
    """Create a new member and return its Firestore document ID."""
    db = get_db()
    _, ref = db.collection(_col('members')).add({
        'name': name,
        'avatar_url': avatar_url,
        'post_count': 0,
        'created_at': firestore.SERVER_TIMESTAMP,
    })
    return ref.id


def update_member(member_id: str, **fields) -> None:
    """Update member fields."""
    db = get_db()
    db.collection(_col('members')).document(member_id).update(fields)


def delete_member(member_id: str) -> None:
    """Delete a member document."""
    db = get_db()
    db.collection(_col('members')).document(member_id).delete()


# ─────────────────────────────────────────────────────────────────────────────
# TAG QUERIES
# ─────────────────────────────────────────────────────────────────────────────

def get_all_tags() -> list[dict]:
    db = get_db()
    docs = db.collection(_col('tags')).order_by('name').stream()
    return [{'id': d.id, **d.to_dict()} for d in docs]


def get_tag_by_slug(slug: str) -> Optional[dict]:
    db = get_db()
    docs = list(db.collection(_col('tags')).where('slug', '==', slug).limit(1).stream())
    if docs:
        return {'id': docs[0].id, **docs[0].to_dict()}
    return None


def create_tag(name: str, slug: str) -> str:
    db = get_db()
    _, ref = db.collection(_col('tags')).add({'name': name, 'slug': slug})
    return ref.id


# ─────────────────────────────────────────────────────────────────────────────
# POST QUERIES
# ─────────────────────────────────────────────────────────────────────────────

def _build_member_map(posts_data: list[dict]) -> dict:
    """Build a {member_id: member_dict} map from a list of raw post dicts."""
    member_ids = {p.get('member_id') for p in posts_data if p.get('member_id')}
    if not member_ids:
        return {}
    db = get_db()
    member_map = {}
    for mid in member_ids:
        doc = db.collection(_col('members')).document(mid).get()
        if doc.exists:
            member_map[mid] = _doc_to_member(doc)
    return member_map

def get_post_by_slug(slug: str):

    db = get_db()

    docs = list(
        db.collection(_col('posts'))
        .where(filter=FieldFilter("slug", "==", slug))
        .limit(1)
        .stream()
    )

    if not docs:
        return None

    return _doc_to_post(docs[0])

def get_posts(
    member_id: str = None,
    tag_slug: str = None,
    limit: int = None,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """
    Return (posts, total_count) with optional filtering.

    Parameters
    ----------
    member_id : filter by member
    tag_slug  : filter by tag slug
    limit     : max number of posts to return (None = all)
    offset    : number of posts to skip (for manual pagination)
    """
    db = get_db()
    col = db.collection(_col('posts'))
    query = col.order_by('created_at', direction=firestore.Query.DESCENDING)

    if member_id:
        query = query.where(filter=FieldFilter("member_id", "==", member_id))

    # Fetch all matching docs (Firestore doesn't support SQL OFFSET natively)
    all_docs = list(query.stream())

    # Tag filtering (done in Python because Firestore array-contains needs exact value)
    if tag_slug:
        tag = get_tag_by_slug(tag_slug)
        if tag:
            all_docs = [d for d in all_docs if tag['id'] in (d.to_dict() or {}).get('tag_ids', [])]
        else:
            all_docs = []

    total = len(all_docs)

    # Apply offset + limit
    sliced = all_docs[offset: offset + limit] if limit else all_docs[offset:]

    # Build member map for efficient lookup
    raw = [d.to_dict() or {} for d in sliced]
    member_map = _build_member_map(raw)

    posts = [_doc_to_post(d, member_map) for d in sliced]

    # Attach tags
    all_tags = {t['id']: t for t in get_all_tags()}
    for post in posts:
        post['tags'] = [all_tags[tid] for tid in post['tag_ids'] if tid in all_tags]

    return posts, total


def get_post_by_id(post_id: str) -> Optional[dict]:
    """Return a single post dict (with downloads, tags, member) or None."""
    db = get_db()
    doc = db.collection(_col('posts')).document(post_id).get()
    if not doc.exists:
        return None

    data = doc.to_dict() or {}
    member_id = data.get('member_id', '')
    member = get_member_by_id(member_id) if member_id else None

    post = _doc_to_post(doc, {member_id: member} if member else {})

    # Attach tags
    all_tags = {t['id']: t for t in get_all_tags()}
    post['tags'] = [all_tags[tid] for tid in post['tag_ids'] if tid in all_tags]

    # Fetch downloads sub-collection
    dl_docs = db.collection(_col('posts')).document(post_id).collection('downloads').stream()
    post['downloads'] = [{'id': d.id, **d.to_dict()} for d in dl_docs]

    return post


def get_related_posts(post: dict, limit: int = 3) -> list[dict]:
    """Return up to `limit` posts from the same member (excluding the post itself)."""
    member = post.get('member')
    if member:
        posts, _ = get_posts(member_id=member['id'], limit=limit + 1)
        return [p for p in posts if p['id'] != post['id']][:limit]
    posts, _ = get_posts(limit=limit + 1)
    return [p for p in posts if p['id'] != post['id']][:limit]


def get_adjacent_posts(post: dict) -> tuple[Optional[dict], Optional[dict]]:
    """
    Return (prev_post, next_post) relative to the given post's created_at.
    prev = older post, next = newer post.
    """
    db = get_db()
    created_at = post.get('created_at')
    if not created_at:
        return None, None

    col = db.collection(_col('posts'))

    # Older post (created before this one)
    prev_docs = list(
        col.order_by('created_at', direction=firestore.Query.DESCENDING)
           .where(filter=FieldFilter("created_at", "<", created_at))
           .limit(1)
           .stream()
    )
    prev_post = _doc_to_post(prev_docs[0]) if prev_docs else None

    # Newer post (created after this one)
    next_docs = list(
        col.order_by('created_at', direction=firestore.Query.ASCENDING)
           .where(filter=FieldFilter("created_at", ">", created_at))
           .limit(1)
           .stream()
    )
    next_post = _doc_to_post(next_docs[0]) if next_docs else None

    return prev_post, next_post


def create_post(
    title: str,
    content: str,
    excerpt: str = '',
    thumbnail_url: str = '',
    category: str = 'General',
    member_id: str = '',
    member_name: str = '',
    tag_ids: list = None,
) -> str:
    """Create a new post and return its Firestore document ID."""
    db = get_db()
    slug = slugify(title)
    _, ref = db.collection(_col('posts')).add({
        'title': title,
        'slug':slug,
        'excerpt': excerpt,
        'content': content,
        'thumbnail_url': thumbnail_url,
        'category': category,
        'member_id': member_id,
        'member_name': member_name,
        'tag_ids': tag_ids or [],
        'created_at': firestore.SERVER_TIMESTAMP,
        'updated_at': firestore.SERVER_TIMESTAMP,
    })
    # Update member post_count
    if member_id:
        db.collection(_col('members')).document(member_id).update(
            {'post_count': firestore.Increment(1)}
        )
    return ref.id


def update_post(post_id: str, **fields) -> None:
    """Update post fields (also sets updated_at)."""
    db = get_db()
    fields['updated_at'] = firestore.SERVER_TIMESTAMP
    db.collection(_col('posts')).document(post_id).update(fields)


def delete_post(post_id: str) -> None:
    """Delete a post and its downloads sub-collection."""
    db = get_db()
    post_ref = db.collection(_col('posts')).document(post_id)

    # Delete downloads sub-collection first
    for dl in post_ref.collection('downloads').stream():
        dl.reference.delete()

    post_ref.delete()


# ─────────────────────────────────────────────────────────────────────────────
# DOWNLOAD LINK QUERIES
# ─────────────────────────────────────────────────────────────────────────────

def add_download_link(
    post_id: str,
    label: str,
    url: str,
    host: str = 'other',
    file_size: str = '',
) -> str:
    """Add a download link to a post's sub-collection."""
    db = get_db()
    _, ref = (
        db.collection(_col('posts'))
          .document(post_id)
          .collection('downloads')
          .add({'label': label, 'url': url, 'host': host, 'file_size': file_size})
    )
    return ref.id


def delete_download_link(post_id: str, download_id: str) -> None:
    db = get_db()
    (
        db.collection(_col('posts'))
          .document(post_id)
          .collection('downloads')
          .document(download_id)
          .delete()
    )


# ─────────────────────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────────────────────

def get_site_stats() -> dict:
    """Return aggregate stats for the hero banner."""
    db = get_db()
    total_posts   = len(list(db.collection(_col('posts')).stream()))
    total_members = len(list(db.collection(_col('members')).stream()))

    # Count all download links across all posts
    total_downloads = 0
    for post_doc in db.collection(_col('posts')).stream():
        total_downloads += len(list(
            db.collection(_col('posts'))
              .document(post_doc.id)
              .collection('downloads')
              .stream()
        ))

    return {
        'total_posts': total_posts,
        'total_members': total_members,
        'total_downloads': total_downloads,
    }
