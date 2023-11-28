from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signUp, name="Signup"),
    path("creator/form/", views.creatorForm, name="creator_form"),
    path("profile/", views.profileView, name="profile"),
    path("creator/<int:pk>/", views.CreatorDetailView.as_view(), name="creator_detail")
]
