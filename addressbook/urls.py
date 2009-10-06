from django.conf.urls.defaults import *
from django.conf import settings

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

from addressbook.models import Person, Organization

dashboard_sqs = SearchQuerySet().models(Person, Organization).order_by('name',)

urlpatterns = patterns('haystack.views',
    url(
        r'^$',
        SearchView(
            template="addressbook/dashboard.html",
            searchqueryset=dashboard_sqs,
            form_class=SearchForm
        ),
        name="addressbook_dashboard"
    ),
)

urlpatterns += patterns('',
    (r'^search/', include('haystack.urls')),
)

urlpatterns += patterns('addressbook.views',
    url(
        r'^people/$', 
        'people', 
        name="addressbook_people"
    ),
    url(
        r'^people/(?P<person_id>\d+)/$',
        'person_detail',
        name="addressbook_person_detail"
    ),
    url(
        r'^organizations/$', 
        'organizations',
        name="addressbook_organizations"
    ),
    url(
        r'^organizations/(?P<organization_id>\d+)/$',
        'organization_detail',
        name="addressbook_organization_detail"
    ),
)
