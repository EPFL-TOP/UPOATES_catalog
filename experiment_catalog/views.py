from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from experiment_catalog.models import Experiment
# Create your views here.

#___________________________________________________________________________________________
class ExperimentListView(generic.ListView):
    """Generic class-based view for a list of experiments."""
    model = Experiment
    paginate_by = 50

#___________________________________________________________________________________________
class ExperimentDetailView(generic.DetailView):
    """Generic class-based detail view for an experiment."""
    model = Experiment

