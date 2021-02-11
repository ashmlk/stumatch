from rest_framework import serializers
from friendship.models import Friend, Follow, Block, FriendshipRequest
from .models import Profile

class ProfileSerializer(serializers.Serializer):
    
    id = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField()
    university = serializers.ReadOnlyField()
    program = serializers.ReadOnlyField()
    bio = serializers.ReadOnlyField()
    profile_image_url = serializers.ReadOnlyField(source='image.url')
    is_private = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    friend_count = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    viewer_is_friend = serializers.SerializerMethodField()
    viewer_sent_request = serializers.SerializerMethodField()
    viewer_received_request = serializers.SerializerMethodField()
    mutual_friends_info = serializers.SerializerMethodField()
    mutual_course_info = serializers.SerializerMethodField()
    profile_absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = fields
    
    def get_id(self, obj):
        return obj.get_hashid()
    
    def get_is_private(self, obj):
        return not obj.public
    
    def get_profile_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_friend_count(self, obj):
        return len(Friend.objects.friends(obj))
    
    def get_course_count(self, obj):
        return obj.courses.count()
    
    def get_post_count(self, obj):
        return obj.post_set.count()
    
    def get_viewer_is_friend(self, obj):
        viewer = self.context['viewer']
        return Friend.objects.are_friends(viewer, obj)
    
    def get_viewer_sent_request(self, obj):
        viewer = self.context['viewer']
        return FriendshipRequest.objects.filter(
            from_user=viewer, to_user=obj
        ).exists()
    
    def get_viewer_received_request(self, obj):
        viewer = self.context['viewer']
        return FriendshipRequest.objects.filter(
            from_user=obj, to_user=viewer
        ).exists()
    
    def get_mutual_friends_info(self, obj):
        viewer_friend_ids = self.context['viewer_friend_ids']
        obj_friend_ids = set([u.id for u in Friend.objects.friends(obj)])
        mutuals = viewer_friend_ids & obj_friend_ids
        mutual_friends_usernames = list(Profile.objects.filter(id__in=mutuals).order_by('username').values_list('username',flat=True))
        return {
            "count": len(mutuals),
            "id":list(mutuals),
            "usernames":mutual_friends_usernames,
        }
    
    def get_mutual_course_info(self, obj):
        viewer_courses = self.context['viewer_courses']
        viewer_university = self.context['viewer_university']
        obj_courses = set([c.course_code for c in obj.courses.filter(course_university=viewer_university)])
        mutuals = viewer_courses & obj_courses
        return {
            "count":len(mutuals),
            "codes":list(mutuals)
        }

    
    