from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
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


@login_required
def party_add(request, form, template):
    # Setup formset classes for all our generically related data.
    email_formset = generic_inlineformset_factory(EmailAddress,
                    extra=1, exclude=('date_added', 'date_modified'))
    street_formset = generic_inlineformset_factory(StreetAddress,
                     extra=1, exclude=('date_added', 'date_modified'))
    phone_formset = generic_inlineformset_factory(PhoneNumber,
                    extra=1, exclude=('date_added', 'date_modified'))
    website_formset = generic_inlineformset_factory(Website,
                      extra=1, exclude=('date_added', 'date_modified'))
    im_formset = generic_inlineformset_factory(IMAccount,
                 extra=1, exclude=('date_added', 'date_modified'))
    note_formset = generic_inlineformset_factory(Note,
                   extra=1, exclude=('date_added', 'date_modified'))
    formset_classes = [email_formset, street_formset, phone_formset, website_formset, 
                       im_formset, note_formset]

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            object = form.save()
            formsets = [formset_class(request.POST, instance=object)
                        for formset_class in formset_classes]
            for formset in formsets:
                if formset.is_valid():
                    formset.save()
            if all([formset.is_valid() for formset in formsets]):
                return HttpResponseRedirect(object.get_absolute_url())
    else:
        form = form()
        email_formset = email_formset() 
        street_formset = street_formset() 
        phone_formset = phone_formset() 
        website_formset = website_formset() 
        im_formset = im_formset()
        note_formset = note_formset()
    context = {
        'form': form,
        'email_formset': email_formset,
        'street_formset': street_formset,
        'phone_formset': phone_formset,
        'website_formset': website_formset,
        'im_formset': im_formset,
        'note_formset': note_formset,
    }
    return render_to_response(
        template,
        context,
        context_instance = RequestContext(request)
    )


@login_required
def person_detail(request, person_id):
    return object_detail(request, queryset=Person.objects.all(),
                         object_id=person_id)


@login_required
def organization_detail(request, organization_id):
    return object_detail(request, queryset=Organization.objects.all(),
                         object_id=organization_id)
