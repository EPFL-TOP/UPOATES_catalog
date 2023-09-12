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

from rawdata_catalog.models import RawDataset
from experiment_catalog.models import ExperimentalDataset
from experimentalcondition_catalog.models import ExperimentalCondition

# Create your views here.

#___________________________________________________________________________________________
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    #num_persons       = Person.objects.all().count()
    #num_affiliations  = Affiliation.objects.all().count()
    #num_contributors  = Contributor.objects.all().count()
    #num_contributions = ExperimentalContribution.objects.all().count()
    #num_projects      = Project.objects.all().count()
    #num_experiments   = Experiment.objects.all().count()
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
        context={#'num_persons':num_persons, 
                 #'num_affiliations':num_affiliations,
                 #'num_contributors':num_contributors,
                 #'num_contributions':num_contributions,
                 #'num_projects':num_projects,
                 #'num_experiments':num_experiments,

                 'num_visits': num_visits},
    )


#___________________________________________________________________________________________
def rawdataset_catalog(request):

    result = RawDataset.objects.values()
    list_result = [entry for entry in result] 
    list_uid=[os.path.join(e["data_type"], e["data_name"]) for e in list_result]

    metadata_file=None
    if os.path.exists('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary_2023-08-24_17:39:01.045292_latest.json'):
        metadata_file = open('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary_2023-08-24_17:39:01.045292_latest.json')
    else:
        metadata_file = open('/home/clement/Software/UPOATES_catalog/metadatasummary_2023-08-24_17:39:01.045292_latest.json')
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
                rawds = RawDataset(data_type=os.path.split(newkey)[0], data_name=os.path.split(newkey)[-1], data_status="available",
                                  number_of_files=n_files, total_size=tot_size,files_data={'files':value["data"]["raw_files"]},
                                  date_added=datetime.datetime.now())
                rawds.save()

                expcond = ExperimentalCondition()
                expcond.save()
                expds = ExperimentalDataset(raw_dataset=rawds, experimental_condition=expcond)
                expds.save()



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


    mydata = ExperimentalCondition.objects.all()
    print(mydata)
    for d in mydata:
        print('-----------------, ',d.animal)
        for a in d.animal.all():
            print('ssssssss  ',a.specie)
    mydata = ExperimentalCondition.objects.filter(animal__specie='zebrafish')
    print('================================',mydata)
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
        newlist = sorted(rawdata_dict[e["data_type"]]['datasets'], key=lambda d: d['data_name'])
        rawdata_dict[e["data_type"]]['datasets']=newlist
    

    plt.rcParams['figure.figsize'] = [12, 3]
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
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)


    context={'datasetsummary':datasetsummary, 'rawdata_dict':rawdata_dict, 'model_data':model_data, 'plot':uri, 'plottot':uri2}
    return render(request, "rawdata_catalog/rawdata.html", context)#, {"form": form})


#___________________________________________________________________________________________
class RawdatasetDetailView(generic.DetailView):
    """Generic class-based detail view for an affiliation."""
    model = RawDataset

