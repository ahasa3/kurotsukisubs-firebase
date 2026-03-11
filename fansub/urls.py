"""
URL patterns for the fansub app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.member_posts, name='member_posts'),
    # Post IDs in Firestore are strings (auto-generated document IDs)
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
