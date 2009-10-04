from haystack import site 
from addressbook.models import Person, EmailAddress, IMAccount, Note, \
    Organization, PhoneNumber, StreetAddress, Website

site.register(Person)
site.register(EmailAddress)
site.register(IMAccount)
site.register(Note)
site.register(Organization)
site.register(PhoneNumber)
site.register(StreetAddress)
site.register(Website)
