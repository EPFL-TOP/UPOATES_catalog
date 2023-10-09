from . import views
from django.urls import path


urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
]


