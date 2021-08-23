from decimal import Decimal

from rest_framework import serializers

from main.models import *


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'user', 'category', 'text', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(user=request.user, **validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentsSerializer(instance.comments.all(), many=True).data
        representation['likes'] = LikesSerializer(instance.likes.all(), many=True).data
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data

        rates = Rating.objects.filter(post=instance)
        if not rates:
            representation['rating'] = 'null'
        else:
            sum = 0
            for i in rates:
                sum = sum + i.rating
            representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(post=instance).count())
        return representation


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comments
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        post = Comments.objects.create(user=request.user, **validated_data)
        return post


class LikesSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        post = Likes.objects.create(user=request.user, **validated_data)
        return post


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        rating, obj = Rating.objects.update_or_create(user=request.user, **validated_data)
        return rating


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Bookmark
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['title'] = PostSerializer(instance.post).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        post = Bookmark.objects.create(user=request.user, **validated_data)
        return post


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('image',)

    def _get_image_url(self, obj):
        print()
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url
