from django.shortcuts import redirect
from django.urls import path, reverse

from home.views import home_page

urlpatterns = [
    path('home/', view=home_page, name="home"),
    path('', view=lambda request: redirect(reverse("home"))),
    # path('home/<str:event_id>/', view=get_event_detail, name="event_detail"),
]
