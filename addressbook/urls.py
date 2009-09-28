from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('addressbook.views',
    url(
        r'^contacts/$', 
        'contact_list', 
        name="addressbook_contact_list"
    ),
    url(
        r'^contacts/(?P<contact_id>\d+)/$',
        'contact_detail',
        name="addressbook_contact_detail"
    ),
    url(
        r'^organizations/$', 
        'organization_list',
        name="addressbook_organization_list"
    ),
    url(
        r'^organizations/(?P<organization_id>\d+)/$',
        'organization_detail',
        name="addressbook_organization_detail"
    ),
)
