from django.conf.urls.defaults import *
from django.conf import settings

from haystack.query import SearchQuerySet

from addressbook.models import Organization, Person
from addressbook.forms import OrganizationForm, PersonForm

urlpatterns = patterns('addressbook.views',
    url(
        r'^$',
        'party_list',
        {
            'searchqueryset': SearchQuerySet().models(Organization, Person).order_by('sort_name'),
            'template': 'addressbook/dashboard.html',
        },
        name="addressbook_dashboard"
    ),
    url(
        r'^people/$', 
        'party_list',
        {
            'searchqueryset': SearchQuerySet().models(Person).order_by('sort_name'),
            'template': 'addressbook/people.html',
        },
        name="addressbook_people"
    ),
    url(
        r'^organizations/$', 
        'party_list', 
        {
            'searchqueryset': SearchQuerySet().models(Organization).order_by('sort_name'),
            'template': 'addressbook/organizations.html',
        },
        name="addressbook_organizations"
    ),
    url(
        r'^people/(?P<person_id>\d+)/$',
        'person_detail',
        name="addressbook_person_detail"
    ),
    url(
        r'^people/add/$',
        'party_add',
        {
            'form': PersonForm,
            'template': 'addressbook/person_add.html',
        },
        name="addressbook_person_add"
    ),
    url(
        r'^organizations/(?P<organization_id>\d+)/$',
        'organization_detail',
        name="addressbook_organization_detail"
    ),
    url(
        r'^organizations/add/$',
        'party_add',
        {
            'form': OrganizationForm,
            'template': 'addressbook/organization_add.html',
        },
        name="addressbook_organization_add"
    ),
)
