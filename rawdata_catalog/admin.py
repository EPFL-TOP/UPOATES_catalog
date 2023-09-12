from django.contrib import admin
from django import forms

# Register your models here.


from .models import RawDataset

admin.site.register(RawDataset)


#@admin.register(Entry)
#class EntryAdmin(admin.ModelAdmin):
#    autocomplete_fields = ['blog']
#    search_fields = ['headline']
#    def get_search_results(self, request, queryset, search_term):
#        print("In get search results ")#,search_term)
#        print("=============== ", Entry.objects.all())
#        results = super().get_search_results(request, queryset, search_term)
#        return results


#import json
#class ExperimentalDatasetAdminForm(forms.ModelForm):
#    ''' collecting subcategories and corvert it to json. for use in javascript code '''
#    data = {}
#    for exp in ExperimentalDataset.objects.all():
#        data[str(exp.id)]={}
#    for sub in ExperimentalDataset.objects.all():
#        data[str(sub.id)] = {
#                'id': str(sub.id)
#                
#                #'cat_id': str(sub.category.id),
#                #'name': str(sub.name)
#        }
#    data = json.dumps(data)
#    ''' converted to json '''
#    print('json data-----------------------  ',data)
#
#    rcp_name = forms.ModelChoiceField(queryset=ExperimentalDataset.objects.all(), 
#    widget=forms.Select(attrs={'onchange':  'category = this.options[this.selectedIndex].value; var data = ' + data + ';(function(){ var select = document.getElementById("id_subcategory");  select.options.length=0; select.options[select.options.length] = new Option("----",""); for(let [key, value] of Object.entries(data[category.toString()])) { select.options[select.options.length] = new Option(value.ady,value.id); } })()'}));
#    class Meta:
#        model = ExperimentalDataset
#        fields='__all__'


#class ExperimentalDatasetAdmin(admin.ModelAdmin):
#    fields = 'data_type','rcp_name',
#    autocomplete_fields = 'rcp_name',
#    #form = ExperimentalDatasetAdminForm
#    # class Media:
#    #     js = ('own.js',)

##admin.site.register(ExperimentalDataset, ExperimentalDatasetAdmin)


#class BooksInline(admin.TabularInline):
#    """Defines format of inline book insertion (used in AuthorAdmin)"""
#    model = Book


#@admin.register(Author)
#class AuthorAdmin(admin.ModelAdmin):
#    """Administration object for Author models.
#    Defines:
#     - fields to be displayed in list view (list_display)
#     - orders fields in detail view (fields),
#       grouping the date fields horizontally
#     - adds inline addition of books in author view (inlines)
#    """
#    list_display = ('last_name',
#                    'first_name', 'date_of_birth', 'date_of_death')
#    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
#    inlines = [BooksInline]


#class BooksInstanceInline(admin.TabularInline):
#    """Defines format of inline book instance insertion (used in BookAdmin)"""
#    model = BookInstance


#class BookAdmin(admin.ModelAdmin):
#    """Administration object for Book models.
#    Defines:
#     - fields to be displayed in list view (list_display)
#     - adds inline addition of book instances in book view (inlines)
#    """
#    list_display = ('title', 'author', 'display_genre')
#    inlines = [BooksInstanceInline]


#admin.site.register(Book, BookAdmin)


##@admin.register(BookInstance)
#class BookInstanceAdmin(admin.ModelAdmin):
#    """Administration object for BookInstance models.
#    Defines:
#     - fields to be displayed in list view (list_display)
#     - filters that will be displayed in sidebar (list_filter)
#     - grouping of fields into sections (fieldsets)
#    """
#    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
#    list_filter = ('status', 'due_back')

#    fieldsets = (
#        (None, {
#            'fields': ('book', 'imprint', 'id')
#        }),
#        ('Availability', {
#            'fields': ('status', 'due_back', 'borrower')
#        }),
#    )
