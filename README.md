python-ddb
====== 

This is an open source project to use Python bindings for the [DDB
database](http://sourceforge.net/projects/twoddb/) whose original bindings are
in Perl.

The main effort of the DDB project lies in the database and its abstraction
layers. The approach of this project is twofold:

- wrap the existing Perl codebase
- provide pure Python ORM implementations

These efforts can be approach concurrently and where a lot of code needs to be
re-written, it may be more useful to wrap existing Perl code whereas new code
may already be implemented directly in Python.


