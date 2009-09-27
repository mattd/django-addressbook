from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class GenericRelationshipMixin(models.Model):
    """A mixin for adding generic relationship fields to a model."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class DateMixin(models.Model):
    """A mixin for adding created and modified dates to a model."""
    date_added = models.DateTimeField(default=datetime.now)
    date_modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self):
        self.date_modified = datetime.now()
        super(DateMixin, self).save()


class EmailAddress(GenericRelationshipMixin, DateMixin):
    """A generically related email address model."""
    TYPE_CHOICES = (
        ('main', 'Main'),
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    )
    address = models.EmailField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    class Meta:
        verbose_name_plural = 'email addresses'

    def __unicode__(self):
        return u'%s' % self.address


class StreetAddress(GenericRelationshipMixin, DateMixin):
    """A generically related street address model."""
    TYPE_CHOICES = (
        ('main', 'Main'),
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    )
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    class Meta:
        verbose_name_plural = 'street addresses'

    def __unicode__(self):
        return u'%s, %s, %s %s' % (self.address, self.city, self.state,
                                   self.zip)


class PhoneNumber(GenericRelationshipMixin, DateMixin):
    """A generically related phone number model."""
    TYPE_CHOICES = (
        ('main', 'Main'),
        ('home', 'Home'),
        ('work', 'Work'),
        ('mobile', 'Mobile'),
        ('fax', 'Fax'),
        ('other', 'Other'),
    )
    number = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    def __unicode__(self):
        return u'%s' % self.number


class Website(GenericRelationshipMixin, DateMixin):
    """A generically related website model."""
    TYPE_CHOICES = (
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    )
    url = models.URLField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    def __unicode__(self):
        return u'%s' % self.url


class IMAccount(GenericRelationshipMixin, DateMixin):
    """A generically related IM model."""
    SERVICE_CHOICES = (
        ('aim', 'AIM'),
        ('msn', 'MSN'),
        ('icq', 'ICQ'),
        ('jabber', 'Jabber'),
        ('yahoo', 'Yahoo'),
        ('skype', 'Skype'),
        ('qq', 'QQ'),
        ('sametime', 'Sametime'),
        ('gadu-gadu', 'Gadu-Gadu'),
        ('google-talk', 'Google Talk'),
        ('other', 'Other')
    )
    TYPE_CHOICES = (
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    )
    username = models.CharField(max_length=100)
    service = models.CharField(max_length=15, choices=SERVICE_CHOICES, blank=True,
                               null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    class Meta:
        verbose_name = 'IM account'
        verbose_name_plural = 'IM accounts'

    def __unicode__(self):
        return u'%s: %s' % (self.service, self.username)


class Note(GenericRelationshipMixin, DateMixin):
    """A generic note model."""
    content = models.TextField()
    reference_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.content


class ClientInfoMixin(models.Model):
    """An abstract base class providing common client information."""
    street_addresses = generic.GenericRelation(StreetAddress, blank=True, null=True)
    phone_numbers = generic.GenericRelation(PhoneNumber, blank=True, null=True)
    email_addresses = generic.GenericRelation(EmailAddress, blank=True, null=True)
    websites = generic.GenericRelation(Website, blank=True, null=True)
    im_accounts = generic.GenericRelation(IMAccount, blank=True, null=True)
    notes = generic.GenericRelation(Note, blank=True, null=True)

    class Meta:
        abstract = True


class Organization(ClientInfoMixin, DateMixin):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return u'%s' % self.name


class Contact(ClientInfoMixin, DateMixin):
    organization = models.ForeignKey(Organization, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.full_name
        
    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)
        
