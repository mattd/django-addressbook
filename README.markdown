##django-addressbook 
###A contact management application for the Django web framework.

Addressbook is intended to be a fully pluggable Django application. By this we mean that everything you need to get going - including template files and static media - will be included. Customize as much as you want, but the idea here is to get you up and running as fast as possible.

NOTE: This software is in a pre-alpha state. If you can make use of pieces of this application, by all means, have at it. Be warned, however, that this code may change substantively. If you need the code for a production environment, consider forking.

##Dependencies

* [django-haystack](http://github.com/toastdriven/django-haystack/) (Optional)

##Enabling Search

Addressbook uses Haystack for full text search. To enable search with Haystack,

1. Setup your search backend by following the tutorial at [haystacksearch.org](http://haystacksearch.org/docs/tutorial.html#initial-setup). That should take you to the end of their Step 2.
2. Put the following code in a file called `search_sites.py` at your project root:

		import haystack
		haystack.autodiscover()

3. Index your data with `python manage.py reindex --verbosity=2`

Search related templates are included in the Addressbook templates directory. Of course, you can also customize the display and indexing templates to your heart's content. Just follow the instructions at the link above.
