from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from addressbook.models import Contact, Organization

@login_required
def contact_list(request):
    return object_list(request, queryset=Contact.objects.all())


@login_required
def contact_detail(request, contact_id):
    return object_detail(request, queryset=Contact.objects.all(),
                         object_id=contact_id)


@login_required
def organization_list(request):
    return object_list(request, queryset=Organization.objects.all())


@login_required
def organization_detail(request, organization_id):
    return object_detail(request, queryset=Organization.objects.all(),
                         object_id=organization_id)
