from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Face(models.Model):
    kind = models.CharField(max_length=20)
    content = MarkdownxField()
    artist = MarkdownxField()
    def __str__(self):
        return '{}'.format(self.kind)

    def get_markdown_content(self):
        return markdown(self.content)
    def get_markdown_artist(self):
        return markdown(self.artist)

class FaceHist(models.Model):
    # unique_id = models.AutoField(primary_key=True)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='media/%Y/%m')
    message = models.TextField(blank=True, null=True)
    face = models.ForeignKey(Face, on_delete=models.CASCADE, blank=True, null=True)
    kinds = models.CharField(max_length=50, null=True)
    scores = models.CharField(max_length=30, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.face,self.gender)

    def get_absolute_url(self):
        return '/face/facehist/{}'.format(self.pk)

class FaceScore(models.Model):
    kind = models.CharField(max_length=50)
    score = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.kind)