from django import forms
from django.contrib.auth.models import User
from progress.models import UserProfile, Tip

import bleach


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('uva_id', 'cf_id', 'loj_id', 'timus_id', 'location', 'institute', 'picture')


class TipForm(forms.ModelForm):
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ['iframe', 'pre']
    allowed_attributes = {**bleach.sanitizer.ALLOWED_ATTRIBUTES, **{'iframe': ['src', 'frameborder', 'allowfullscreen']}}

    help_text = "Supported HTML tags are: " + ', '.join(allowed_tags)
    help_text += ".\n Use <pre> for block text, like sample input"
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': help_text}))

    def clean_content(self):
        content = self.cleaned_data['content']
        content = bleach.clean(content, tags=self.allowed_tags, attributes=self.allowed_attributes)

        return bleach.linkify(content)

    class Meta:
        model = Tip
        fields = ('content', )
