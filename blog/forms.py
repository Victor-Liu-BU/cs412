# blog/forms.py
# define the forms that we use for create/update/delete operations 

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database"""

    class Meta:
        """Associate this form with a model in the database"""
        model = Article
        fields = ['author', 'title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    """A form to add comments about an Article"""

    class Meta:
        """Associate this form with a model in the database"""
        model = Comment
        fields = ["author", "text"]