from rest_framework import serializers

from .models import Category, Feature, Event, Enroll, Review, Favorite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('title', )


class EventSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    category_name = serializers.CharField(source='category.title')
    number_of_enrolled = serializers.IntegerField(source='display_enroll_count')

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'category_name', 'date_start', 'participants_number',
                  'number_of_enrolled', 'is_private', 'features')


class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
