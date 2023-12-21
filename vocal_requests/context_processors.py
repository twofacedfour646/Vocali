from users.models import Profile
from vocal_requests.models import VocalRequest


def navbar_context(request):
    # Add your specific context for the navbar
    # Get all incoming requests if user is a creator
    currentCreatorsRequests = None
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            currentCreatorsRequests = VocalRequest.objects.filter(receiver=request.user.profile)
        
        mySentRequests = VocalRequest.objects.filter(sender=request.user)

    return {'myRequests': currentCreatorsRequests, 'sentRequests': mySentRequests}