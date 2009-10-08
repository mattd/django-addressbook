from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from haystack.views import SearchView
from haystack.forms import SearchForm 
from haystack.query import SearchQuerySet

from addressbook.models import Party, Person, Organization


@login_required
def dashboard(request):
    form = SearchForm()
    sqs = SearchQuerySet().models(Person, Organization).order_by('sort_name')

    if request.GET.get('q'):
        form = SearchForm(request.GET, searchqueryset=sqs)

        if form.is_valid():
            sqs = form.search()
    
    if request.is_ajax():
        # The live filter was used. Return a filtered list.
        query = request.GET.get('query')
        sqs = sqs.auto_query(query)

        context = {
            'object_list': sqs,
        }
        return render_to_response(
            "addressbook/includes/search_results.html",
            context,
            context_instance = RequestContext(request)
        )

    # Paginate the results. Note we don't send pagination on ajax requests.
    paginator = Paginator(sqs, 20)

    try:
        page = paginator.page(int(request.GET.get('page',1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
    }
    return render_to_response(
        'addressbook/dashboard.html',
        context,
        context_instance = RequestContext(request)
    )

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
