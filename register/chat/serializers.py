from rest_framework import serializers
from .models import Message
import json

class MessageSerializer(serializers.ModelSerializer):

    timestamp = serializers.SerializerMethodField()
    formatted_timestamp = serializers.SerializerMethodField()
    hashed_id = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Message
        fields = "__all__"
    
    def get_timestamp(self, obj):
        return obj.get_time_sent()

    def get_formatted_timestamp(self, obj):
        return obj.get_time_sent_formatted()
    
    def get_hashed_id(self, obj):
        return obj.get_hashid()
    