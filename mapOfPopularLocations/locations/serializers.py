from rest_framework import serializers
from .models import Location, Review
from user.serializers import UserSerializer

class LocationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = '__all__'
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
