from django.urls import path
from .views import follow_person, list_following, list_follower, unfollow_person, is_follow_person_API

urlpatterns = [
    path('follow-person/', follow_person, name="follow"),
    path('list-following/', list_following, name="following"),
    path('list-follower/', list_follower, name="follower"),
    path('unfollow-person/', unfollow_person, name="unfollow"),
    path('is-follow/', is_follow_person_API, name="isfollow"),
]
