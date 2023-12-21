from django.urls import path
from . import views

urlpatterns = [
    path("request/<int:pk>/", views.RequestDetailView.as_view(), name="vocal_request"),
]
