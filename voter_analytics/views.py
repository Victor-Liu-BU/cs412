# voter_analytics/views.py
# Ting Shing Liu, 10/31/25
# Views for Voter Analytics app

from datetime import datetime
from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go 
from django.db.models import Count, Q

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """
        Overrides the default queryset to implement filtering.
        """
        # Start with all voters
        queryset = super().get_queryset()

        # Get filter parameters from the request's GET dictionary
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        score = self.request.GET.get('voter_score')
        
        # Election checkboxes
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        # Apply filters if they are present and not empty
        if party:
            queryset = queryset.filter(party_affiliation=party)
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)
            
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)
            
        if score:
            queryset = queryset.filter(voter_score=score)

        # Apply checkbox filters (only filter if the box is checked)
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Passes filter options and current filter values to the template.
        """
        # Get the default context
        context = super().get_context_data(**kwargs)
        
        # Add data for filter <select> options to the context
        
        # Get distinct party affiliations from the DB
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        
        # Get distinct voter scores from the DB
        context['score_options'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('-voter_score')
        
        # Generate a list of years for the date of birth dropdowns
        current_year = datetime.now().year
        context['year_options'] = range(current_year, 1900, -1) # Years 2024 down to 1901
        
        # Pass current filter values back to the template 
        # This allows the form to "remember" the user's selections
        context['current_filters'] = self.request.GET
        
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(VoterListView):
    """
    A view that inherits from VoterListView to display
    graphs based on the filtered data.
    """
    # Use a new template
    template_name = 'voter_analytics/graphs.html'
    
    # We are not paginating the graphs, so set this to None
    paginate_by = None 

    def get_context_data(self, **kwargs):
        """
        1. Calls the parent (VoterListView) to get all the
           filter options context.
        2. Gets the filtered queryset.
        3. Generates graphs based on that queryset.
        4. Adds the graph HTML to the context.
        """
        # Get the base context from VoterListView
        # This will include 'party_options', 'year_options', etc.
        context = super().get_context_data(**kwargs)
        
        # Get the fully filtered queryset
        # self.get_queryset() runs the inherited method with all
        # the same request.GET logic.
        filtered_qs = self.get_queryset()

        # Generate Graphs
        
        # Graph 1: Birth Year Histogram 
        # Get a list of all birth years from the filtered queryset
        birth_years = list(filtered_qs.values_list('date_of_birth__year', flat=True))
        
        if birth_years:
            fig1 = go.Figure(
                data=[go.Histogram(x=birth_years)]
            )
            fig1.update_layout(
                title_text='Voter Distribution by Birth Year',
                xaxis_title='Birth Year',
                yaxis_title='Count'
            )
            # Convert to HTML div
            context['birth_year_graph'] = plotly.offline.plot(fig1, auto_open=False, output_type="div")
        
        # Graph 2: Party Affiliation Pie Chart 
        # Get a count of each party, grouped by party
        party_data = filtered_qs.values('party_affiliation').annotate(
            count=Count('party_affiliation')
        ).order_by('-count')
        
        if party_data:
            fig2 = go.Figure(
                data=[go.Pie(
                    labels=[item['party_affiliation'] for item in party_data], 
                    values=[item['count'] for item in party_data]
                )]
            )
            fig2.update_layout(title_text='Voter Distribution by Party Affiliation')
            # Convert to HTML div
            context['party_pie_chart'] = plotly.offline.plot(fig2, auto_open=False, output_type="div")

        # Graph 3: Election Participation Bar Chart 
        # Aggregate counts for each election column where the value is True
        election_counts = filtered_qs.aggregate(
            v20state=Count('pk', filter=Q(v20state=True)),
            v21town=Count('pk', filter=Q(v21town=True)),
            v21primary=Count('pk', filter=Q(v21primary=True)),
            v22general=Count('pk', filter=Q(v22general=True)),
            v23town=Count('pk', filter=Q(v23town=True)),
        )

        if election_counts:
            elections = ['20 State', '21 Town', '21 Primary', '22 General', '23 Town']
            counts = [
                election_counts['v20state'],
                election_counts['v21town'],
                election_counts['v21primary'],
                election_counts['v22general'],
                election_counts['v23town']
            ]
            
            fig3 = go.Figure(data=[go.Bar(x=elections, y=counts)])
            fig3.update_layout(
                title_text='Voter Participation by Election',
                xaxis_title='Election',
                yaxis_title='Number of Voters'
            )
            # Convert to HTML div
            context['election_bar_chart'] = plotly.offline.plot(fig3, auto_open=False, output_type="div")

        return context