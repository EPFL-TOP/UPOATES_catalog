from . import views
from django.urls import path


urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
]


# Add URLConf to create, update, and delete books
urlpatterns += [
#    path('book/create/', views.BookCreate.as_view(), name='book-create'),
#    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
#    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),

    #path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/create/', views.ProjectCreate, name='project-create'),

]
