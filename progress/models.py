from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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
            return ''
        elif self.judge.slug == 'cf':
            return ''
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

    solved_list = models.ManyToManyField(Problem)

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

    def get_progress(self):
        return int((self.points/Variable.get('total_points'))*100)

    def get_rank(self):
        all_users = UserProfile.objects.order_by('points', 'last_updated')
        for i, u in enumerate(all_users):
            if u.pk == self.pk:
                return i+1
        return -1

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


def save_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(save_profile, sender=User)
