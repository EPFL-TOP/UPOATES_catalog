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
from experimentalcondition_catalog.models import ExperimentalCondition, MutationName, MutationGrade, Parent, Sample

import requests
from requests.auth import HTTPBasicAuth

import accesskeys as accessk

# Create your views here.
DEBUG=False
#___________________________________________________________________________________________
def add_mutations(): 
    mutation_name = [
    "None",
    "Cdh1-YFP",
    "Cdh1-tdTomato",
    "DCX-GFP",
    "Dlc",
    "Dlc-mKate2",
    "Dlc-mNeongreen",
    "Dover",
    "GTIIC:eGFP",
    "GTIIC:mCherry",
    "H2A-GFP",
    "H2B-Cherry",
    "H2B-HaloTag",
    "Heidi-Blue",
    "Her7 Stop",
    "Hoff-mAID",
    "Ism1",
    "MCP-10AA-NG",
    "MCP-1AA-GFP",
    "MCP-1AA-NG",
    "Nacre",
    "Ntla D5",
    "Ntla:DrmKate2",
    "Ntla:DrmNeongreen",
    "Ripply1",
    "Ripply2",
    "Sox10:nRFP-Kalt4ER",
    "Ta52b",
    "Tbx16",
    "Tbx6-mKate2",
    "Tbx6:mNeonGreen",
    "Tbx6:venus",
    "Transparent",
    "Utr-Cherry",
    "Utr-GFP",
    "cdh2",
    "cdh2-GFP",
    "cdh2-sfGFP-TagRFP",
    "dUAS:dnSu(H)-GFP",
    "dUAS:dnSu(H)-mScarlet",
    "dld",
    "dmd:citrine-mcherry",
    "drl:cre-ert2,cryaa:venus",
    "fgfr1-dn-cargo",
    "fused somites(fss)/tbx6 -/-",
    "glo",
    "gullum",
    "hannibal",
    "heidi",
    "her1",
    "her1-MS2",
    "hes6",
    "hoff",
    "lector",
    "looping",
    "m119",
    "notch1a",
    "ntla D8",
    "ntlb D8",
    "phOTO-Bow",
    "phOTO-M",
    "smyhc1:EGFP",
    "βActin-Myl-EGFP",
    "βActin-Myl-mCherry"
]

    mutation_grade = [
    "N/A",
    "F0",
    "Founder",
    "Het",
    "Het/Homo",
    "Homo",
    "Unkown",
    "WT",
    "WT/Het",
    "WT/Het/Homo"
]

    mutations = MutationName.objects.values()
    list_mutations = [entry for entry in mutations] 
    list_mutations_uid=[e["name"] for e in list_mutations]

    for name in mutation_name:
        if name in list_mutations_uid: continue
        mutation =  MutationName(name=name)
        mutation.save()
        list_mutations_uid.append(name)
        print('adding mutation ',name)
    
    grades = MutationGrade.objects.values()
    list_grades = [entry for entry in grades] 
    list_grades_uid=[e["grade"] for e in list_grades]

    for grade in mutation_grade:
        if grade in list_grades_uid: continue
        mutation_grade =  MutationGrade(grade=grade)
        mutation_grade.save()
        list_grades_uid.append(grade)
        print('adding mutation grade ',grade)

#___________________________________________________________________________________________
def fill_parents():
    
    username = accessk.PYRAT_username
    password = accessk.PYRAT_password
    auth = HTTPBasicAuth(username, password)
    base_url = 'https://sv-pyrat-aquatic-test.epfl.ch/pyrat-aquatic-test/api/v3/'
    api_url_tanks     = base_url +'tanks'
    api_url_crossings = base_url + 'tanks/crossings'
    api_url_strains   = base_url + 'strains'
    
    sample = Sample.objects.values()
    list_pyrat = [entry for entry in sample] 
    list_pyrat_uid = [e["pyrat_crossing_id"] for e in list_pyrat]

    parents = Parent.objects.values()
    list_parent_pyrat = [entry for entry in parents] 
    list_parent_pyrat_uid = [e["pyrat_crossing_id"] for e in list_parent_pyrat]

    if DEBUG: print('---------------------------pyrat uid ',list_pyrat_uid)
    if DEBUG: print('---------------------------pyrat parent uid ',list_parent_pyrat_uid)
    for xid in list_pyrat_uid:


        if DEBUG: print('========------------------==================, ',xid)
        if xid in list_parent_pyrat_uid: continue

        query = {'tk':['strain_id', 'strain_name', 'strain_name_id','strain_name_with_id','mutations','date_of_birth'],'crossing_id':'{}'.format(str(xid))}
        if DEBUG: print(query)
        response = requests.get(api_url_crossings, auth=auth, params=query )
        if DEBUG: print(response)
        response_json = response.json()
        if DEBUG: print(response_json)

        sample_with_date = Sample.objects.get(pyrat_crossing_id=xid)
        if sample_with_date.date_of_crossing == '' or sample_with_date.date_of_crossing == None:
            sample_with_date.date_of_crossing = response_json[0]['date_of_record']
            sample_with_date.save()

        for p in response_json[0]['tanks']['parents']:
  
            d1 = datetime.datetime.strptime(response_json[0]['date_of_record'], "%Y-%m-%d")
            d2 = datetime.datetime.strptime(p["date_of_birth"], "%Y-%m-%d")
            if DEBUG: print('[rewewwerwerwerfwdfegjfhgjuafhgjdafjdk;zjkdjaf;jeakfjEKAfjkeAJf;ieAJfejwfkjZI]      ',d2-d1)
            delta = d1 - d2
            
            mutation = ''
            if DEBUG: print('mutation         ----------------------  ',p["mutations"])
            for m in p["mutations"]:
                if mutation!='':mutation+=", "
                mutation+="("+m["mutation_name"]+","+m["mutation_grade_name"]+")"
            if DEBUG: print('mutations        ',mutation)
            parent = Parent(number_of_male=str(p["number_of_male"]),
                            number_of_female=p["number_of_female"],
                            number_of_unknown=p["number_of_unknown"],
                            date_of_birth=p["date_of_birth"],
                            strain_name=p["strain_name"],
                            age_at_crossing=delta.days,
                            pyrat_crossing_id=xid,
                            mutation_grade=mutation)

            parent.save()
            sample_with_date.parent.add(parent)
            sample_with_date.save()

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

    if DEBUG: print('The visualisation request method is:', request.method)
    if DEBUG: print('The visualisation POST data is:     ', request.POST)

    #TO BE DONE ONCE AT THE BEGINING
    if 'reload_pyrat' in request.POST:
        fill_parents()
    if 'reload_mutation' in request.POST:
        add_mutations()
    result = RawDataset.objects.values()
    if DEBUG: print(RawDataset.objects)
    if DEBUG: print('-------------------------------------------',result)
    list_result = [entry for entry in result] 
    list_uid=[os.path.join(e["data_type"], e["data_name"]) for e in list_result]

    metadata_file=None
    if os.path.exists('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary.json'):
        metadata_file = open('/Users/helsens/Software/github/EPFL-TOP/UPOATES_catalog/metadatasummary.json')
    elif os.path.isdir('/mnt/nas_rcp/raw_data/metadata/'):
        import glob
        latestfile=glob.glob('/mnt/nas_rcp/raw_data/metadata/*_latest.json')
        if len(latestfile)!=1:
            print('should not have more than 1 latest file')
            print(latestfile)
        metadata_file = open(latestfile[0])
    else:
        print('not local and rcp not mounted, please do something')
    metadata = json.load(metadata_file)
    data_list = metadata['data']
    n_newdatasets=0
    n_newfiles=0
    n_newsize=0

    n_totdatasets=0
    n_totfiles_raw=0
    n_totsize_raw=0
    n_totfiles_other=0
    n_totsize_other=0

    for data in data_list:
        for key, value in data.items():
            #CLEMENT SPECIFIC TO MY MAC
            newkey=key.replace("/Volumes/upoates/Common/raw_data/","")
            if newkey in list_uid:
                n_totdatasets+=1
                n_totfiles_raw+=len(value["data"]["raw_files"])
                n_totfiles_other+=len(value["data"]["other_files"])
                for f in value["data"]["raw_files"]:
                    n_totsize_raw+=int(f["size"])
                for f in value["data"]["other_files"]:
                    n_totsize_other+=int(f["size"])
            
                for r in list_result:
                    if newkey != os.path.join(r["data_type"], r["data_name"]): continue
                    if len(value["data"]["raw_files"])!=len(r["raw_files"]["files"]):
                        nrds = RawDataset.objects.get(id=r["id"])
                        nrds.raw_files={'files':value["data"]["raw_files"]}
                        nrds.number_of_raw_files=len(value["data"]["raw_files"])
                        tot_size_raw=0
                        for f in value["data"]["raw_files"]:
                            tot_size_raw+=int(f["size"])
                        nrds.total_raw_size=tot_size_raw
                        nrds.save()
                    
                    #TEMPORARY
                    if r["other_files"]==None or r["other_files"]==[]:
                        nrds = RawDataset.objects.get(id=r["id"])
                        nrds.other_files={'files':[]}
                        nrds.save()
                    if r["total_other_size"]=='':
                        nrds = RawDataset.objects.get(id=r["id"])
                        nrds.total_other_size=0
                        nrds.number_of_other_files=0
                        nrds.save()
                    #ENDTEMP
                    print('---------------------------------------------------------newkey  ',newkey)
                    print(len(value["data"]["other_files"]),'===========================',len(r["other_files"]["files"]))
                    if len(value["data"]["other_files"])!=len(r["other_files"]["files"]):
                        nrds = RawDataset.objects.get(id=r["id"])
                        nrds.other_files={'files':value["data"]["other_files"]}
                        nrds.number_of_other_files=len(value["data"]["other_files"])
                        tot_size_other=0
                        for f in value["data"]["other_files"]:
                            tot_size_other+=int(f["size"])
                        nrds.total_other_size=tot_size_other
                        nrds.save()

            else:
                n_files_raw=len(value["data"]["raw_files"])
                n_files_other=len(value["data"]["other_files"])
                tot_size_raw=0
                tot_size_other=0
                for f in value["data"]["raw_files"]:
                    tot_size_raw+=int(f["size"])
                for f in value["data"]["other_files"]:
                    tot_size_other+=int(f["size"])
                    
                rawds = RawDataset(data_type=os.path.split(newkey)[0], data_name=os.path.split(newkey)[-1], data_status="available",
                                  number_of_raw_files=n_files_raw, total_raw_size=tot_size_raw, raw_files={'files':value["data"]["raw_files"]}, 
                                  number_of_other_files=n_files_other, total_other_size=tot_size_other, other_files={'files':value["data"]["other_files"]},
                                  date_added=value["date"])
                rawds.save()

                expcond = ExperimentalCondition()
                if DEBUG: print(expcond)
                expcond.save()
                expds = ExperimentalDataset(raw_dataset=rawds, experimental_condition=expcond)
                expds.save()


                n_newdatasets+=1
                n_newfiles+=n_files_raw
                n_newsize+=tot_size_raw
    datasetsummary={'n_newdatasets':n_newdatasets, 'n_newfiles':n_newfiles, 'n_newsize':n_newsize/10**9, 
                     'n_totdatasets':n_totdatasets, 'n_totfiles':n_totfiles_raw, 'n_totsize':n_totsize_raw/10**12}

    search_dict = {
        'specie':[],
        'developmental_stage':[],
        'mutation':[],
        'grade':[],
        'instrument_type':[],
        'instrument_name':[],
        }
    
    mydata = ExperimentalCondition.objects.all()



    for d in mydata:
        for a in d.sample.all():
            if a.specie not in search_dict['specie']:
                search_dict['specie'].append(a.specie)
            if a.developmental_stage not in search_dict['developmental_stage']:
                search_dict['developmental_stage'].append(a.developmental_stage)
            for m in a.mutation.all():
                if m.name.name not in search_dict['mutation']:
                    search_dict['mutation'].append(m.name.name)
                if m.grade.grade not in search_dict['grade']:
                    search_dict['grade'].append(m.grade.grade)
        for a in d.instrumental_condition.all():
            if DEBUG: print('a-------------- ',a)
            if a.instrument_type not in search_dict["instrument_type"]:
                search_dict["instrument_type"].append(a.instrument_type)
            if a.instrument_name not in search_dict["instrument_name"]:
                search_dict["instrument_name"].append(a.instrument_name)

    if DEBUG: print('------------------------------------------------  search dict  ',search_dict)
    model_data = RawDataset.objects.all()

    if request.method=="POST":
        search_specie=request.POST.get('search_specie')
        if search_specie != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__sample__specie=search_specie)

        search_devstage=request.POST.get('search_devstage')
        if search_devstage != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__sample__developmental_stage=search_devstage)

        search_mutation=request.POST.get('search_mutation')
        if search_mutation != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__sample__mutation__name__name=search_mutation)

        search_grade=request.POST.get('search_grade')
        if search_grade != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__sample__mutation__grade__grade=search_grade)
            model_data=model_data.distinct()

        search_instrument_type=request.POST.get('search_instrument_type')
        if search_instrument_type != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__instrumental_condition__instrument_type=search_instrument_type)

        search_instrument_name=request.POST.get('search_instrument_name')
        if search_instrument_name != None:
            model_data = model_data.filter(experimentaldataset__experimental_condition__instrumental_condition__instrument_name=search_instrument_name)

    #print('=this one===============================',model_data)

    model_values = model_data.values()
    model_list = [entry for entry in model_values] 
    list_uid2=[os.path.join(e["data_type"], e["data_name"]) for e in model_list]

    n_totdatasets_filter=0
    n_totfiles_filter=0
    n_totsize_filter=0
    for data in data_list:
        for key, value in data.items():
            #CLEMENT SPECIFIC TO MY MAC
            newkey=key.replace("/Volumes/upoates/Common/raw_data/","")
            if newkey in list_uid2:
                n_totdatasets_filter+=1
                n_totfiles_filter+=len(value["data"]["raw_files"])
                for f in value["data"]["raw_files"]:
                    n_totsize_filter+=int(f["size"])

    datasetsummary['n_totdatasets_filter']=n_totdatasets_filter
    datasetsummary['n_totfiles_filter']=n_totfiles_filter
    datasetsummary['n_totsize_filter']=n_totsize_filter/10**12
    
    date_added=[]
    nfiles_added=[]
    ndatasets_added=[]
    size_added=[]

    for e in model_list:

        if e["date_added"] in date_added:
            #continue
            nfiles_added[date_added.index(e["date_added"])]+=int(e["number_of_raw_files"])
            size_added[date_added.index(e["date_added"])]+=int(e["total_raw_size"])/10**12
            ndatasets_added[date_added.index(e["date_added"])]+=1
        else:
            date_added.append(e["date_added"])
            nfiles_added.append(int(e["number_of_raw_files"]))
            size_added.append(int(e["total_raw_size"])/10**12)
            ndatasets_added.append(1)

    nfiles_added=[x for _, x in sorted(zip(date_added, nfiles_added))]
    size_added=[x for _, x in sorted(zip(date_added, size_added))]
    ndatasets_added=[x for _, x in sorted(zip(date_added, ndatasets_added))]
    date_added=sorted(date_added)

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

    print('================================',model_data)




    rawdata_dict={}
    for e in model_list:
        try:
            t=rawdata_dict[e["data_type"]]
        except KeyError:
            rawdata_dict[e["data_type"]]={'tot_size':0, 'tot_files':0, 'n_datasets':0, 'datasets':[]}


    for e in model_list:
        rawdata_dict[e["data_type"]]['datasets'].append(e)
        rawdata_dict[e["data_type"]]['datasets'][-1]['total_raw_size']=int(rawdata_dict[e["data_type"]]['datasets'][-1]['total_raw_size'])/10**9
        rawdata_dict[e["data_type"]]['tot_size']=rawdata_dict[e["data_type"]]['tot_size']+e["total_raw_size"]/10**3
        rawdata_dict[e["data_type"]]['tot_files']=rawdata_dict[e["data_type"]]['tot_files']+int(e["number_of_raw_files"])
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

    p1, = ax.plot(date_added, size_added, "C0",  marker='.', label="size", color='tab:red')
    p2, = twin1.plot(date_added, nfiles_added, "C0",  marker='.', label="n files", color='tab:green')
    p3, = twin2.plot(date_added, ndatasets_added, "C0",  marker='.', label="n datasets")

    print(size_added)
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

    p1, = ax.plot(date_added, sizetot_added, "C0",  marker='.', label="size", color='tab:red')
    p2, = twin1.plot(date_added, nfilestot_added, "C0",  marker='.', label="n files", color='tab:green')
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


    context={'datasetsummary':datasetsummary, 'rawdata_dict':rawdata_dict, 'model_data':model_data, 'plot':uri, 'plottot':uri2, 'search_dict':search_dict}
    return render(request, "rawdata_catalog/rawdata.html", context)#, {"form": form})


#___________________________________________________________________________________________
class RawdatasetDetailView(generic.DetailView):
    """Generic class-based detail view for an affiliation."""
    model = RawDataset

