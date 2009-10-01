from haystack import site 
from addressbook.models import Contact, EmailAddress, IMAccount, Note, \
    Organization, PhoneNumber, StreetAddress, Website

site.register(Contact)
site.register(EmailAddress)
site.register(IMAccount)
site.register(Note)
site.register(Organization)
site.register(PhoneNumber)
site.register(StreetAddress)
site.register(Website)
