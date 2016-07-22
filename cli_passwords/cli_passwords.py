from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from functools import wraps
from getpass import getpass

import keyring

LOG = logging.getLogger(__name__)


class TooManyFailedPasswordAttemptsException(Exception):
    """
    Thrown when there are too many password attempts
    in the retry password function
    """


def get_password(system, username, display=None, refresh=False):
    """
    Gets the password by first looking in the keyring.  If
    the user has already specified the password, then they
    will not be prompted and the stored password will be returned.
    If the password has not been stored yet, or ``refresh=True``
    then the user will be prompted for the password and it will be
    stored.

    Effectively it will ask the user once and then reuse that across
    processes

    .. code-block:: python

        >>> from cli_passwords import get_password
        >>> get_password('my-system', 'username')
        my-system password for username:
        <password>
        >>> get_password('my-system', 'username')
        <password>

    :param unicode system: The name of the system that the password
        is for.  Typically, this will be the cli tools name. It effectively
        acts as a namespace
    :param unicode username: The username that the password corresponds to
    :param unicode display: Defaults to "{system} password for {username}: "
        This will be displayed to the user when/if they are asked for the password
    :param bool refresh: If ``True`` then it will force the user to type in
        the password even if it's already been store
    :return:
    :rtype: unicode
    """
    display = display or '{0} password for {1}: '.format(system, username)
    password = None
    if not refresh:
        password = keyring.get_password(system, username)
    if not password:
        LOG.debug('Refreshing {0} password for user {1}'.format(system, username))
        password = getpass(display)
        keyring.set_password(system, username, password)
    return password


def expire_password(system, username):
    """
    Deletes the password corresponding to the system and username.
    This will completely remove the password from the keyring

    :param unicode system: The name of the system that the password
        is for.  Typically, this will be the cli tools name. It effectively
        acts as a namespace
    :param unicode username: The username that the password corresponds to
    :rtype: None
    """
    LOG.debug('Expiring {0} password for user {1}'.format(system, username))
    keyring.delete_password(system, username)


def inject_password(system, username, display=None, refresh=False):
    """
    Retrieves the password using ``get_password`` and then injects
    it as the first argument in the wrapped function.

    .. code-block:: python

        from cli_passwords import inject_password

        @inject_password('my-system', 'username')
        def my_func(password, arg):
            # Do something with the password

        my_func('arg')

    :param unicode system: The name of the system that the password
        is for.  Typically, this will be the cli tools name. It effectively
        acts as a namespace
    :param unicode username: The username that the password corresponds to
    :param unicode display: Defaults to "{system} password for {username}: "
        This will be displayed to the user when/if they are asked for the password
    :param bool refresh: If ``True`` then it will force the user to type in
        the password even if it's already been store
    :rtype: func
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            password = get_password(system, username, display=display, refresh=refresh)
            LOG.debug('Injecting password into function {0}'.format(func.__name__))
            return func(password, *args, **kwargs)
        return wrapper
    return decorator


def retry_password(system, username, display=None, refresh=False, retries=5, exception=Exception):
    """
    Same as inject password except that when the exception class
    specified in the exception parameter is thrown it will
    prompt the user to enter the password again and then retry
    the function.

    It will only retry up to the int specified by the ``retries``
    keyword argument

    Minimum Example:

    .. code-block:: python

        from cli_passwords import retry_password

        @retry_password('my-system', 'username')
        def my_func(password, parameter1):
            print(parameter1)
            raise Exception('Some Exception')

    .. code-block:: python

        >>> my_func('my-arg')
        my-arg
        my-arg
        my-arg
        my-arg
        my-arg
        Traceback (most recent call last):
            ...
        Exception: Some Exception

    More realistic Example

    .. testcode:: retrypassword2

        from cli_passwords import retry_password

        @retry_password('my-system', 'username', retries=3, exception=AuthenticationException)
        def my_func(password, my_arg):
            print(my_arg)
            throw AuthenticationException('An Exception')

        @retry_password('my-system', 'username', retries=3, exception=AuthenticationException)
        def my_other_func(password, my_arg):
            print(my_arg)
            throw Exception('It won't be retried')

    .. code-block:: python

        >>> my_func('some-arg')
        some-arg
        some-arg
        some-arg
        Traceback (most recent call last):
            ...
        AuthenticationException: An Exception
        >>> my_other_func('some-arg')
        some-arg
        Traceback (most recent call last):
            ...
        Exception: It won't be retried


    :param unicode system: The name of the system that the password
        is for.  Typically, this will be the cli tools name. It effectively
        acts as a namespace
    :param unicode username: The username that the password corresponds to
    :param unicode display: Defaults to "{system} password for {username}: "
        This will be displayed to the user when/if they are asked for the password
    :param bool refresh: If ``True`` then it will force the user to type in
        the password even if it's already been store
    :param int retries: The maximum number of times to retry
        the wrapped function
    :param class exception: This exception will be caught and
        the wrapped function will be retried, requiring the user to
        refresh the password.  Defaults to ``Exception`` but it
        is highly recommended to be more specific with some sort
        of authentication exception
    :return:
    :rtype: func
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < retries:
                count += 1
                password = get_password(system, username, display=display, refresh=refresh)
                try:
                    return func(password, *args, **kwargs)
                except exception as exc:
                    LOG.warning(str(exc), exc_info=True)
                    print('Uh oh, it looks like the {0} password for user'
                          ' {1} was incorrect. '.format(system, username))
                    expire_password(system, username)
            print('Too many password attempts')
            raise TooManyFailedPasswordAttemptsException('Too many failed password attempts')
        return wrapper
    return decorator

