from django.urls import path
from .views import HelloView


urlpatterns = [
    path('api/hello/', HelloView.as_view(), name='hello'),
]