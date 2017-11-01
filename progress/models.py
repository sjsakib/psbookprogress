from django.db import models
from django.contrib.auth.models import User


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Part(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class Judge(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Problem(models.Model):
    judge = models.ForeignKey(Judge)
    pid = models.CharField(max_length=15)
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    chapter = models.ForeignKey(Chapter)
    part = models.ForeignKey(Part)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    cf_id = models.CharField(max_length=50)
    loj_id = models.CharField(max_length=50)
    uva_id = models.CharField(max_length=50)
    timus_id = models.CharField(max_length=50)
