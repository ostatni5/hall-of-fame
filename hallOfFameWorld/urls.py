from django.urls import path

from hallOfFameWorld.views import WorldView

app_name = 'world'
urlpatterns = [
    path('',WorldView.as_view(),name="main"),
]