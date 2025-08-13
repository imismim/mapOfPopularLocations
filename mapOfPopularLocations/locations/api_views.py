from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import LocationSerializer, ReviewSerializer
from .models import Location, Review


@api_view(['GET'])
def getLocations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLocation(request, id):
    location = Location.objects.get(id=id)
    serializer = LocationSerializer(location, many=False)
    return Response(serializer.data)


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
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteReview(request, id):
    try:
        review = Review.objects.get(id=id, owner=request.user)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'})
    
    review.delete()
    return Response({'message': 'Review was deleted'})
