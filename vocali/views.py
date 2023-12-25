from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from vocal_requests.models import VocalRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.forms import SearchForm
from django.contrib.auth.models import User

def landing(request):
    if request.user.is_authenticated:
        return redirect("/home")
    return render(request, "landing.html", {})


@login_required
def home(request):
    # Get all creators in 3 creator intervals
    creator_list = Profile.objects.all()

    creators_per_page = 3
    paginator = Paginator(creator_list, creators_per_page)

    page = request.GET.get("page")
    try:
        creators = paginator.page(page)
    except PageNotAnInteger:
        creators = paginator.page(1)
    except EmptyPage:
        creators = paginator.page(paginator.num_pages)

    return render(request, "home.html", {"creators": creators})


@login_required
def searchView(request):
    results = Profile.objects.all()[:5]
    form = SearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        results = User.objects.filter(username__icontains=query)

    return render(request, "search.html", {"creators": results, "form": form})
