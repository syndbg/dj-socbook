from django.db import models


class Publication(models.Model):
    PUBLIC, PRIVATE = range(2)
    VISIBILITY_CHOICES = (
        PUBLIC, 'Public',
        PRIVATE, 'Private')

    author = models.ForeignKey('profiles.Profile', null=True)
    title = models.CharField(max_length=125, blank=False)
    content = models.TextField(max_length=500, blank=False)
    visibility = models.SmallIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class PublicationComment(models.Model):
    author = models.ForeignKey('profiles.Profile', null=True)
    content = models.TextField(max_length=500, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    publication = models.ForeignKey(Publication, related_name='comments')


class PublicationLike(models.Model):
    author = models.ForeignKey('profiles.Profile', null=True)
    publication = models.ForeignKey(Publication, related_name='likes')
