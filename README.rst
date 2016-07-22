===============================
cli-passwords
===============================


.. image:: https://img.shields.io/pypi/v/cli_passwords.svg
        :target: https://pypi.python.org/pypi/cli-passwords

.. image:: https://img.shields.io/travis/timmartin19/cli_passwords.svg
        :target: https://travis-ci.org/timmartin19/cli-passwords

.. image:: https://readthedocs.org/projects/cli-passwords/badge/?version=latest
        :target: https://cli-passwords.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/timmartin19/cli_passwords/shield.svg
     :target: https://pyup.io/repos/github/timmartin19/cli-passwords/
     :alt: Updates


Makes securely getting, storing, and retrying passwords from a command line interface easy!


* Free software: MIT license
* Documentation: https://cli-passwords.readthedocs.io.


Features
--------

* Get passwords from the keyring and if it's not there prompt the user to securely enter their password.  The password will be stored in their keyring and they will not be prompted for their password again
* Inject passwords into functions using the process described above
* Automatically prompt the user to re-enter their password when they inputted the incorrect one

Installation
------------

.. code-block:: bash

    pip install cli-passwords

Quick Start
-----------

Prompt the user for the password and store the password in their keyring.
This password will perists until ``expire_password`` is used or the keyword
argument ``refresh=True`` is passed into the function.

.. code-block:: python

    from cli_passwords import get_password

    # This will prompt the user for their password on the first
    # use only.  Whether it's a month later or minutes later, it
    # will pull the password from the keyring and not prompt the user again
    password = get_password('namespace', 'username')


Inject the password into a function and retry when the password is incorrect.
You can specify the maximum number of retries using the ``retry`` keyword
argument

.. code-block:: python

    from cli_passwords import retry_password

    @retry_password('namespace', 'username', exception=AuthenticationException)
    def my_func(password, arguments):
        if password is not correct:
            raise AuthenticationException('The password is wrong')
        else:
            # do something with the password

    my_func('arguments')


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

