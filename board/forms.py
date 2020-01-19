from django import forms
from .models import Topic, Post


class NewTopic(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 6, 'placeholder': 'What''s on your mind?'}
            ),
        max_length=4000,
        help_text='Max length is 4000 characters.'
        )

    def __init__(self, *args, **kwargs):
        super(NewTopic, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['placeholder'] = 'Enter New Topic'

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class NewReply(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']