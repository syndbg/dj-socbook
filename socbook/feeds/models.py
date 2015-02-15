from django.db import models


class Publication(models.Model):
    author = models.ForeignKey('profiles.Profile', null=True)
    title = models.CharField(max_length=125, blank=False)
    content = models.TextField(max_length=500, blank=False)

    class Meta:
        unique_together = (('author', 'title'),)


class PublicationComment(models.Model):
    author = models.ForeignKey('profiles.Profile', null=True)
    content = models.TextField(max_length=500, blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    publication = models.ForeignKey(Publication, related_name='comments')
