from typing import Any
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreatorForm, ReviewForm
from django.contrib.auth import login
from vocali.settings import storage
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views.generic import DetailView
from vocal_requests.forms import RequestForm
from django.utils import timezone
from django.contrib import messages


class CreatorDetailView(DetailView):
    model = Profile
    template_name = "creatorDetailPage.html"
    context_object_name = "creator"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = RequestForm(instance=self.object)
        context["reviewForm"] = ReviewForm(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        requestForm = RequestForm(request.POST)
        
        if requestForm.is_valid():
            requestObject = requestForm.save(commit=False)

            requestObject.sender = request.user
            requestObject.receiver = self.get_object()
            requestObject.datePosted = timezone.now()

            requestObject.save()

            messages.success(request, 'Vocal Request submitted successfully!')
            return redirect("/home")

        messages.error(request, "Something went wrong. Please try again.")
        return redirect("/creator/" + self.get_object().pk)


def profileView(request):
    return render(request, "profile.html")


def upload_file_to_firebase(file, folder):
    # Upload file to Firebase Storage
    file_url = storage.child(folder).put(file)['downloadTokens']
    # Get the public download URL
    return storage.child(folder).get_url(file_url)


# Authentication templates
@login_required
def creatorForm(request):
    if Profile.objects.filter(user=request.user).exists():
        return redirect("/home")

    if request.method == "POST":
        form = CreatorForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.isCreator = True
            user_profile.activated = False
            user_profile.earnings = 0.0

            if 'avatar' in request.FILES:
                avatar_path = f'media/avatars/{request.FILES["avatar"].name}'
                avatar_url = upload_file_to_firebase(request.FILES['avatar'], avatar_path)
                user_profile.avatar = avatar_url

            # If a banner is uploaded, store the URL in the model
            if 'banner' in request.FILES:
                banner_path = f'media/banners/{request.FILES["banner"].name}'
                banner_url = upload_file_to_firebase(request.FILES['banner'], banner_path)
                user_profile.banner = banner_url

            
            user_profile.save()
            return redirect("/home")

    else:
        form = CreatorForm()

    return render(request, "creatorForm.html", {"form": form})


def signUp(request):
    if request.user.is_authenticated:
        return redirect("/home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("/home")
    else:
        form = RegistrationForm()

    return render(request, "registration/signUp.html", {"form": form})
