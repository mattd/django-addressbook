from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.generic import generic_inlineformset_factory

from haystack.views import SearchView
from haystack.forms import SearchForm 
from haystack.query import SearchQuerySet

from addressbook.models import Party, Person, Organization, EmailAddress, \
    StreetAddress, PhoneNumber, Website, IMAccount, Note 


@login_required
def party_list(request, searchqueryset, template):
    form = SearchForm()
    if request.GET.get('q'):
        form = SearchForm(request.GET, searchqueryset=searchqueryset)
        if form.is_valid():
            searchqueryset = form.search()
    
    if request.is_ajax():
        # The live filter was used. Return a filtered list.
        query = request.GET.get('query')
        searchqueryset = searchqueryset.auto_query(query)
        context = {
            'object_list': searchqueryset,
        }
        return render_to_response(
            "addressbook/includes/search_results.html",
            context,
            context_instance = RequestContext(request)
        )

    # SearchQuerySet is instantiated in urls.py, thus only loaded once per
    # server process. Get a fresh instance.
    searchqueryset = searchqueryset.all()
    # Paginate the results. Note we don't send pagination on ajax requests.
    paginator = Paginator(searchqueryset, 20)
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
        template,
        context,
        context_instance = RequestContext(request)
    )


def _create_generic_inlineformset_classes():
    """Generate generic formset classes for all generically related models."""
    generic_models = [EmailAddress, StreetAddress, PhoneNumber, Website, 
                      IMAccount, Note]
    formset_classes = []
    for generic_model in generic_models:
        formset_classes.append(generic_inlineformset_factory(
                               generic_model, extra=1, 
                               exclude=('date_added', 'date_modified')))

    return formset_classes


@login_required
def add_party(request, form, template):
    """Add a party child instance - either a Person or an Organization.

    Context includes a form for the object itself and a list of formsets for all
    generically related content types.

    """
    formset_classes = _create_generic_inlineformset_classes()
    formsets = []
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            object = form.save()
            # Bind the request data and connect each formset to our object,
            # then save each if valid.
            for formset_class in formset_classes:
                formsets.append(formset_class(request.POST, instance=object))
            for formset in formsets:
                if formset.is_valid():
                    formset.save()
            # Make sure all formsets passed validation before redirecting.
            if all([formset.is_valid() for formset in formsets]):
                return HttpResponseRedirect(object.get_absolute_url())
    else:
        form = form()
        for formset_class in formset_classes:
            formsets.append(formset_class())
    context = {
        'form': form,
        'formsets': formsets,
    }
    return render_to_response(
        template,
        context,
        context_instance = RequestContext(request)
    )


@login_required
def edit_party(request, form, template, model, object_id):
    """Edit a party child instance - either a Person or an Organization.

    Context includes a form for the object itself and a list of formsets for all
    generically related content types.

    """
    formset_classes = _create_generic_inlineformset_classes()
    formsets = []
    if request.method == 'POST':
        object = get_object_or_404(model, pk=object_id)
        form = form(request.POST, instance=object)
        if form.is_valid():
            object = form.save()
            # Bind the request data and connect each formset to our object,
            # then save each if valid.
            for formset_class in formset_classes:
                formsets.append(formset_class(request.POST, instance=object))
            for formset in formsets:
                if formset.is_valid():
                    formset.save()
            # Make sure all formsets passed validation before redirecting.
            if all([formset.is_valid() for formset in formsets]):
                return HttpResponseRedirect(object.get_absolute_url())
    else:
        object = get_object_or_404(model, pk=object_id)
        if model is Person:
            # Get the Organization name if it exists and send it to the form.
            try:
                initial = {'organization': object.organization.name}
            except AttributeError:
                initial = {}
            form = form(instance=object, initial=initial)
        else:
            form = form(instance=object)
        for formset_class in formset_classes:
            formsets.append(formset_class(instance=object))
    context = {
        'form': form,
        'formsets': formsets,
    }
    return render_to_response(
        template,
        context,
        context_instance = RequestContext(request)
    )


@login_required
def person_detail(request, object_id):
    return object_detail(request, queryset=Person.objects.all(),
                         object_id=object_id)


@login_required
def organization_detail(request, object_id):
    return object_detail(request, queryset=Organization.objects.all(),
                         object_id=object_id)


def autocomplete_organization(request):
    """An ajax-only url returning a .txt of the query results."""
    if request.is_ajax():
        query = request.GET.get('q')
        organizations = Organization.objects.filter(name__istartswith=query)
        context = {
            'organizations': organizations,
        }
        return render_to_response(
            "addressbook/includes/autocomplete_organization.txt",
            context,
            context_instance = RequestContext(request)
        )
    else:
        raise SuspiciousOperation("Access Denied")

