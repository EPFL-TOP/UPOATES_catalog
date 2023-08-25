from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('rawdatasets/', views.rawdataset_catalog, name='rawdatasets'),
    path('rawdataset/<int:pk>', views.RawdatasetDetailView.as_view(), name='rawdataset-detail'),
    #path('books/', views.BookListView.as_view(), name='books'),
    #path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    #path('authors/', views.AuthorListView.as_view(), name='authors'),
    #path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    #Added by clement
    path('persons/', views.PersonListView.as_view(), name='persons'),
    path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),

    path('contributors/', views.ContributorListView.as_view(), name='contributors'),
    path('contributor/<int:pk>', views.ContributorDetailView.as_view(), name='contributor-detail'),

    path('experimentalcontributions/', views.ExperimentalContributionListView.as_view(), name='experimentalcontributions'),
    path('experimentalcontribution/<int:pk>', views.ExperimentalContributionDetailView.as_view(), name='experimentalcontribution-detail'),

    path('affiliations/', views.AffiliationListView.as_view(), name='affiliations'),
    path('affiliation/<int:pk>', views.AffiliationDetailView.as_view(), name='affiliation-detail'),

    path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    path('experiment/<int:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),

    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),

]


#urlpatterns += [
#   path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
#   path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
#]


# Add URLConf for librarian to renew a book.
#urlpatterns += [
#    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
#]


# Add URLConf to create, update, and delete authors
#urlpatterns += [
#    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
#    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
#    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
#]

# Add URLConf to create, update, and delete books
urlpatterns += [
#    path('book/create/', views.BookCreate.as_view(), name='book-create'),
#    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
#    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),

    #path('project/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('project/create/', views.ProjectCreate, name='project-create'),

]
