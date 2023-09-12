from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from contribution_catalog.models import Contributor, Person, Affiliation, Contribution
# Create your views here.

#___________________________________________________________________________________________
class ContributorListView(generic.ListView):
    """Generic class-based view for a list of contributors."""
    model = Contributor
    paginate_by = 10

#___________________________________________________________________________________________
class ContributorDetailView(generic.DetailView):
    """Generic class-based detail view for a contributor."""
    model = Contributor

#___________________________________________________________________________________________
class PersonListView(generic.ListView):
    """Generic class-based view for a list of persons."""
    model = Person
    paginate_by = 10

#___________________________________________________________________________________________
class PersonDetailView(generic.DetailView):
    """Generic class-based detail view for a contributor."""
    model = Person

#___________________________________________________________________________________________
class AffiliationListView(generic.ListView):
    """Generic class-based view for a list of affiliations."""
    model = Affiliation
    paginate_by = 10

#___________________________________________________________________________________________
class AffiliationDetailView(generic.DetailView):
    """Generic class-based detail view for an affiliation."""
    model = Affiliation

    #___________________________________________________________________________________________
class ContributionListView(generic.ListView):
    """Generic class-based view for a list of contributions."""
    model = Contribution
    paginate_by = 10

#___________________________________________________________________________________________
class ContributionDetailView(generic.DetailView):
    """Generic class-based detail view for a contribution."""
    model = Contribution
