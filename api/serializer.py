from rest_framework import serializers
from .models import user,section,box,files


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = box
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = files
        fields = '__all__'