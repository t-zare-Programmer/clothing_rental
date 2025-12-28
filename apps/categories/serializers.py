from rest_framework import serializers
from .models import Category

#___________________________________________________________________________________________
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
