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
    GENDER_CHOICES =( 
        ("남자", "남자"), 
        ("여자", "여자")
    ) 

    AGE_CHOICES =(
        ('10대', '10대'),
        ('20대', '20대'),
        ('30대', '30대'),
        ('40대 이상', '40대 이상'),
    )

    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='media/%Y/%m')
    message = models.TextField(blank=True, null=True)
    face = models.ForeignKey(Face, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.face,self.gender)

    def get_absolute_url(self):
        return '/face/facehist/{}'.format(self.pk)
