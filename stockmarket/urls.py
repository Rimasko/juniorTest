from django.urls import path
from .views import DealsAPIView

urlpatterns = [
    path('deals/', DealsAPIView.as_view()),
]
