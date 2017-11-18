from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    slug = models.SlugField(unique=True)
    points = models.IntegerField()

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
            return 'http://lightoj.com/volume_showproblem.php?problem='+self.pid
        elif self.judge.slug == 'cf':
            return 'http://codeforces.com/problemset/problem/'+'/'.join(self.pid.split('-'))
        elif self.judge.slug == 'timus':
            return "http://acm.timus.ru/problem.aspx?num="+self.pid

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    cf_id = models.CharField(max_length=50, blank=True, verbose_name='CF ID')
    loj_id = models.CharField(max_length=50, blank=True, verbose_name='LightOJ ID')
    uva_id = models.CharField(max_length=50, blank=True, verbose_name='UVa ID')
    timus_id = models.CharField(max_length=50, blank=True, verbose_name='Timus ID')

    solved_list = models.ManyToManyField(Problem, blank=True)

    last_updated = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True)
    points = models.IntegerField(default=0)

    location = models.CharField(max_length=100, blank=True)
    institute = models.CharField(max_length=100, blank=True)

    picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def get_name(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username
    get_name.short_description = 'Name'

    def get_progress(self):
        return int((self.points/Variable.get('total_points'))*100)

    def get_rank(self):
        all_users = UserProfile.objects.order_by('-points', 'last_updated')
        for i, u in enumerate(all_users):
            if u.pk == self.pk:
                return i+1
        return -1

    def get_tips(self):
        return self.tip_set.count()

    def save(self, *args, **kwargs):
        if self.picture:
            if self.pk:
                this = UserProfile.objects.get(pk=self.pk)
                if this.picture.name == self.picture.name:
                    super(UserProfile, self).save(*args, **kwargs)
                    return

            im = Image.open(self.picture)
            output = BytesIO()
            im = im.resize((150, 150))
            im = im.convert("RGB")
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            self.picture = InMemoryUploadedFile(output,
                                                'ImageField',
                                                '%s.jpg' % self.picture.name.split('.')[0],
                                                'image/jpeg', sys.getsizeof(output),
                                                None)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class ProblemAlias(models.Model):
    problem = models.ForeignKey(Problem)
    pid = models.CharField(max_length=15)

    def __str__(self):
        return self.problem.pid + ': ' + self.pid


class Variable(models.Model):
    name = models.CharField(max_length=100)
    dtype = models.CharField(max_length=10)
    value = models.CharField(max_length=200)

    def get_val(self):
        if self.dtype == 'str':
            return self.value
        elif self.dtype == 'int':
            return int(self.value)
        elif self.dtype == 'bool':
            return bool(self.value)

    @staticmethod
    def get(name):
        v = Variable.objects.get(name=name)
        return v.get_val()

    @staticmethod
    def set(name, value, dtype):
        v, _ = Variable.objects.get_or_create(name=name)
        v.value = str(value)
        v.dtype = dtype
        v.save()

    def __str__(self):
        return self.name + ': ' + self.value


class Tip(models.Model):
    problem = models.ForeignKey(Problem)
    author = models.ForeignKey(UserProfile)
    time = models.DateTimeField(blank=True, null=True)

    content = models.CharField(max_length=800)


def save_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(save_profile, sender=User)
