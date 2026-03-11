"""
Lightweight dataclass wrappers around Firestore documents.

These are NOT Django ORM models — they have no database table.
They exist purely so that Django templates can use dot-notation
(e.g. post.title, post.member.name) and so that the paginator
can work with a list of objects.

The actual data lives in Firebase Firestore and is fetched via
fansub.firebase_service.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Tag:
    id: str
    name: str
    slug: str = ''

    def __str__(self) -> str:
        return self.name


@dataclass
class DownloadLink:
    id: str
    label: str
    url: str
    host: str = 'other'
    file_size: str = ''

    def __str__(self) -> str:
        return self.label


@dataclass
class Member:
    id: str
    name: str
    avatar_url: str = ''
    post_count: int = 0
    created_at: Optional[datetime] = None

    # Alias so templates can use member.pk
    @property
    def pk(self) -> str:
        return self.id

    # Fake ImageField-like object so templates can use member.avatar.url
    @property
    def avatar(self):
        if self.avatar_url:
            return _FakeImageField(self.avatar_url)
        return None

    def __str__(self) -> str:
        return self.name


@dataclass
class Post:
    id: str
    title: str
    excerpt: str = ''
    content: str = ''
    thumbnail_url: str = ''
    category: str = 'General'
    member: Optional[Member] = None
    tags: list = field(default_factory=list)
    downloads: list = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Alias so templates can use post.pk
    @property
    def pk(self) -> str:
        return self.id

    # Fake ImageField-like object so templates can use post.thumbnail.url
    @property
    def thumbnail(self):
        if self.thumbnail_url:
            return _FakeImageField(self.thumbnail_url)
        return None

    def __str__(self) -> str:
        return self.title


class _FakeImageField:
    """Mimics Django's FieldFile so templates can call .url on it."""

    def __init__(self, url: str):
        self._url = url

    @property
    def url(self) -> str:
        return self._url

    def __bool__(self) -> bool:
        return bool(self._url)

    def __str__(self) -> str:
        return self._url


# ─────────────────────────────────────────────────────────────────────────────
# FACTORY FUNCTIONS
# Convert raw firebase_service dicts → dataclass instances
# ─────────────────────────────────────────────────────────────────────────────

def member_from_dict(d: dict) -> Member:
    return Member(
        id=d.get('id', ''),
        name=d.get('name', ''),
        avatar_url=d.get('avatar_url', ''),
        post_count=d.get('post_count', 0),
        created_at=d.get('created_at'),
    )


def tag_from_dict(d: dict) -> Tag:
    return Tag(
        id=d.get('id', ''),
        name=d.get('name', ''),
        slug=d.get('slug', ''),
    )


def download_from_dict(d: dict) -> DownloadLink:
    return DownloadLink(
        id=d.get('id', ''),
        label=d.get('label', ''),
        url=d.get('url', ''),
        host=d.get('host', 'other'),
        file_size=d.get('file_size', ''),
    )


def post_from_dict(d: dict) -> Post:
    member_data = d.get('member')
    member = member_from_dict(member_data) if member_data else None

    tags = [tag_from_dict(t) for t in d.get('tags', [])]
    downloads = [download_from_dict(dl) for dl in d.get('downloads', [])]

    return Post(
        id=d.get('id', d.get('pk', '')),
        title=d.get('title', ''),
        slug=d.get('slug', ''),
        excerpt=d.get('excerpt', ''),
        content=d.get('content', ''),
        thumbnail_url=d.get('thumbnail_url', ''),
        category=d.get('category', 'General'),
        member=member,
        tags=tags,
        downloads=downloads,
        created_at=d.get('created_at'),
        updated_at=d.get('updated_at'),
    )
