from typing import Any
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreatorForm, ReviewForm
from django.contrib.auth import login
from vocali.settings import storage
from django.contrib.auth.decorators import login_required
from .models import Profile, Review
from django.views.generic import DetailView
from vocal_requests.forms import RequestForm
from django.utils import timezone
from django.contrib import messages

# Upload file to specific folder in firebase
def upload_file_to_firebase(file, folder):
    # Upload file to Firebase Storage
    file_url = storage.child(folder).put(file)['downloadTokens']
    # Get the public download URL
    return storage.child(folder).get_url(file_url)


# Delete review
def deleteReview(request, pk):
    # Get review
    review = Review.objects.get(id=pk)

    # Get creator Id to redirect
    creatorId = review.receiver.id

    # Delete review
    review.delete()

    # Redirect back to creator page with success message
    messages.success(request, "Review deleted")
    return redirect("/creator/" + str(creatorId))

# View for specific creator page
class CreatorDetailView(DetailView):
    model = Profile
    template_name = "creatorDetailPage.html"
    context_object_name = "creator"

    # Sends context to template
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = RequestForm(instance=self.object)
        context["reviewForm"] = ReviewForm(instance=self.object)
        context["myReviews"] = Review.objects.filter(receiver=self.get_object())
        context["creator_update_form"] = CreatorForm(instance=self.object)
        return context
    
    # Called on post request from template
    def post(self, request, *args, **kwargs):
        # Check if the creator update form has been submitted
        if "bio" in request.POST:
            # Generate form populated with submitted data
            creatorForm = CreatorForm(request.POST, request.FILES, instance=self.get_object())

            # Check if form is valid
            if creatorForm.is_valid():
                # Get saved model
                creatorUpdated = creatorForm.save(commit=False)

                # Check for avatar and banner file submissions
                if "avatar" in request.FILES:
                    avatar_path = f'media/avatars/{request.FILES["avatar"].name}'
                    avatar_url = upload_file_to_firebase(request.FILES['avatar'], avatar_path)
                    creatorUpdated.avatar = avatar_url

                # If a banner is uploaded, store the URL in the model
                if 'banner' in request.FILES:
                    banner_path = f'media/banners/{request.FILES["banner"].name}'
                    banner_url = upload_file_to_firebase(request.FILES['banner'], banner_path)
                    creatorUpdated.banner = banner_url

                # Commit save to all fields
                creatorUpdated.save()

                # Redirect to home page with success message
                messages.success(request, "Profile Updated")
                return redirect("/creator/" + str(self.get_object().pk))
        else:
            # Check which form was submitted
            if "rating" in request.POST:
                # Set requested form to review form with review message
                requestForm = ReviewForm(request.POST)
                successMsg = "Review submitted successfully!"
            else:
                # Set requested form to vocal request form with vocal request message
                requestForm = RequestForm(request.POST)
                successMsg = "Vocal Request submitted successfully!"
            
            # Check that submitted form is valid
            if requestForm.is_valid():
                # Create object of submitted form data
                requestObject = requestForm.save(commit=False)

                # Set fields not asked for in form
                requestObject.sender = request.user
                requestObject.receiver = self.get_object()
                requestObject.datePosted = timezone.now()

                # Save object data
                requestObject.save()

                # Redirect to home page with success message
                messages.success(request, successMsg)
                return redirect("/creator/" + str(self.get_object().pk))

        # If form data invalid, stay on creator page and push error message
        messages.error(request, "Something went wrong. Please try again.")
        return redirect("/creator/" + str(self.get_object().pk))


def profileView(request):
    return render(request, "profile.html")


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
