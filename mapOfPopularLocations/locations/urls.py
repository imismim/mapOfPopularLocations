from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r'locations', api_views.LocationViewSet, basename='location')

urlpatterns = [
    path("locations/export/", api_views.exportLocations, name="exportlocations"),
    path("locations/create/", api_views.createLocation, name="createLocation"),
    
    path("locations/<str:id>/", api_views.getLocation, name="getLocation"),
    path("locations/<str:id>/update", api_views.updateLocation, name="updateLocation"),
    path("locations/<str:id>/delete", api_views.deleteLocation, name="deleteLocation"),
    
    path("locations/<str:id>/add-review", api_views.createReview, name="createReview"),
    path("reviews/<str:id>/delete", api_views.deleteReview, name="deleteReview"),
    path("reviews/<str:id>/subscribe", api_views.subscribeToLocation, name="subscribeToLocation"),
    path('', include(router.urls)),
    
]
