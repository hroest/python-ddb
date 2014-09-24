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


Install
=======

For the wrapping of Python code to work, you need the python-perlmodule. On
debian, you can get it as follows

```
$ sudo apt-get install libpython-perl
$ git clone https://github.com/nikicat/python-perlmodule
$ python setup.py build
$ sudo python setup.py install
```

Note that the code in the current module is not really installable code but
rather research-grade. 

