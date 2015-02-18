from django.db import models


class Publication(models.Model):
    author = models.ForeignKey('accounts.Account')
    content = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    to_publication = models.ForeignKey('self', null=True, related_name='+')

    LIKE, COMMENT, ARTICLE = range(3)
    TYPE_CHOICES = (
        (LIKE, 'like'),
        (COMMENT, 'comment'),
        (ARTICLE, 'article'),
    )
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=LIKE)

    @property
    def likes(self):
        return Publication.objects.filter(to_publication=self, type=self.LIKE)

    @property
    def first_like_and_others(self):
        raise NotImplementedError

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments(self):
        return Publication.objects.filter(to_publication=self, type=self.COMMENT)

    @property
    def comments_count(self):
        return self.comments.count()
