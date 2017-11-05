from django.db import models
from django.contrib.auth.models import User


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Judge(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    judge = models.ForeignKey(Judge)
    pid = models.CharField(max_length=15)
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    chapter = models.ForeignKey(Chapter)
    part = models.ForeignKey(Part)

    def solved_by(self):
        return self.userprofile_set.count()

    def get_link(self):
        if self.judge.slug == 'uva':
            return "https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem="+self.pid
        elif self.judge.slug == 'loj':
            return ''
        elif self.judge.slug == 'cf':
            return ''
        elif self.judge.slug == 'timus':
            return "http://acm.timus.ru/problem.aspx?num="+self.pid

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    cf_id = models.CharField(max_length=50, blank=True)
    loj_id = models.CharField(max_length=50, blank=True)
    uva_id = models.CharField(max_length=50, blank=True)
    timus_id = models.CharField(max_length=50, blank=True)

    solved_list = models.ManyToManyField(Problem)

    last_updated = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True)

    def get_name(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username

    def __str__(self):
        return self.user.username


class ProblemAlias(models.Model):
    problem = models.ForeignKey(Problem)
    pid = models.CharField(max_length=15)

    def __str__(self):
        return self.problem.pid + ' <-> ' + self.pid
