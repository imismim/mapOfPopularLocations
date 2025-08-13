import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LocationSerializer, ReviewSerializer
from .models import Location, Review, ReviewSubscription


# @api_view(['GET'])
# def getLocations(request):
#     locations = Location.objects.all()
#     serializer = LocationSerializer(locations, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def getLocation(request, id):
    data = cache.get('location')
    
    if not data:
        location = Location.objects.get(id=id)
        data = LocationSerializer(location, many=False).data
        cache.set('location', data, timeout=300)
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createLocation(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateLocation(request, id):
    try:
        location = Location.objects.get(id=id, owner=request.user)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found or not owned by you'})

    partial = request.method == 'PATCH'

    serializer = LocationSerializer(location, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteLocation(request, id):
    try:
        location = Location.objects.get(id=id, owner=request.user)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found or not owned by you'})

    location.delete()
    return Response({'message': 'Location was deleted'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createReview(request, id):
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'})
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user, location=location)
        location.updateVoteTotal()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteReview(request, id):
    try:
        review = Review.objects.get(id=id, owner=request.user)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'})
    
    location = review.location
    review.delete()
    location.updateVoteTotal()
    return Response({'message': 'Review was deleted'})


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    
    filterset_fields = ['vote_total', 'category'] 

    search_fields = ['title', 'description']
    
    
@api_view(['GET'])
def exportLocations(request):
    formatType = request.GET.get('format').lower()
    
    locations = Location.objects.all()
    if formatType == 'csv':
        data = [{
            'ID': loc.id,
            'Title': loc.title,
            'Description': loc.description,
            'Link': loc.link_location,
            'Vote Total': loc.vote_total,
            'Created': loc.created
        } for loc in locations]

        df = pd.DataFrame(data)

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="locations.csv"'

        df.to_csv(response, index=False)
        return response
    else: 
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribeToLocation(request, id):
    location = get_object_or_404(Location, id=id)
    subscription, created = ReviewSubscription.objects.get_or_create(
        user=request.user,
        location=location
    )
    
    if not subscription.active:
        subscription.active = True
        subscription.save()

    return Response({'message': 'Subscribed successfully'})