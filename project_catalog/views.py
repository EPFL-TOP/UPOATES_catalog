from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from project_catalog.models import Project

# Create your views here.


#___________________________________________________________________________________________
class ProjectListView(generic.ListView):
    """Generic class-based view for a list of experiments."""
    model = Project
    paginate_by = 10

#___________________________________________________________________________________________
class ProjectDetailView(generic.DetailView):
    """Generic class-based detail view for an experiment."""
    model = Project


@login_required
@permission_required('rawdata_catalog.can_mark_returned', raise_exception=True)
class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'date', 'description']
    #initial = {'date_of_death': '11/06/2020'}
    permission_required = 'rawdata_catalog.can_mark_returned'
