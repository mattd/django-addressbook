from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.generic import generic_inlineformset_factory

from addressbook.models import Party, Person, Organization, EmailAddress, \
    StreetAddress, PhoneNumber, Website, IMAccount, Note 

@login_required
def party_list(request, model, template):
    try:
        queryset = model.objects.children()
    except AttributeError:
        queryset = model.objects.all()
    if request.is_ajax():
        query = request.GET.get('query', '').replace('+', ' ')
        results = []
        for object in queryset:
            if query.lower() in object.search_index.lower():
                results.append(object)
        return render_to_response(
            "addressbook/includes/search_results.html",
            {'results': results,},
            context_instance = RequestContext(request)
        )
    paginator = Paginator(queryset, 20)
    try:
        page = paginator.page(int(request.GET.get('page',1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'page': page,
        'paginator': paginator,
    }
    return render_to_response(
        template,
        context,
        context_instance = RequestContext(request)
    )


def _create_generic_inlineformsets(post_data=None, object=None):
    """Generate formsets for all generically related models."""
    generic_models = [EmailAddress, StreetAddress, PhoneNumber, Website, 
                      IMAccount, Note]
    formset_classes = []
    for generic_model in generic_models:
        formset_classes.append(generic_inlineformset_factory(
                               generic_model, extra=1,
                               exclude=('date_added', 'date_modified')))
    formsets = []
    for formset_class in formset_classes:
        formsets.append(formset_class(post_data, instance=object))

    return formsets


@login_required
def add_party(request, form, template):
    """Add a party child instance - either a Person or an Organization.

    Context includes a form for the object itself and a list of formsets for all
    generically related content types.

    """
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            object = form.save()
            formsets = _create_generic_inlineformsets(post_data=request.POST, 
                                                      object=object)
            for formset in formsets:
                if formset.is_valid():
                    formset.save()
            # Make sure all formsets passed validation before redirecting.
            if all([formset.is_valid() for formset in formsets]):
                return HttpResponseRedirect(object.get_absolute_url())
        else:
            formsets = _create_generic_inline_formsets()
    else:
        form = form()
        formsets = _create_generic_inlineformsets()
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
    if request.method == 'POST':
        object = get_object_or_404(model, pk=object_id)
        form = form(request.POST, instance=object)
        if form.is_valid():
            object = form.save()
            formsets = _create_generic_inlineformsets(post_data=request.POST, 
                                                      object=object)
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
        formsets = _create_generic_inlineformsets(object=object)
        
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
        organizations = Organization.objects.filter(name__icontains=query)
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

