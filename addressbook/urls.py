from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('addressbook.views',
    url(
        r'^$',
        'dashboard',
        name="addressbook_dashboard"
    ),
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
