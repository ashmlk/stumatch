from rest_framework import serializers
from .models import Message
import json

class MessageSerializer(serializers.Serializer):

    timestamp = serializers.SerializerMethodField()
    formatted_timestamp = serializers.SerializerMethodField()
    hashed_id = serializers.SerializerMethodField()
    replied_message = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    author_hashed_id = serializers.SerializerMethodField()
    author_full_name = serializers.SerializerMethodField()
    content = serializers.CharField()
    is_photo = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = fields
    
    def get_timestamp(self, obj):
        return obj.get_time_sent()

    def get_formatted_timestamp(self, obj):
        return obj.get_time_sent_formatted()
    
    def get_hashed_id(self, obj):
        return obj.get_hashid()
    
    def get_replied_message(self, obj):
        return obj.get_replied_message()
    
    def get_author_hashed_id(self, obj):
        return obj.get_author_hashed_id()
    
    def get_author_full_name(self, obj):
        return obj.get_author_full_name()
    
    def get_is_photo(self, obj):
        return obj.is_image_message()
    
    def get_photo_url(self, obj):
        return obj.get_photo_url()
    