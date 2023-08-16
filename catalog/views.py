from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

import datetime

from catalog.forms import RenewBookForm

from .models import Person, Affiliation, Contributor, ExperimentalContribution, Experiment, Project

# Create your views here.



def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_persons       = Person.objects.all().count()
    num_affiliations  = Affiliation.objects.all().count()
    num_contributors  = Contributor.objects.all().count()
    num_contributions = ExperimentalContribution.objects.all().count()
    num_projects      = Project.objects.all().count()
    num_experiments   = Experiment.objects.all().count()
    #print('-->1  ',Experiment.objects.values_list())
    #print('-->2  ',Experiment.objects.all())
    #print('-->3  ',Experiment.objects.values())
    #print('-->4  ',Experiment.objects.get(project_name__isnull=False))
   
    # Available copies of books
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_persons':num_persons, 
                 'num_affiliations':num_affiliations,
                 'num_contributors':num_contributors,
                 'num_contributions':num_contributions,
                 'num_projects':num_projects,
                 'num_experiments':num_experiments,

                 'num_visits': num_visits},
    )

#___________________________________________________________________________________________
class ProjectListView(generic.ListView):
    """Generic class-based view for a list of experiments."""
    model = Project
    paginate_by = 10

#___________________________________________________________________________________________
class ProjectDetailView(generic.DetailView):
    """Generic class-based detail view for an experiment."""
    model = Project

#___________________________________________________________________________________________
class ExperimentListView(generic.ListView):
    """Generic class-based view for a list of experiments."""
    model = Experiment
    paginate_by = 10

#___________________________________________________________________________________________
class ExperimentDetailView(generic.DetailView):
    """Generic class-based detail view for an experiment."""
    model = Experiment

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
class ExperimentalContributionListView(generic.ListView):
    """Generic class-based view for a list of contributions."""
    model = ExperimentalContribution
    paginate_by = 10

#___________________________________________________________________________________________
class ExperimentalContributionDetailView(generic.DetailView):
    """Generic class-based detail view for a contribution."""
    model = ExperimentalContribution

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



#class BookListView(generic.ListView):
#    """Generic class-based view for a list of books."""
#    model = Book
#    paginate_by = 10


#class BookDetailView(generic.DetailView):
#    """Generic class-based detail view for a book."""
#    model = Book


#class AuthorListView(generic.ListView):
#    """Generic class-based list view for a list of authors."""
#    model = Author
#    paginate_by = 10


#class AuthorDetailView(generic.DetailView):
#    """Generic class-based detail view for an author."""
#    model = Author




#class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
#    """Generic class-based view listing books on loan to current user."""
#    model = BookInstance
#    template_name = 'catalog/bookinstance_list_borrowed_user.html'
#    paginate_by = 10

#    def get_queryset(self):
#        return (
#            BookInstance.objects.filter(borrower=self.request.user)
#            .filter(status__exact='o')
#            .order_by('due_back')
#        )




#class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
#    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
#    model = BookInstance
#    permission_required = 'catalog.can_mark_returned'
#    template_name = 'catalog/bookinstance_list_borrowed_all.html'
#    paginate_by = 10

#    def get_queryset(self):
#        return BookInstance.objects.filter(status__exact='o').order_by('due_back')




#@login_required
#@permission_required('catalog.can_mark_returned', raise_exception=True)
#def renew_book_librarian(request, pk):
#    """View function for renewing a specific BookInstance by librarian."""
#    book_instance = get_object_or_404(BookInstance, pk=pk)
#
#    # If this is a POST request then process the Form data
#    if request.method == 'POST':
#
#        # Create a form instance and populate it with data from the request (binding):
#        form = RenewBookForm(request.POST)
#
#        # Check if the form is valid:
#        if form.is_valid():
#            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#            book_instance.due_back = form.cleaned_data['renewal_date']
#            book_instance.save()
#
#            # redirect to a new URL:
#            return HttpResponseRedirect(reverse('all-borrowed'))
#
#    # If this is a GET (or any other method) create the default form
#    else:
#        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
#
#    context = {
#        'form': form,
#        'book_instance': book_instance,
#    }
#
#    return render(request, 'catalog/book_renew_librarian.html', context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'date', 'description']
    #initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


#class AuthorCreate(PermissionRequiredMixin, CreateView):
#    model = Author
#    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#    initial = {'date_of_death': '11/06/2020'}
#    permission_required = 'catalog.can_mark_returned'


#class AuthorUpdate(PermissionRequiredMixin, UpdateView):
#    model = Author
#    fields = '__all__' # Not recommended (potential security issue if more fields added)
#    permission_required = 'catalog.can_mark_returned'


#class AuthorDelete(PermissionRequiredMixin, DeleteView):
#    model = Author
#    success_url = reverse_lazy('authors')
#    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
#class BookCreate(PermissionRequiredMixin, CreateView):
#    model = Book
#    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
#    permission_required = 'catalog.can_mark_returned'


#class BookUpdate(PermissionRequiredMixin, UpdateView):
#    model = Book
#    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
#    permission_required = 'catalog.can_mark_returned'


#class BookDelete(PermissionRequiredMixin, DeleteView):
#    model = Book
#    success_url = reverse_lazy('books')
#    permission_required = 'catalog.can_mark_returned'
