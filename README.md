Introduction
============

Pathagar is a simple book server for schools where there is little or no internet.
For more information, see [this presentation](http://www.slideshare.net/sverma/pathagar-a-book-server) by Prof. Sameer Verma.
For some of the history of the project, read this [blogpost at OLPC-SF](http://www.olpcsf.org/node/126)

Pathagar2 is a fork to keep simplicity of original project and keeping it alive.

OPDS
====

It uses the OPDS spec:

http://opds-spec.org

It was tested successfully with Aldiko Book Reader on Android.


# Adding Contents

Books can be added via the admin interface, as well as via the command
line, in batch (using CSV files, JSON files or a directory with EPUB
files), through the command:

    python manage.py addbooks

            OR

    python manage.py addepub

Pathagar runs on the python web app framework Django.  It is known to work in Django 1.11


## Loading content

Once installed, Pathagar contains no books. You can upload individual books
through the UI or you can bulk load them by following the instructions below.

### From Internet Archive

You can download book files from Internet Archive. First you need to create
a user and a bookmarks list. Once created, you'll fetch the book files on your
bookmarks list with the `fetch_ia_item` command.

    python manage.py fetch_ia_item --username=<your-username> --out=books.json

This can take a while depending on your internet connection and how many books
you have on your bookmarks list. You might want to go grab a coffee and take
a stretch break.

Once complete, you'll have a `books.json` file which you can use with the
`addbooks` command.

    python manage.py addbooks --json books.json

Learn more about the `addbooks` command below.


### addbooks command

If you have your books already with metadata described in a file, use the
`addbooks` command to import them into Pathagar.


#### CSV format

To add books from a CSV file:

    python manage.py addbooks books.csv

The format of the CSV file is like:

```
"Path to ebook file","Title","Author","Description"
```

If you need to add more fields, please use the JSON file.


#### JSON format

To add books from a JSON file:

    python manage.py addbooks --json books.json

The format of the JSON file is like::

    [
      {
        "book_path": "Path to ebook file",
        "cover_path": "Path to cover image",
        "a_title": "Title",
        "a_author": "Author",
        "a_status": "Published",
        "a_summary": "Description",
        "tags": "set, of, tags"
      },
      ...
    ]

You can add more fields.  Please refer to the Book model.


Dependencies
============

* Python 2.7 or Python 3.5
* Django
* django-taggit
* django-sendfile

Quickstart
==========

* Install mysql (optional)

In Fedora

    sudo yum install -y mysql mysql-devel

* Install requirements

    python3 -m venv venv_pathagar
    . ./venv_pathagar/bin/activate
    pip install -r requirements.pip

* In the Pathagar folder, copy `local_settings.example.py` to
  `local_settings.py` and edit it to suite your needs and environment.

* In the Pathagar folder, run

    python manage.py migrate
    python manage.py createsuperuser

  You will be asked to create an admin user during this stage.

* To run the server, run

    python manage.py runserver

  This starts a server listening on localhost, port 8000

  If the port 8000 is in use, can change the port (by example to 8081) running

    python manage.py runserver 0.0.0.0:8081

* With your browser, access http://localhost:8000 and see if the index
  page comes up. If it comes up, click on "Add books" in the footer to
  start adding books. You will be asked for a username/password. This is
  the admin username/password you supplied while running `createsuperuser`.

  NOTE: You can also mass add books via the command line through CSV files
  or by simply pointing to a directory with a set of EPUB files.

* To run the server in a production environment, look at Django deployment
  docs at : https://docs.djangoproject.com/en/1.11/howto/deployment/
