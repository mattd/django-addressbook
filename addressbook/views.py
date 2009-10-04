from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from addressbook.models import Person, Organization

@login_required
def people(request):
    return object_list(request, template_name="addressbook/people.html",
                       queryset=Person.objects.all())


@login_required
def person_detail(request, person_id):
    return object_detail(request, queryset=Person.objects.all(),
                         object_id=person_id)


@login_required
def organizations(request):
    return object_list(request, template_name="addressbook/organizations.html",
                       queryset=Organization.objects.all())


@login_required
def organization_detail(request, organization_id):
    return object_detail(request, queryset=Organization.objects.all(),
                         object_id=organization_id)
