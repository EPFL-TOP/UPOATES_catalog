from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

import datetime, os, json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import io
import urllib, base64

from rawdata_catalog.forms import RenewBookForm, RawDataForm
from rawdata_catalog.models import Person, Affiliation, Contributor, ExperimentalContribution, Experiment, Project,RawDataset

# Create your views here.



#___________________________________________________________________________________________
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
def rawdataset_catalog(request):

    result = RawDataset.objects.values()
    list_result = [entry for entry in result] 
    list_uid=[os.path.join(e["data_type"], e["rcp_name"]) for e in list_result]

    metadata_file=None
    if os.path.exists('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary_2023-08-24_17:39:01.045292_latest.json'):
        metadata_file = open('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary_2023-08-24_17:39:01.045292_latest.json')
    else:
        metadata_file = open('/home/clement/Software/UPOATES_catalog/metadatasummary_2023-08-06_15:59:42.191884_latest.json')
    metadata = json.load(metadata_file)
    data_list = metadata['data']
    n_newdatasets=0
    n_newfiles=0
    n_newsize=0

    n_totdatasets=0
    n_totfiles=0
    n_totsize=0
    for data in data_list:
        for key, value in data.items():
            #CLEMENT SPECIFIC TO MY MAC
            newkey=key.replace("/Volumes/upoates-raw/raw_data/","")
            print(newkey)
            if newkey in list_uid:
                print('found key ',key)
                n_totdatasets+=1
                n_totfiles+=len(value["data"]["raw_files"])
                for f in value["data"]["raw_files"]:
                    n_totsize+=int(f["size"])
            else:
                n_files=len(value["data"]["raw_files"])
                tot_size=0
                for f in value["data"]["raw_files"]:
                    tot_size+=int(f["size"])
                test = RawDataset(data_type=os.path.split(newkey)[0], rcp_name=os.path.split(newkey)[-1], data_status="available",
                                  number_of_files=n_files, total_size=tot_size,files_data={'files':value["data"]["raw_files"]},
                                  date_added=datetime.datetime.now())
                test.save()
                n_newdatasets+=1
                n_newfiles+=n_files
                n_newsize+=tot_size
    datasetsummary={'n_newdatasets':n_newdatasets, 'n_newfiles':n_newfiles, 'n_newsize':n_newsize/10**9, 
                     'n_totdatasets':n_totdatasets, 'n_totfiles':n_totfiles, 'n_totsize':n_totsize/10**12}
    model_data = RawDataset.objects.all()

    model_values = RawDataset.objects.values()
    model_list = [entry for entry in model_values] 
    date_added=[]
    nfiles_added=[]
    ndatasets_added=[]
    size_added=[]

    for e in model_list:
        if e["date_added"] in date_added:
            #continue
            #print(index(e["date_added"])
            nfiles_added[date_added.index(e["date_added"])]+=int(e["number_of_files"])
            size_added[date_added.index(e["date_added"])]+=int(e["total_size"])/10**12
            ndatasets_added[date_added.index(e["date_added"])]+=1
        else:
            date_added.append(e["date_added"])
            nfiles_added.append(int(e["number_of_files"]))
            size_added.append(int(e["total_size"])/10**12)
            ndatasets_added.append(1)

    nfiles_added=[x for _, x in sorted(zip(date_added, nfiles_added))]
    size_added=[x for _, x in sorted(zip(date_added, size_added))]
    ndatasets_added=[x for _, x in sorted(zip(date_added, ndatasets_added))]
    date_added=sorted(date_added)
    print(date_added)
    print(nfiles_added)
    print(size_added)
    print(ndatasets_added)

    nfilestot_added=[0 for x in range(len(date_added))]
    ndatasetstot_added=[0 for x in range(len(date_added))]
    sizetot_added=[0 for x in range(len(date_added))]

    for x in range(len(date_added)):
        if x==0:
            nfilestot_added[x]=nfiles_added[x]
            ndatasetstot_added[x]=ndatasets_added[x]
            sizetot_added[x]=size_added[x]
        else:
            nfilestot_added[x]=nfilestot_added[x-1]+nfiles_added[x]
            ndatasetstot_added[x]=ndatasetstot_added[x-1]+ndatasets_added[x]
            sizetot_added[x]=sizetot_added[x-1]+size_added[x]

    print(nfilestot_added)
    print(sizetot_added)
    print(ndatasetstot_added)

    rawdata_dict={}
    for e in model_list:
        try:
            t=rawdata_dict[e["data_type"]]
        except KeyError:
            rawdata_dict[e["data_type"]]={'tot_size':0, 'tot_files':0, 'n_datasets':0, 'datasets':[]}


    for e in model_list:
        rawdata_dict[e["data_type"]]['datasets'].append(e)
        rawdata_dict[e["data_type"]]['datasets'][-1]['total_size']=int(rawdata_dict[e["data_type"]]['datasets'][-1]['total_size'])/10**9
        rawdata_dict[e["data_type"]]['tot_size']=rawdata_dict[e["data_type"]]['tot_size']+e["total_size"]/10**3
        rawdata_dict[e["data_type"]]['tot_files']=rawdata_dict[e["data_type"]]['tot_files']+int(e["number_of_files"])
        rawdata_dict[e["data_type"]]['n_datasets']=rawdata_dict[e["data_type"]]['n_datasets']+1
    for e in model_list:
        newlist = sorted(rawdata_dict[e["data_type"]]['datasets'], key=lambda d: d['rcp_name'])
        rawdata_dict[e["data_type"]]['datasets']=newlist
    


    fig, ax = plt.subplots()

    fig.subplots_adjust(right=0.75)

    twin1 = ax.twinx()
    twin2 = ax.twinx()

    twin2.spines.right.set_position(("axes", 1.05))

    p1, = ax.plot(date_added, size_added, "C0",  marker='.', label="size")
    p2, = twin1.plot(date_added, nfiles_added, "C0",  marker='.', label="n files")
    p3, = twin2.plot(date_added, ndatasets_added, "C0",  marker='.', label="n datasets")

    ax.set(ylim=(min(size_added), max(size_added)), xlabel="Date", ylabel="Size (TB)")
    twin1.set(ylim=(min(nfiles_added), max(nfiles_added)), ylabel="Number of files")
    twin2.set(ylim=(min(ndatasets_added), max(ndatasets_added)), ylabel="Number of datasets")

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())

    ax.tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())
    twin2.tick_params(axis='y', colors=p3.get_color())
    #ax.legend(handles=[p1, p2, p3])


    fig.tight_layout()
    fig = plt.gcf()
    plt.rcParams['figure.figsize'] = [15, 4]
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)


    
    fig, ax = plt.subplots()

    fig.subplots_adjust(right=0.75)

    twin1 = ax.twinx()
    twin2 = ax.twinx()

    twin2.spines.right.set_position(("axes", 1.05))

    p1, = ax.plot(date_added, sizetot_added, "C0",  marker='.', label="size")
    p2, = twin1.plot(date_added, nfilestot_added, "C0",  marker='.', label="n files")
    p3, = twin2.plot(date_added, ndatasetstot_added, "C0",  marker='.', label="n datasets")

    ax.set(ylim=(min(sizetot_added), max(sizetot_added)), xlabel="Date", ylabel="Size (TB)")
    twin1.set(ylim=(min(nfilestot_added), max(nfilestot_added)), ylabel="Number of files")
    twin2.set(ylim=(min(ndatasetstot_added), max(ndatasetstot_added)), ylabel="Number of datasets")

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())

    ax.tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())
    twin2.tick_params(axis='y', colors=p3.get_color())
    #ax.legend(handles=[p1, p2, p3])

    fig.tight_layout()
    fig = plt.gcf()
    plt.rcParams['figure.figsize'] = [15, 4]
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)


    context={'datasetsummary':datasetsummary, 'rawdata_dict':rawdata_dict, 'model_data':model_data, 'plot':uri, 'plottot':uri2}
    return render(request, "rawdata_catalog/rawdata.html", context)#, {"form": form})



 # data_type           = models.CharField(max_length=100, choices=DATA_TYPE, help_text='Type of data for this dataset (reflecting the the RCP storage categories)')
 #   rcp_name            = models.CharField(max_length=100, choices=sorted(RCP_NAME), help_text="Name of the experimental dataset folder on the RCP storage.")
 #   experiment          = models.ForeignKey('Experiment', on_delete=models.SET_DEFAULT, help_text="Select experimental datasets for this experiment", default='', null=True)
 #   experimental_sample = models.ManyToManyField(ExperimentalSample, help_text="Select experimental samples for this experimental dataset", default='', null=True)
 ##   data_status         = models.CharField(blank=True, max_length=100, choices=DATA_STATUS, default='', help_text='Status of the data on the RCP storage')
  #  compression         = models.CharField(blank=True, max_length=100, choices=COMPRESSION_TYPE, default='', help_text='Type of compression if any')
  #  file_format         = models.CharField(blank=True, max_length=100, choices=FILE_FORMAT, default='', help_text='Format of the files')

   # number_of_files = models.CharField(blank=True, max_length=10, help_text='Number of files for this dataset. FILLED AUTOMATICALLY', default='')
    #total_size      = models.CharField(blank=True, max_length=100, help_text='Total size for this dataset. FILLED AUTOMATICALLY', default='')


    # if this is a POST request we need to process the form data
    #if request.method == "POST":
        # create a form instance and populate it with data from the request:
    #    form = RawDataForm(request.POST)
        # check whether it's valid:
        #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        #    return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    #else:
    #    form = RawDataForm()





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

#___________________________________________________________________________________________
class RawdatasetDetailView(generic.DetailView):
    """Generic class-based detail view for an affiliation."""
    model = RawDataset

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
#    template_name = 'rawdata_catalog/bookinstance_list_borrowed_user.html'
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
#    permission_required = 'rawdata_catalog.can_mark_returned'
#    template_name = 'rawdata_catalog/bookinstance_list_borrowed_all.html'
#    paginate_by = 10

#    def get_queryset(self):
#        return BookInstance.objects.filter(status__exact='o').order_by('due_back')




#@login_required
#@permission_required('rawdata_catalog.can_mark_returned', raise_exception=True)
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
#    return render(request, 'rawdata_catalog/book_renew_librarian.html', context)

@login_required
@permission_required('rawdata_catalog.can_mark_returned', raise_exception=True)
class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'date', 'description']
    #initial = {'date_of_death': '11/06/2020'}
    permission_required = 'rawdata_catalog.can_mark_returned'


#class AuthorCreate(PermissionRequiredMixin, CreateView):
#    model = Author
#    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#    initial = {'date_of_death': '11/06/2020'}
#    permission_required = 'rawdata_catalog.can_mark_returned'


#class AuthorUpdate(PermissionRequiredMixin, UpdateView):
#    model = Author
#    fields = '__all__' # Not recommended (potential security issue if more fields added)
#    permission_required = 'rawdata_catalog.can_mark_returned'


#class AuthorDelete(PermissionRequiredMixin, DeleteView):
#    model = Author
#    success_url = reverse_lazy('authors')
#    permission_required = 'rawdata_catalog.can_mark_returned'


# Classes created for the forms challenge
#class BookCreate(PermissionRequiredMixin, CreateView):
#    model = Book
#    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
#    permission_required = 'rawdata_catalog.can_mark_returned'


#class BookUpdate(PermissionRequiredMixin, UpdateView):
#    model = Book
#    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
#    permission_required = 'rawdata_catalog.can_mark_returned'


#class BookDelete(PermissionRequiredMixin, DeleteView):
#    model = Book
#    success_url = reverse_lazy('books')
#    permission_required = 'rawdata_catalog.can_mark_returned'
