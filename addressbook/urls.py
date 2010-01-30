from django.conf.urls.defaults import *
from django.conf import settings

from addressbook.models import Organization, Person
from addressbook.forms import OrganizationForm, PersonForm

urlpatterns = patterns('addressbook.views',
    url(
        r'^$',
        'party_list',
        {'template': 'addressbook/dashboard.html',},
        name="addressbook_dashboard"
    ),

    # People URLs
    url(
        r'^people/$', 
        'party_list',
        {'template': 'addressbook/people.html',},
        name="addressbook_people"
    ),
    url(
        r'^people/add/$',
        'add_party',
        {
            'form': PersonForm,
            'template': 'addressbook/person_add.html',
        },
        name="addressbook_person_add"
    ),
    url(
        r'^people/(?P<object_id>\d+)/$',
        'person_detail',
        name="addressbook_person_detail"
    ),
    url(
        r'^people/(?P<object_id>\d+)/edit/$',
        'edit_party',
        {
            'model': Person,
            'form': PersonForm,
            'template': 'addressbook/person_edit.html',
        },
        name="addressbook_person_edit"
    ),

    # Organization URLs
    url(
        r'^organizations/$', 
        'party_list', 
        {'template': 'addressbook/organizations.html',},
        name="addressbook_organizations"
    ),
    url(
        r'^organizations/add/$',
        'add_party',
        {
            'form': OrganizationForm,
            'template': 'addressbook/organization_add.html',
        },
        name="addressbook_organization_add"
    ),
    url(
        r'^organizations/(?P<object_id>\d+)/$',
        'organization_detail',
        name="addressbook_organization_detail"
    ),
    url(
        r'^organizations/(?P<object_id>\d+)/edit/$',
        'edit_party',
        {
            'model': Organization,
            'form': OrganizationForm,
            'template': 'addressbook/organization_edit.html',
        },
        name="addressbook_organization_edit"
    ),
    url(
        r'^autocomplete-organization/$',
        'autocomplete_organization',
        name="addressbook_organization_autocomplete"
    ),
)
