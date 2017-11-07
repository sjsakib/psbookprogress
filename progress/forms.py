from django import forms
from django.contrib.auth.models import User
from progress.models import UserProfile


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('uva_id', 'cf_id', 'loj_id', 'timus_id', 'location', 'institute', 'picture')
