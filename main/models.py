from django.db import models

from account.models import CustomUser


class Categories(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.like


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f'{self.rating}'


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
    choice = models.BooleanField(default=False)

    def __str__(self):
        return self.post


class Images(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
