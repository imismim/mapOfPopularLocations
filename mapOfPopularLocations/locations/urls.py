from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import api_views

urlpatterns = [
    path("locations/", api_views.getLocations, name="getLocations"),
    path("locations/create/", api_views.createLocation, name="createLocation"),
    
    path("locations/<str:id>/", api_views.getLocation, name="getLocation"),
    path("locations/<str:id>/update", api_views.updateLocation, name="updateLocation"),
    path("locations/<str:id>/delete", api_views.deleteLocation, name="deleteLocation"),
    
    path("locations/<str:id>/add-review", api_views.createReview, name="createReview"),
    path("reviews/<str:id>/delete", api_views.deleteReview, name="deleteReview"),
]
