# Introduction

Pathagar is a simple book server for schools where there is little or no
internet. For more information, see [this
presentation](http://www.slideshare.net/sverma/pathagar-a-book-server) by Prof.
Sameer Verma. To get involved, please join our [mailing
list](http://mail.archive.org/cgi-bin/mailman/listinfo/pathagar). For some of
the history of the project, read this [blogpost at
OLPC-SF](http://www.olpcsf.org/node/126). Pathagar is built with the
[Django](https://www.djangoproject.com/) framework.


## OPDS

It uses the [OPDS spec](http://opds-spec.org).


### Known good clients

We've successfully used the following OPDS clients with Pathagar.

- Aldiko Book Reader on Android


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


#### CSV format

To add books from a CSV file:

    python manage.py addbooks books.csv

The format of the CSV file is like:

```
"Path to ebook file","Title","Author","Description"
```

If you need to add more fields, please use the JSON file.


## Dependencies

* Python 2.7 or Python 3.5


## Quickstart

Create a virtualenv and install the dependencies.

    python3 -m venv venv_pathagar
    . ./venv_pathagar/bin/activate
    pip install -r requirements.pip

In the Pathagar folder, copy `local_settings.example.py` to `local_settings.py`
and edit it to suite your needs and environment.

Create the database schema and admin user.

    python manage.py migrate
    python manage.py createsuperuser

You will be asked for an admin username and password during this stage. This is
only for development, so an easy to remember username and password is fine.

Start the development server.

    python manage.py runserver

Open your web browser to [http://localhost:8000/](http://localhost:8000/).

Click on "Add books" in the footer to start adding books. You will be asked for
a username/password. This is the admin username/password you supplied while
running `createsuperuser`.


## Deployment

To run the server in a production environment, look at [Django deployment
docs](https://docs.djangoproject.com/en/1.11/howto/deployment/).

[pathagar.info](http://pathagar.info/get-pathagar/) also contains some common
options for deploying Pathagar.


## Contributing

Bugfix or enhancement are welcome.

Please drop me a message or issue for big feature to avoid duplicate efforts.

The unittest must be working for Python 2.7 and Python 3.5.

To run selenium tests, the tool (geckodriver)[https://github.com/mozilla/geckodriver/releases]
must be downloaded and put somewhere in PATH.
