from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rawdatasets/', views.rawdataset_catalog, name='rawdatasets'),
    path('rawdataset/<int:pk>', views.RawdatasetDetailView.as_view(), name='rawdataset-detail'),
]

