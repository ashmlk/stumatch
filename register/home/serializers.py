from rest_framework import serializers
from .models import Comment
from main.models import Profile

class CommentSerializer(serializers.Serializer):
    
    timestamp = serializers.SerializerMethodField()
    hashed_id = serializers.SerializerMethodField()
    name_username = serializers.ReadOnlyField(source='name.username')
    name_image_url = serializers.ReadOnlyField(source='name.image.url')
    name_hashed_id = serializers.SerializerMethodField()
    body = serializers.CharField()
    like_count = serializers.SerializerMethodField()
    viewer_has_liked = serializers.SerializerMethodField()
    has_replies = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = fields
        
    def get_timestamp(self, obj):
        return obj.get_created_on()
    
    def get_hashed_id(self, obj):
        return obj.get_hashid()
    
    def get_name_username(self, obj):
        return obj.name.get_username()
    
    def get_name_image_url(self, obj):
        return obj.name.image.url
    
    def get_name_hashed_id(self, obj):
        return obj.name.get_hashid()
    
    def get_like_count(self, obj):
        c = obj.likes.count() 
        return c if c > 0 else ''
    
    def get_has_replies(self, obj):
        return obj.replies.exists()
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def get_viewer_has_liked(self, obj):
        try:
            liked_by_viewer = self.context['liked_by_viewer']
        except KeyError:
            liked_by_viewer = []
        return True if obj.id in liked_by_viewer else False