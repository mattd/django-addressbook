from haystack import indexes
from haystack import site 

from addressbook.models import Organization, Person, EmailAddress, IMAccount, \
    Note, PhoneNumber, StreetAddress, Website


class OrganizationIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    sort_name = indexes.CharField()
    rendered = indexes.CharField(use_template=True, indexed=False)

    def prepare_sort_name(self, object):
        return "%s" % object.name
    

class PersonIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    sort_name = indexes.CharField()
    rendered = indexes.CharField(use_template=True, indexed=False)

    def prepare_sort_name(self, object):
        return "%s %s %s" % (object.last_name, object.first_name,
                             object.middle_name)
    

class EmailAddressIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


class IMAccountIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


class NoteIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


class PhoneNumberIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


class StreetAddressIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


class WebsiteIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)


site.register(Organization, OrganizationIndex)
site.register(Person, PersonIndex)
site.register(EmailAddress)
site.register(IMAccount)
site.register(Note)
site.register(PhoneNumber)
site.register(StreetAddress)
site.register(Website)
