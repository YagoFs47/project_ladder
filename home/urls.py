from django.urls import include, path, reverse
from home.views import home
from django.shortcuts import redirect



urlpatterns = [
    path('home/', view=home, name="home"),
    path('', view=lambda request: redirect(reverse("home"))),
    # path('home/<str:event_id>/', view=get_event_detail, name="event_detail"),
]