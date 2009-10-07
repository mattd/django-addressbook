from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from haystack.views import SearchView
from haystack.forms import SearchForm 
from haystack.query import SearchQuerySet

from addressbook.models import Party, Person, Organization


class DashboardSearchView(SearchView):
    def __name__(self):
        return "DashboardSearchView"

    def get_results(self):
        """Fetch results based on the query submitted.

        If no query is present, fetch all Organization and Person objects.
        
        """
        if self.query:
            return self.form.search()

        return SearchQuerySet().models(Person, Organization).order_by('sort_name').load_all()
        

@login_required
def dashboard(request):
    sqs = SearchQuerySet().models(Person, Organization).order_by('sort_name')
    return DashboardSearchView(template="addressbook/dashboard.html", 
                               searchqueryset=sqs,
                               form_class=SearchForm).__call__(request)


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
