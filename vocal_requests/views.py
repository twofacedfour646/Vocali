from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView
from .models import VocalRequest

# Create your views here.
class RequestDetailView(DetailView):
    model = VocalRequest
    template_name = "requestDetailPage.html"
    context_object_name = "request"

    # Send context to template
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
