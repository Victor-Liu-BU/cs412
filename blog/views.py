from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse

import random
# Create your views here.

class ShowAllView(ListView):
    '''Define a class to show all blog Articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name 

class RandomArticleView(DetailView):
    '''Display a random article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name 

    def get_object(self):
        """returns one instance of the Article object selected at random"""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class CreateArticleView(CreateView):
    """A form to handle the creation of a new Article
    [1] Display the html form to the user's {GET}
    [2] Process the form submission and store the new Article object {POST}"""

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        '''Override the default method to add some debug information'''

        # Print out the form data:
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        # Delegate work to the superclass to do the rest 
        return super().form_valid(form)

class CreateCommentView(CreateView):
    """A view to handle creation of a new Comment on an Article"""
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        """Provide a url to direct to after a successful submission when making a new comment"""

        # Retrieve the pk from the URL
        pk = self.kwargs['pk']
        return reverse("article",kwargs={'pk':pk})
    
    def get_context_data(self):
        # Calling the superclass method 
        context = super().get_context_data()
        
        # find/add article to the context data
        # Retrieve the pk from the URL
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # Add this article to the context dictionary
        context['article'] = article
        return context
    
    def form_valid(self, form):
        """This method handles the form submission and saves the new object 
        to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database."""

        print(form.cleaned_data)
        # Retrieve the pk from the URL
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # Attach this article to the comment
        form.instance.article = article # Set the Foreign Key

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    """View class to handle the update of an Article based on its PK"""

    model = Article
    form_class = UpdateArticleForm
    template_name = 'blog/update_article_form.html'

class DeleteCommentView(DeleteView):
    """View class to handle the deletion of a Comment on an Article"""

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        """Return a url to return to after a successful deletion"""

        # find the PK for this comment:
        pk = self.kwargs['pk']
        # find the Comment object:
        comment = Comment.objects.get(pk=pk)
        
        # find the PK of the article for which this comment is associated to 
        article = comment.article

        # return the URL to redirect to:
        return reverse('article', kwargs={'pk': article.pk})