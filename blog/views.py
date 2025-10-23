from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
import random
# Create your views here.

class ShowAllView(ListView):
    '''Define a class to show all blog Articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)
    
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
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    """A form to handle the creation of a new Article
    [1] Display the html form to the user's {GET}
    [2] Process the form submission and store the new Article object {POST}"""

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
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
    

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
 
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')
    
class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
 