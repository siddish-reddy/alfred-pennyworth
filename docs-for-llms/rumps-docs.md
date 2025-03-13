================================================
File: README.rst
================================================
rumps
=====

**R**\ idiculously **U**\ ncomplicated **m**\ acOS **P**\ ython **S**\ tatusbar apps.

.. image:: https://raw.github.com/jaredks/rumps/master/examples/rumps_example.png

.. code-block:: python

    import rumps

    class AwesomeStatusBarApp(rumps.App):
        @rumps.clicked("Preferences")
        def prefs(self, _):
            rumps.alert("jk! no preferences available!")

        @rumps.clicked("Silly button")
        def onoff(self, sender):
            sender.state = not sender.state

        @rumps.clicked("Say hi")
        def sayhi(self, _):
            rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    if __name__ == "__main__":
        AwesomeStatusBarApp("Awesome App").run()

How fun!?

``rumps`` can greatly shorten the code required to generate a working app. No ``PyObjC`` underscore syntax required!


Use case
--------

``rumps`` is for any console-based program that would benefit from a simple configuration toolbar or launch menu.

Good for:

* Notification-center-based app
* Controlling daemons / launching separate programs
* Updating simple info from web APIs on a timer

Not good for:

* Any app that is first and foremost a GUI application


Required
--------

* PyObjC
* Python 2.6+

Mac OS X 10.6 was shipped with Python 2.6 as the default version and PyObjC has been included in the default Python
since Mac OS X 10.5. If you're using Mac OS X 10.6+ and the default Python that came with it, then ``rumps`` should be
good to go!


Recommended
-----------

* py2app

For creating standalone apps, just make sure to include ``rumps`` in the ``packages`` list. Most simple statusbar-based
apps are just "background" apps (no icon in the dock; inability to tab to the application) so it is likely that you
would want to set ``'LSUIElement'`` to ``True``. A basic ``setup.py`` would look like,

.. code-block:: python

    from setuptools import setup

    APP = ['example_class.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps'],
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

With this you can then create a standalone,

.. code-block:: bash

    python setup.py py2app


Installation
------------

Using pip,

.. code-block:: bash

    pip install rumps

Or from source,

.. code-block:: bash

    python setup.py install

Both of which will require ``sudo`` if installing in a system-wide location.


Virtual Environments
--------------------

There are issues with using ``virtualenv`` because of the way the Python
executable is copied. Although ``rumps`` attempts to apply a fix (hack) during
the install process, it is not suggested to use ``virtualenv``.

To ensure proper functionality, either use ``venv`` (packaged with Python 3) or
create a standalone app using ``py2app``.

.. code-block:: bash

    python3 -m venv env


Documentation
-------------

Documentation is available at http://rumps.readthedocs.org


================================================
File: docs/alert.rst
================================================
alert
=====

.. autofunction:: rumps.alert



================================================
File: docs/App.rst
================================================
App
===

.. autoclass:: rumps.App
   :members:



================================================
File: docs/application_support.rst
================================================
application_support
===================

.. autofunction:: rumps.application_support



================================================
File: docs/classes.rst
================================================
rumps Classes
=============

.. toctree::
   :maxdepth: 1

   App
   MenuItem
   Window
   Response
   Timer



================================================
File: docs/clicked.rst
================================================
clicked
=======

.. autofunction:: rumps.clicked




================================================
File: docs/creating.rst
================================================
Creating Standalone Applications
================================

If you want to create your own bundled .app you need to download py2app: https://pythonhosted.org/py2app/

For creating standalone apps, just make sure to include ``rumps`` in the ``packages`` list. Most simple statusbar-based
apps are just "background" apps (no icon in the dock; inability to tab to the application) so it is likely that you
would want to set ``'LSUIElement'`` to ``True``. A basic ``setup.py`` would look like,

.. code-block:: python

    from setuptools import setup

    APP = ['example_class.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'plist': {
            'LSUIElement': True,
        },
        'packages': ['rumps'],
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

With this you can then create a standalone,

.. code-block:: bash

    python setup.py py2app



================================================
File: docs/debug_mode.rst
================================================
debug_mode
==========

.. autofunction:: rumps.debug_mode



================================================
File: docs/debugging.rst
================================================
Debugging Your Application
==========================

When writing your application you will want to turn on debugging mode.

.. code-block:: python

    import rumps
    rumps.debug_mode(True)

If you are running your program from the interpreter, you should see the informational messages.

.. code-block:: bash

    python {your app name}.py

If testing the .app generated using py2app, to be able to see these messages you must not,

.. code-block:: bash

    open {your app name}.app

but instead run the executable. While within the directory containing the .app,

.. code-block:: bash

    ./{your app name}.app/Contents/MacOS/{your app name}

And, by default, your .app will be in ``dist`` folder after running ``python setup.py py2app``. So of course that would then be,

.. code-block:: bash

    ./dist/{your app name}.app/Contents/MacOS/{your app name}



================================================
File: docs/examples.rst
================================================
Examples
==============

Sometimes the best way to learn something is by example. Form your own application based on some of these samples.

Simple subclass structure
-------------------------

Just a straightforward application,

.. code-block:: python

    import rumps

    class AwesomeStatusBarApp(rumps.App):
        def __init__(self):
            super(AwesomeStatusBarApp, self).__init__("Awesome App")
            self.menu = ["Preferences", "Silly button", "Say hi"]

        @rumps.clicked("Preferences")
        def prefs(self, _):
            rumps.alert("jk! no preferences available!")

        @rumps.clicked("Silly button")
        def onoff(self, sender):
            sender.state = not sender.state

        @rumps.clicked("Say hi")
        def sayhi(self, _):
            rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    if __name__ == "__main__":
        AwesomeStatusBarApp().run()

Decorating any functions
------------------------

The following code demonstrates how you can decorate functions with :func:`rumps.clicked` whether or not they are inside a subclass of :class:`rumps.App`. The parameter ``sender``, the :class:`rumps.MenuItem` object, is correctly passed to both functions even though ``button`` needs an instance of ``SomeApp`` as its ``self`` parameter.

Usually functions registered as callbacks should accept one and only one argument but an `App` subclass is viewed as a special case as its use can provide a simple and pythonic way to implement the logic behind an application.

.. code-block:: python

    from rumps import *

    @clicked('Testing')
    def tester(sender):
        sender.state = not sender.state

    class SomeApp(rumps.App):
        def __init__(self):
            super(SomeApp, self).__init__(type(self).__name__, menu=['On', 'Testing'])
            rumps.debug_mode(True)

        @clicked('On')
        def button(self, sender):
            sender.title = 'Off' if sender.title == 'On' else 'On'
            Window("I can't think of a good example app...").run()

    if __name__ == "__main__":
        SomeApp().run()

New features in 0.2.0
---------------------

Menu items can be disabled (greyed out) by passing ``None`` to :meth:`rumps.MenuItem.set_callback`. :func:`rumps.alert` no longer requires `title` (will use a default localized string) and allows for custom `cancel` button text. The new parameter `quit_button` for :class:`rumps.App` allows for custom quit button text or removal of the quit button entirely by passing ``None``.

.. warning::
   By setting :attr:`rumps.App.quit_button` to ``None`` you **must include another way to quit the application** by somehow calling :func:`rumps.quit_application` otherwise you will have to force quit.

.. code-block:: python

    import rumps
    
    rumps.debug_mode(True)
    
    @rumps.clicked('Print Something')
    def print_something(_):
        rumps.alert(message='something', ok='YES!', cancel='NO!')
    
    
    @rumps.clicked('On/Off Test')
    def on_off_test(_):
        print_button = app.menu['Print Something']
        if print_button.callback is None:
            print_button.set_callback(print_something)
        else:
            print_button.set_callback(None)
    
    
    @rumps.clicked('Clean Quit')
    def clean_up_before_quit(_):
        print 'execute clean up code'
        rumps.quit_application()
    
    
    app = rumps.App('Hallo Thar', menu=['Print Something', 'On/Off Test', 'Clean Quit'], quit_button=None)
    app.run()




================================================
File: docs/functions.rst
================================================
rumps Functions
===============

.. toctree::
   :maxdepth: 1

   notifications
   clicked
   timerfunc
   timers
   application_support
   notification
   alert
   debug_mode
   quit_application



================================================
File: docs/index.rst
================================================
.. rumps documentation master file, created by
   sphinx-quickstart on Mon Aug  4 23:56:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to rumps
================

rumps is...

Ridiculously Uncomplicated Mac os x Python Statusbar apps!

rumps exposes Objective-C classes as Python classes and functions which greatly simplifies the process of creating a statusbar application.

Say you have a Python program and want to create a relatively simple interface for end user interaction on a Mac. There are a number of GUI tools available to Python programmers (PyQt, Tkinter, PyGTK, WxPython, etc.) but most are overkill if you just want to expose a few configuration options or an execution switch.

If all you want is a statusbar app, rumps makes it easy.

GitHub project: https://github.com/jaredks/rumps

Contents:

.. toctree::
   :maxdepth: 2

   examples
   creating
   debugging
   classes
   functions


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`




================================================
File: docs/MenuItem.rst
================================================
MenuItem
========

.. autoclass:: rumps.MenuItem
   :members:
   :inherited-members:

   .. method:: d[key]

      Return the item of d with key `key`. Raises a ``KeyError`` if key is not in the map.

   .. method:: d[key] = value

      Set `d[key]` to `value` if `key` does not exist in d. `value` will be converted to a `MenuItem` object if not one already.

   .. method:: del d[key]

      Remove `d[key]` from d. Raises a ``KeyError`` if `key` is not in the map.



================================================
File: docs/notification.rst
================================================
notification
============

.. autofunction:: rumps.notification



================================================
File: docs/notifications.rst
================================================
notifications
=============

.. autofunction:: rumps.notifications



================================================
File: docs/quit_application.rst
================================================
quit_application
================

.. autofunction:: rumps.quit_application



================================================
File: docs/Response.rst
================================================
Response
========

.. autoclass:: rumps.rumps.Response
   :members:



================================================
File: docs/Timer.rst
================================================
Timer
=====

.. autoclass:: rumps.Timer
   :members:



================================================
File: docs/timerfunc.rst
================================================
timer
=====

.. autofunction:: rumps.timer



================================================
File: docs/timers.rst
================================================
timers
======

.. autofunction:: rumps.timers



================================================
File: docs/Window.rst
================================================
Window
======

.. autoclass:: rumps.Window
   :members:



================================================
File: examples/example_0_2_0_features.py
================================================
import rumps

rumps.debug_mode(True)

@rumps.clicked('Print Something')
def print_something(_):
    rumps.alert(message='something', ok='YES!', cancel='NO!')


@rumps.clicked('On/Off Test')
def on_off_test(_):
    print_button = app.menu['Print Something']
    if print_button.callback is None:
        print_button.set_callback(print_something)
    else:
        print_button.set_callback(None)


@rumps.clicked('Clean Quit')
def clean_up_before_quit(_):
    print('execute clean up code')
    rumps.quit_application()


app = rumps.App('Hallo Thar', menu=['Print Something', 'On/Off Test', 'Clean Quit'], quit_button=None)
app.run()



================================================
File: examples/example_class.py
================================================
import rumps

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp().run()



================================================
File: examples/example_class_new_style.py
================================================
import rumps

class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

if __name__ == "__main__":
    AwesomeStatusBarApp("Awesome App").run()



================================================
File: examples/example_delayed_callbacks.py
================================================
from rumps import *

@clicked('Testing')
def tester(sender):
    sender.state = not sender.state

class SomeApp(rumps.App):
    def __init__(self):
        super(SomeApp, self).__init__(type(self).__name__, menu=['On', 'Testing'])
        rumps.debug_mode(True)

    @clicked('On')
    def button(self, sender):
        sender.title = 'Off' if sender.title == 'On' else 'On'
        Window("I can't think of a good example app...").run()

if __name__ == "__main__":
    SomeApp().run()



================================================
File: examples/example_dynamic_title_icon.py
================================================
import rumps

rumps.debug_mode(True)

@rumps.clicked('Icon', 'On')
def a(_):
    app.icon = 'pony.jpg'

@rumps.clicked('Icon', 'Off')
def b(_):
    app.icon = None

@rumps.clicked('Title', 'On')
def c(_):
    app.title = 'Buzz'

@rumps.clicked('Title', 'Off')
def d(_):
    app.title = None

app = rumps.App('Buzz Application', quit_button=rumps.MenuItem('Quit Buzz', key='q'))
app.menu = [
    ('Icon', ('On', 'Off')),
    ('Title', ('On', 'Off'))
]
app.run()



================================================
File: examples/example_menu.py
================================================
from rumps import *

try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

def sayhello(sender):
    print('hello {}'.format(sender))

def e(_):
    print('EEEEEEE')

def adjust_f(sender):
    if adjust_f.huh:
        sender.add('$')
        sender.add('%')
        sender['zzz'] = 'zzz'
        sender['separator'] = separator
        sender['ppp'] = MenuItem('ppp')
    else:
        del sender['$']
        del sender['%']
        del sender['separator']
        del sender['ppp']
    adjust_f.huh = not adjust_f.huh
adjust_f.huh = True

def print_f(_):
    print(f)

f = MenuItem('F', callback=adjust_f)

urlretrieve('http://upload.wikimedia.org/wikipedia/commons/thumb/c/'
            'c4/Kiss_Logo.svg/200px-Kiss_Logo.svg.png', 'kiss.png')
app = App('lovegun', icon='kiss.png')
app.menu = [
    MenuItem('A', callback=print_f, key='F'),
    ('B', ['1', 2, '3', [4, [5, (6, range(7, 14))]]]),
    'C',
    [MenuItem('D', callback=sayhello), (1, 11, 111)],
    MenuItem('E', callback=e, key='e'),
    f,
    None,
    {
        'x': {'hello', 'hey'},
        'y': ['what is up']
    },
    [1, [2]],
    ('update method', ['walking', 'back', 'to', 'you']),
    'stuff',
    None
]

@clicked('update method')
def dict_update(menu):
    print(menu)
    print(menu.setdefault('boo', MenuItem('boo',
                                          callback=lambda _: add_separator(menu))))  # lambda gets THIS menu not submenu

def add_separator(menu):
    menu.add(separator)

@clicked('C')
def change_main_menu(_):
    print(app.menu)
    print('goodbye C')
    del app.menu['C']  # DELETE SELF!!!1

@clicked('stuff')
def stuff(sender):
    print(sender)
    if len(sender):
        sender.insert_after('lets', 'go?')
        sender['the'].insert_before('band', 'not')
        sender['the'].insert_before('band', 'a')
    else:
        sender.update(['hey', ['ho', MenuItem('HOOOO')], 'lets', 'teenage'], the=['who', 'is', 'band'])
        sender.add('waste land')

app.run()



================================================
File: examples/example_simple.py
================================================
import rumps
import time

rumps.debug_mode(True)  # turn on command line logging information for development - default is off


@rumps.clicked("About")
def about(sender):
    sender.title = 'NOM' if sender.title == 'About' else 'About'  # can adjust titles of menu items dynamically
    rumps.alert("This is a cool app!")


@rumps.clicked("Arbitrary", "Depth", "It's pretty easy")  # very simple to access nested menu items
def does_something(sender):
    my_data = {'poop': 88}
    rumps.notification(title='Hi', subtitle='There.', message='Friend!', sound=does_something.sound, data=my_data)
does_something.sound = True


@rumps.clicked("Preferences")
def not_actually_prefs(sender):
    if not sender.icon:
        sender.icon = 'level_4.png'
    sender.state = not sender.state
    does_something.sound = not does_something.sound


@rumps.timer(4)  # create a new thread that calls the decorated function every 4 seconds
def write_unix_time(sender):
    with app.open('times', 'a') as f:  # this opens files in your app's Application Support folder
        f.write('The unix time now: {}\n'.format(time.time()))


@rumps.clicked("Arbitrary")
def change_statusbar_title(sender):
    app.title = 'Hello World' if app.title != 'Hello World' else 'World, Hello'


@rumps.notifications
def notifications(notification):  # function that reacts to incoming notification dicts
    print(notification)


def onebitcallback(sender):  # functions don't have to be decorated to serve as callbacks for buttons
    print(4848484)           # this function is specified as a callback when creating a MenuItem below


if __name__ == "__main__":
    app = rumps.App("My Toolbar App", title='World, Hello')
    app.menu = [
        rumps.MenuItem('About', icon='pony.jpg', dimensions=(18, 18)),  # can specify an icon to be placed near text
        'Preferences',
        None,  # None functions as a separator in your menu
        {'Arbitrary':
            {"Depth": ["Menus", "It's pretty easy"],
             "And doesn't": ["Even look like Objective C", rumps.MenuItem("One bit", callback=onebitcallback)]}},
        None
    ]
    app.run()



================================================
File: examples/example_timers.py
================================================
import rumps
import time


def timez():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())


@rumps.timer(1)
def a(sender):
    print('%r %r' % (sender, timez()))


@rumps.clicked('Change timer')
def changeit(_):
    response = rumps.Window('Enter new interval').run()
    if response.clicked:
        global_namespace_timer.interval = int(response.text)


@rumps.clicked('All timers')
def activetimers(_):
    print(rumps.timers())


@rumps.clicked('Start timer')
def start_timer(_):
    global_namespace_timer.start()


@rumps.clicked('Stop timer')
def stop_timer(_):
    global_namespace_timer.stop()


if __name__ == "__main__":
    global_namespace_timer = rumps.Timer(a, 4)
    rumps.App('fuuu', menu=('Change timer', 'All timers', 'Start timer', 'Stop timer')).run()



================================================
File: examples/example_windows.py
================================================
import rumps

window = rumps.Window('Nothing...', 'ALERTZ')
window.title = 'WINDOWS jk'
window.message = 'Something.'
window.default_text = 'eh'

response = window.run()
print (response)

window.add_buttons('One', 'Two', 'Three')

print (window.run())



================================================
File: examples/setup.py
================================================
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['example_class.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)



================================================
File: rumps/__init__.py
================================================
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rumps: Ridiculously Uncomplicated macOS Python Statusbar apps.
# Copyright: (c) 2020, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
rumps
=====

Ridiculously Uncomplicated macOS Python Statusbar apps.

rumps exposes Objective-C classes as Python classes and functions which greatly simplifies the process of creating a
statusbar application.
"""

__title__ = 'rumps'
__version__ = '0.4.0'
__author__ = 'Jared Suttles'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2020 Jared Suttles'

from . import notifications as _notifications
from .rumps import (separator, debug_mode, alert, application_support, timers, quit_application, timer,
                    clicked, MenuItem, SliderMenuItem, Timer, Window, App, slider)

notifications = _notifications.on_notification
notification = _notifications.notify



================================================
File: rumps/_internal.py
================================================
# -*- coding: utf-8 -*-

from __future__ import print_function

import inspect
import traceback

import Foundation

from . import compat
from . import exceptions


def require_string(*objs):
    for obj in objs:
        if not isinstance(obj, compat.string_types):
            raise TypeError(
                'a string is required but given {0}, a {1}'.format(obj, type(obj).__name__)
            )


def require_string_or_none(*objs):
    for obj in objs:
        if not(obj is None or isinstance(obj, compat.string_types)):
            raise TypeError(
                'a string or None is required but given {0}, a {1}'.format(obj, type(obj).__name__)
            )


def call_as_function_or_method(func, *args, **kwargs):
    # The idea here is that when using decorators in a class, the functions passed are not bound so we have to
    # determine later if the functions we have (those saved as callbacks) for particular events need to be passed
    # 'self'.
    #
    # This works for an App subclass method or a standalone decorated function. Will attempt to find function as
    # a bound method of the App instance. If it is found, use it, otherwise simply call function.
    from . import rumps
    try:
        app = getattr(rumps.App, '*app_instance')
    except AttributeError:
        pass
    else:
        for name, method in inspect.getmembers(app, predicate=inspect.ismethod):
            if method.__func__ is func:
                return method(*args, **kwargs)
    return func(*args, **kwargs)


def guard_unexpected_errors(func):
    """Decorator to be used in PyObjC callbacks where an error bubbling up
    would cause a crash. Instead of crashing, print the error to stderr and
    prevent passing to PyObjC layer.

    For Python 3, print the exception using chaining. Accomplished by setting
    the cause of :exc:`rumps.exceptions.InternalRumpsError` to the exception.

    For Python 2, emulate exception chaining by printing the original exception
    followed by :exc:`rumps.exceptions.InternalRumpsError`.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            internal_error = exceptions.InternalRumpsError(
                'an unexpected error occurred within an internal callback'
            )
            if compat.PY2:
                import sys
                traceback.print_exc()
                print('\nThe above exception was the direct cause of the following exception:\n', file=sys.stderr)
                traceback.print_exception(exceptions.InternalRumpsError, internal_error, None)
            else:
                internal_error.__cause__ = e
                traceback.print_exception(exceptions.InternalRumpsError, internal_error, None)

    return wrapper


def string_to_objc(x):
    if isinstance(x, compat.binary_type):
        return Foundation.NSData.alloc().initWithData_(x)
    elif isinstance(x, compat.string_types):
        return Foundation.NSString.alloc().initWithString_(x)
    else:
        raise TypeError(
            "expected a string or a bytes-like object but provided %s, "
            "having type '%s'" % (
                x,
                type(x).__name__
            )
        )



================================================
File: rumps/compat.py
================================================
# -*- coding: utf-8 -*-

"""
rumps.compat
~~~~~~~~~~~~

Compatibility for Python 2 and Python 3 major versions.

:copyright: (c) 2020 by Jared Suttles
:license: BSD-3-Clause, see LICENSE for details.
"""

import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    binary_type = bytes
    text_type = str
    string_types = (str,)

    iteritems = lambda d: iter(d.items())

    import collections.abc as collections_abc

else:
    binary_type = ()
    text_type = unicode
    string_types = (str, unicode)

    iteritems = lambda d: d.iteritems()

    import collections as collections_abc



================================================
File: rumps/events.py
================================================
# -*- coding: utf-8 -*-

import traceback

from . import _internal


class EventEmitter(object):
    def __init__(self, name):
        self.name = name
        self.callbacks = set()
        self._executor = _internal.call_as_function_or_method

    def register(self, func):
        self.callbacks.add(func)
        return func

    def unregister(self, func):
        try:
            self.callbacks.remove(func)
            return True
        except KeyError:
            return False

    def emit(self, *args, **kwargs):
        #print('EventEmitter("%s").emit called' % self.name)
        for callback in self.callbacks:
            try:
                self._executor(callback, *args, **kwargs)
            except Exception:
                traceback.print_exc()

    __call__ = register


before_start = EventEmitter('before_start')
on_notification = EventEmitter('on_notification')
on_sleep = EventEmitter('on_sleep')
on_wake = EventEmitter('on_wake')
before_quit = EventEmitter('before_quit')



================================================
File: rumps/exceptions.py
================================================
# -*- coding: utf-8 -*-


class RumpsError(Exception):
    """A generic rumps error occurred."""


class InternalRumpsError(RumpsError):
    """Internal mechanism powering functionality of rumps failed."""



================================================
File: rumps/notifications.py
================================================
# -*- coding: utf-8 -*-

_ENABLED = True
try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
except ImportError:
    _ENABLED = False

import datetime
import os
import sys
import traceback

import Foundation

from . import _internal
from . import compat
from . import events


def on_notification(f):
    """Decorator for registering a function to serve as a "notification center"
    for the application. This function will receive the data associated with an
    incoming macOS notification sent using :func:`rumps.notification`. This
    occurs whenever the user clicks on a notification for this application in
    the macOS Notification Center.

    .. code-block:: python

        @rumps.notifications
        def notification_center(info):
            if 'unix' in info:
                print 'i know this'

    """
    return events.on_notification.register(f)


def _gather_info_issue_9():  # pragma: no cover
    missing_plist = False
    missing_bundle_ident = False
    info_plist_path = os.path.join(os.path.dirname(sys.executable), 'Info.plist')
    try:
        with open(info_plist_path) as f:
            import plistlib
            try:
                load_plist = plistlib.load
            except AttributeError:
                load_plist = plistlib.readPlist
            try:
                load_plist(f)['CFBundleIdentifier']
            except Exception:
                missing_bundle_ident = True

    except IOError as e:
        import errno
        if e.errno == errno.ENOENT:  # No such file or directory
            missing_plist = True

    info = '\n\n'
    if missing_plist:
        info += 'In this case there is no file at "%(info_plist_path)s"'
        info += '\n\n'
        confidence = 'should'
    elif missing_bundle_ident:
        info += 'In this case the file at "%(info_plist_path)s" does not contain a value for "CFBundleIdentifier"'
        info += '\n\n'
        confidence = 'should'
    else:
        confidence = 'may'
    info += 'Running the following command %(confidence)s fix the issue:\n'
    info += '/usr/libexec/PlistBuddy -c \'Add :CFBundleIdentifier string "rumps"\' %(info_plist_path)s\n'
    return info % {'info_plist_path': info_plist_path, 'confidence': confidence}


def _default_user_notification_center():
    notification_center = NSUserNotificationCenter.defaultUserNotificationCenter()
    if notification_center is None:  # pragma: no cover
        info = (
            'Failed to setup the notification center. This issue occurs when the "Info.plist" file '
            'cannot be found or is missing "CFBundleIdentifier".'
        )
        try:
            info += _gather_info_issue_9()
        except Exception:
            pass
        raise RuntimeError(info)
    else:
        return notification_center


def _init_nsapp(nsapp):
    if _ENABLED:
        try:
            notification_center = _default_user_notification_center()
        except RuntimeError:
            pass
        else:
            notification_center.setDelegate_(nsapp)


@_internal.guard_unexpected_errors
def _clicked(ns_user_notification_center, ns_user_notification):
    from . import rumps

    ns_user_notification_center.removeDeliveredNotification_(ns_user_notification)
    ns_dict = ns_user_notification.userInfo()
    if ns_dict is None:
        data = None
    else:
        dumped = ns_dict['value']
        app = getattr(rumps.App, '*app_instance', rumps.App)
        try:
            data = app.serializer.loads(dumped)
        except Exception:
            traceback.print_exc()
            return

    # notification center function not specified => no error but log warning
    if not events.on_notification.callbacks:
        rumps._log(
            'WARNING: notification received but no function specified for '
            'answering it; use @notifications decorator to register a function.'
        )
    else:
        notification = Notification(ns_user_notification, data)
        events.on_notification.emit(notification)


def notify(title, subtitle, message, data=None, sound=True,
           action_button=None, other_button=None, has_reply_button=False,
           icon=None, ignoreDnD=False):
    """Send a notification to Notification Center (OS X 10.8+). If running on a
    version of macOS that does not support notifications, a ``RuntimeError``
    will be raised. Apple says,

        "The userInfo content must be of reasonable serialized size (less than
        1k) or an exception will be thrown."

    So don't do that!

    :param title: text in a larger font.
    :param subtitle: text in a smaller font below the `title`.
    :param message: text representing the body of the notification below the
                    `subtitle`.
    :param data: will be passed to the application's "notification center" (see
                 :func:`rumps.notifications`) when this notification is clicked.
    :param sound: whether the notification should make a noise when it arrives.
    :param action_button: title for the action button.
    :param other_button: title for the other button.
    :param has_reply_button: whether or not the notification has a reply button.
    :param icon: the filename of an image for the notification's icon, will
                 replace the default.
    :param ignoreDnD: whether the notification should ignore do not disturb,
                 e.g., appear also while screen sharing.
    """
    from . import rumps

    if not _ENABLED:
        raise RuntimeError('OS X 10.8+ is required to send notifications')

    _internal.require_string_or_none(title, subtitle, message)

    notification = NSUserNotification.alloc().init()

    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)

    if data is not None:
        app = getattr(rumps.App, '*app_instance', rumps.App)
        dumped = app.serializer.dumps(data)
        objc_string = _internal.string_to_objc(dumped)
        ns_dict = Foundation.NSMutableDictionary.alloc().init()
        ns_dict.setDictionary_({'value': objc_string})
        notification.setUserInfo_(ns_dict)

    if icon is not None:
        notification.set_identityImage_(rumps._nsimage_from_file(icon))
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    if action_button:
        notification.setActionButtonTitle_(action_button)
        notification.set_showsButtons_(True)
    if other_button:
        notification.setOtherButtonTitle_(other_button)
        notification.set_showsButtons_(True)
    if has_reply_button:
        notification.setHasReplyButton_(True)
    if ignoreDnD:
        notification.set_ignoresDoNotDisturb_(True)

    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date()))
    notification_center = _default_user_notification_center()
    notification_center.scheduleNotification_(notification)


class Notification(compat.collections_abc.Mapping):
    def __init__(self, ns_user_notification, data):
        self._ns = ns_user_notification
        self._data = data

    def __repr__(self):
        return '<{0}: [data: {1}]>'.format(type(self).__name__, repr(self._data))

    @property
    def title(self):
        return compat.text_type(self._ns.title())

    @property
    def subtitle(self):
        return compat.text_type(self._ns.subtitle())

    @property
    def message(self):
        return compat.text_type(self._ns.informativeText())

    @property
    def activation_type(self):
        activation_type = self._ns.activationType()
        if activation_type == 1:
            return 'contents_clicked'
        elif activation_type == 2:
            return 'action_button_clicked'
        elif activation_type == 3:
            return 'replied'
        elif activation_type == 4:
            return 'additional_action_clicked'

    @property
    def delivered_at(self):
        ns_date = self._ns.actualDeliveryDate()
        seconds = ns_date.timeIntervalSince1970()
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt

    @property
    def response(self):
        ns_attributed_string = self._ns.response()
        if ns_attributed_string is None:
            return None
        ns_string = ns_attributed_string.string()
        return compat.text_type(ns_string)

    @property
    def data(self):
        return self._data

    def _check_if_mapping(self):
        if not isinstance(self._data, compat.collections_abc.Mapping):
            raise TypeError(
                'notification cannot be used as a mapping when data is not a '
                'mapping'
            )

    def __getitem__(self, key):
        self._check_if_mapping()
        return self._data[key]

    def __iter__(self):
        self._check_if_mapping()
        return iter(self._data)

    def __len__(self):
        self._check_if_mapping()
        return len(self._data)



================================================
File: rumps/rumps.py
================================================
# -*- coding: utf-8 -*-

# rumps: Ridiculously Uncomplicated macOS Python Statusbar apps.
# Copyright: (c) 2020, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.


# For compatibility with pyinstaller
# See: http://stackoverflow.com/questions/21058889/pyinstaller-not-finding-pyobjc-library-macos-python
import Foundation
import AppKit

from Foundation import (NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSSearchPathForDirectoriesInDomains,
                        NSMakeRect, NSLog, NSObject, NSMutableDictionary, NSString, NSUserDefaults)
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSAlert, NSTextField, NSSecureTextField, NSImage, NSSlider, NSSize, NSWorkspace, NSWorkspaceWillSleepNotification, NSWorkspaceDidWakeNotification, NSView
from PyObjCTools import AppHelper

import os
import pickle
import traceback
import weakref

from .compat import text_type, string_types, iteritems, collections_abc
from .text_field import Editing, SecureEditing
from .utils import ListDict

from . import _internal
from . import events
from . import notifications

_TIMERS = weakref.WeakKeyDictionary()
separator = object()


def debug_mode(choice):
    """Enable/disable printing helpful information for debugging the program. Default is off."""
    global _log
    if choice:
        def _log(*args):
            NSLog(' '.join(map(str, args)))
    else:
        def _log(*_):
            pass
debug_mode(False)


def alert(title=None, message='', ok=None, cancel=None, other=None, icon_path=None):
    """Generate a simple alert window.

    .. versionchanged:: 0.2.0
        Providing a `cancel` string will set the button text rather than only using text "Cancel". `title` is no longer
        a required parameter.

    .. versionchanged:: 0.3.0
        Add `other` button functionality as well as `icon_path` to change the alert icon.

    :param title: the text positioned at the top of the window in larger font. If ``None``, a default localized title
                  is used. If not ``None`` or a string, will use the string representation of the object.
    :param message: the text positioned below the `title` in smaller font. If not a string, will use the string
                    representation of the object.
    :param ok: the text for the "ok" button. Must be either a string or ``None``. If ``None``, a default
               localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button will have that text. If `cancel`
                   evaluates to ``True``, will create a button with text "Cancel". Otherwise, this button will not be
                   created.
    :param other: the text for the "other" button. If a string, the button will have that text. Otherwise, this button will not be
                   created.
    :param icon_path: a path to an image. If ``None``, the applications icon is used.
    :return: a number representing the button pressed. The "ok" button is ``1`` and "cancel" is ``0``.
    """
    message = text_type(message)
    message = message.replace('%', '%%')
    if title is not None:
        title = text_type(title)
    _internal.require_string_or_none(ok)
    if not isinstance(cancel, string_types):
        cancel = 'Cancel' if cancel else None
    alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title, ok, cancel, other, message)
    if NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle') == 'Dark':
        alert.window().setAppearance_(AppKit.NSAppearance.appearanceNamed_('NSAppearanceNameVibrantDark'))
    alert.setAlertStyle_(0)  # informational style
    if icon_path is not None:
        icon = _nsimage_from_file(icon_path)
        alert.setIcon_(icon)
    _log('alert opened with message: {0}, title: {1}'.format(repr(message), repr(title)))
    return alert.runModal()


def application_support(name):
    """Return the application support folder path for the given `name`, creating it if it doesn't exist."""
    app_support_path = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, 1).objectAtIndex_(0), name)
    if not os.path.isdir(app_support_path):
        os.mkdir(app_support_path)
    return app_support_path


def timers():
    """Return a list of all :class:`rumps.Timer` objects. These can be active or inactive."""
    return list(_TIMERS)


def quit_application(sender=None):
    """Quit the application. Some menu item should call this function so that the application can exit gracefully."""
    nsapplication = NSApplication.sharedApplication()
    _log('closing application')
    nsapplication.terminate_(sender)


def _nsimage_from_file(filename, dimensions=None, template=None):
    """Take a path to an image file and return an NSImage object."""
    try:
        _log('attempting to open image at {0}'.format(filename))
        with open(filename):
            pass
    except IOError:  # literal file path didn't work -- try to locate image based on main script path
        try:
            from __main__ import __file__ as main_script_path
            main_script_path = os.path.dirname(main_script_path)
            filename = os.path.join(main_script_path, filename)
        except ImportError:
            pass
        _log('attempting (again) to open image at {0}'.format(filename))
        with open(filename):  # file doesn't exist
            pass              # otherwise silently errors in NSImage which isn't helpful for debugging
    image = NSImage.alloc().initByReferencingFile_(filename)
    image.setScalesWhenResized_(True)
    image.setSize_((20, 20) if dimensions is None else dimensions)
    if not template is None:
        image.setTemplate_(template)
    return image


# Decorators and helper function serving to register functions for dealing with interaction and events
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def timer(interval):
    """Decorator for registering a function as a callback in a new thread. The function will be repeatedly called every
    `interval` seconds. This decorator accomplishes the same thing as creating a :class:`rumps.Timer` object by using
    the decorated function and `interval` as parameters and starting it on application launch.

    .. code-block:: python

        @rumps.timer(2)
        def repeating_function(sender):
            print 'hi'

    :param interval: a number representing the time in seconds before the decorated function should be called.
    """
    def decorator(f):
        timers = timer.__dict__.setdefault('*timers', [])
        timers.append(Timer(f, interval))
        return f
    return decorator


def clicked(*args, **options):
    """Decorator for registering a function as a callback for a click action on a :class:`rumps.MenuItem` within the
    application. The passed `args` must specify an existing path in the main menu. The :class:`rumps.MenuItem`
    instance at the end of that path will have its :meth:`rumps.MenuItem.set_callback` method called, passing in the
    decorated function.

    .. versionchanged:: 0.2.1
        Accepts `key` keyword argument.

    .. code-block:: python

        @rumps.clicked('Animal', 'Dog', 'Corgi')
        def corgi_button(sender):
            import subprocess
            subprocess.call(['say', '"corgis are the cutest"'])

    :param args: a series of strings representing the path to a :class:`rumps.MenuItem` in the main menu of the
                 application.
    :param key: a string representing the key shortcut as an alternative means of clicking the menu item.
    """
    def decorator(f):

        def register_click(self):
            menuitem = self._menu  # self not defined yet but will be later in 'run' method
            if menuitem is None:
                raise ValueError('no menu created')
            for arg in args:
                try:
                    menuitem = menuitem[arg]
                except KeyError:
                    menuitem.add(arg)
                    menuitem = menuitem[arg]
            menuitem.set_callback(f, options.get('key'))

        # delay registering the button until we have a current instance to be able to traverse the menu
        buttons = clicked.__dict__.setdefault('*buttons', [])
        buttons.append(register_click)

        return f
    return decorator


def slider(*args, **options):
    """Decorator for registering a function as a callback for a slide action on a :class:`rumps.SliderMenuItem` within
    the application. All elements of the provided path will be created as :class:`rumps.MenuItem` objects. The
    :class:`rumps.SliderMenuItem` will be created as a child of the last menu item.

    Accepts the same keyword arguments as :class:`rumps.SliderMenuItem`.

    .. versionadded:: 0.3.0

    :param args: a series of strings representing the path to a :class:`rumps.SliderMenuItem` in the main menu of the
                 application.
    """
    def decorator(f):

        def register_click(self):

            # self not defined yet but will be later in 'run' method
            menuitem = self._menu
            if menuitem is None:
                raise ValueError('no menu created')

            # create here in case of error so we don't create the path
            slider_menu_item = SliderMenuItem(**options)
            slider_menu_item.set_callback(f)

            for arg in args:
                try:
                    menuitem = menuitem[arg]
                except KeyError:
                    menuitem.add(arg)
                    menuitem = menuitem[arg]

            menuitem.add(slider_menu_item)

        # delay registering the button until we have a current instance to be able to traverse the menu
        buttons = clicked.__dict__.setdefault('*buttons', [])
        buttons.append(register_click)

        return f
    return decorator

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Menu(ListDict):
    """Wrapper for Objective-C's NSMenu class.

    Implements core functionality of menus in rumps. :class:`rumps.MenuItem` subclasses `Menu`.
    """

    # NOTE:
    # Only ever used as the main menu since every other menu would exist as a submenu of a MenuItem

    _choose_key = object()

    def __init__(self):
        self._counts = {}
        if not hasattr(self, '_menu'):
            self._menu = NSMenu.alloc().init()
        super(Menu, self).__init__()

    def __setitem__(self, key, value):
        if key not in self:
            key, value = self._process_new_menuitem(key, value)
            self._menu.addItem_(value._menuitem)
            if isinstance(value, SliderMenuItem):
                self._set_subview_dimensions(self, value)
            super(Menu, self).__setitem__(key, value)

    def __delitem__(self, key):
        value = self[key]
        self._menu.removeItem_(value._menuitem)
        super(Menu, self).__delitem__(key)

    def add(self, menuitem):
        """Adds the object to the menu as a :class:`rumps.MenuItem` using the :attr:`rumps.MenuItem.title` as the
        key. `menuitem` will be converted to a `MenuItem` object if not one already.
        """
        self.__setitem__(self._choose_key, menuitem)

    def clear(self):
        """Remove all `MenuItem` objects from within the menu of this `MenuItem`."""
        self._menu.removeAllItems()
        super(Menu, self).clear()

    def copy(self):
        raise NotImplementedError

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        raise NotImplementedError

    def _set_subview_dimensions(self, menu, ele):
            # Ensure the item view spans the full width of the menu
            menu_width = max(menu._menu.size().width, 200)
            view = ele._menuitem.view()
            view_height = view.frame().size.height
            view.setFrameSize_((menu_width, view_height))

            # Give the subview (e.g. slider) 5% padding on each side
            subview = view.subviews()[0]
            subview.setFrame_(AppKit.NSMakeRect((menu_width - menu_width * 0.9) / 2, (view_height - view_height * 0.9) / 2, menu_width * 0.9, view_height * 0.9))

    def update(self, iterable, **kwargs):
        """Update with objects from `iterable` after each is converted to a :class:`rumps.MenuItem`, ignoring
        existing keys. This update is a bit different from the usual ``dict.update`` method. It works recursively and
        will parse a variety of Python containers and objects, creating `MenuItem` object and submenus as necessary.

        If the `iterable` is an instance of :class:`rumps.MenuItem`, then add to the menu.

        Otherwise, for each element in the `iterable`,

            - if the element is a string or is not an iterable itself, it will be converted to a
              :class:`rumps.MenuItem` and the key will be its string representation.
            - if the element is a :class:`rumps.MenuItem` already, it will remain the same and the key will be its
              :attr:`rumps.MenuItem.title` attribute.
            - if the element is an iterable having a length of 2, the first value will be converted to a
              :class:`rumps.MenuItem` and the second will act as the submenu for that `MenuItem`
            - if the element is an iterable having a length of anything other than 2, a ``ValueError`` will be raised
            - if the element is a mapping, each key-value pair will act as an iterable having a length of 2

        """
        def parse_menu(iterable, menu, depth):
            if isinstance(iterable, MenuItem):
                menu.add(iterable)
                return

            for n, ele in enumerate(iteritems(iterable) if isinstance(iterable, collections_abc.Mapping) else iterable):

                # for mappings we recurse but don't drop down a level in the menu
                if not isinstance(ele, MenuItem) and isinstance(ele, collections_abc.Mapping):
                    parse_menu(ele, menu, depth)

                # any iterables other than strings and MenuItems
                elif not isinstance(ele, (string_types, MenuItem)) and isinstance(ele, collections_abc.Iterable):
                    try:
                        menuitem, submenu = ele
                    except TypeError:
                        raise ValueError('menu iterable element #{0} at depth {1} has length {2}; must be a single '
                                         'menu item or a pair consisting of a menu item and its '
                                         'submenu'.format(n, depth, len(tuple(ele))))
                    menuitem = MenuItem(menuitem)
                    menu.add(menuitem)
                    parse_menu(submenu, menuitem, depth+1)

                # menu item / could be visual separator where ele is None or separator
                else:
                    menu.add(ele)
                    if isinstance(ele, SliderMenuItem):
                        self._set_subview_dimensions(menu, ele)
        parse_menu(iterable, self, 0)
        parse_menu(kwargs, self, 0)

    # ListDict insertion methods
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def insert_after(self, existing_key, menuitem):
        """Insert a :class:`rumps.MenuItem` in the menu after the `existing_key`.

        :param existing_key: a string key for an existing `MenuItem` value.
        :param menuitem: an object to be added. It will be converted to a `MenuItem` if not one already.
        """
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 1)
        super(Menu, self).insert_after(existing_key, (key, menuitem))

    def insert_before(self, existing_key, menuitem):
        """Insert a :class:`rumps.MenuItem` in the menu before the `existing_key`.

        :param existing_key: a string key for an existing `MenuItem` value.
        :param menuitem: an object to be added. It will be converted to a `MenuItem` if not one already.
        """
        key, menuitem = self._process_new_menuitem(self._choose_key, menuitem)
        self._insert_helper(existing_key, key, menuitem, 0)
        super(Menu, self).insert_before(existing_key, (key, menuitem))

    def _insert_helper(self, existing_key, key, menuitem, pos):
        if existing_key == key:  # this would mess stuff up...
            raise ValueError('same key provided for location and insertion')
        existing_menuitem = self[existing_key]
        index = self._menu.indexOfItem_(existing_menuitem._menuitem)
        self._menu.insertItem_atIndex_(menuitem._menuitem, index + pos)
        if isinstance(menuitem, SliderMenuItem):
            self._set_subview_dimensions(self, menuitem)

    # Processing MenuItems
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _process_new_menuitem(self, key, value):
        if value is None or value is separator:
            value = SeparatorMenuItem()

        if not hasattr(value, '_menuitem'):
            value = MenuItem(value)

        if key is self._choose_key:
            if hasattr(value, 'title'):
                key = value.title
            else:
                cls = type(value)
                count = self._counts[cls] = self._counts.get(cls, 0) + 1
                key = '%s_%d' % (cls.__name__, count)

        if hasattr(value, 'title') and key != value.title:
            _log('WARNING: key {0} is not the same as the title of the corresponding MenuItem {1}; while this '
                 'would occur if the title is dynamically altered, having different names at the time of menu '
                 'creation may not be desired '.format(repr(key), repr(value.title)))

        return key, value


class MenuItem(Menu):
    """Represents an item within the application's menu.

    A :class:`rumps.MenuItem` is a button inside a menu but it can also serve as a menu itself whose elements are
    other `MenuItem` instances.

    Encapsulates and abstracts Objective-C NSMenuItem (and possibly a corresponding NSMenu as a submenu).

    A couple of important notes:

        - A new `MenuItem` instance can be created from any object with a string representation.
        - Attempting to create a `MenuItem` by passing an existing `MenuItem` instance as the first parameter will not
          result in a new instance but will instead return the existing instance.

    Remembers the order of items added to menu and has constant time lookup. Can insert new `MenuItem` object before or
    after other specified ones.

    .. note::
       When adding a `MenuItem` instance to a menu, the value of :attr:`title` at that time will serve as its key for
       lookup performed on menus even if the `title` changes during program execution.

    :param title: the name of this menu item. If not a string, will use the string representation of the object.
    :param callback: the function serving as callback for when a click event occurs on this menu item.
    :param key: the key shortcut to click this menu item. Must be a string or ``None``.
    :param icon: a path to an image. If set to ``None``, the current image (if any) is removed.
    :param dimensions: a sequence of numbers whose length is two, specifying the dimensions of the icon.
    :param template: a boolean, specifying template mode for a given icon (proper b/w display in dark menu bar)
    """

    # NOTE:
    # Because of the quirks of PyObjC, a class level dictionary **inside an NSObject subclass for 10.9.x** is required
    # in order to have callback_ be a @classmethod. And we need callback_ to be class level because we can't use
    # instances in setTarget_ method of NSMenuItem. Otherwise this would be much more straightforward like Timer class.
    #
    # So the target is always the NSApp class and action is always the @classmethod callback_ -- for every function
    # decorated with @clicked(...). All we do is lookup the MenuItem instance and the user-provided callback function
    # based on the NSMenuItem (the only argument passed to callback_).

    def __new__(cls, *args, **kwargs):
        if args and isinstance(args[0], MenuItem):  # can safely wrap MenuItem instances
            return args[0]
        return super(MenuItem, cls).__new__(cls, *args, **kwargs)

    def __init__(self, title, callback=None, key=None, icon=None, dimensions=None, template=None):
        if isinstance(title, MenuItem):  # don't initialize already existing instances
            return
        self._menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(text_type(title), None, '')
        self._menuitem.setTarget_(NSApp)
        self._menu = self._icon = None
        self.set_callback(callback, key)
        self._template = template
        self.set_icon(icon, dimensions, template)
        super(MenuItem, self).__init__()

    def __setitem__(self, key, value):
        if self._menu is None:
            self._menu = NSMenu.alloc().init()
            self._menuitem.setSubmenu_(self._menu)
        super(MenuItem, self).__setitem__(key, value)

    def __repr__(self):
        return '<{0}: [{1} -> {2}; callback: {3}]>'.format(type(self).__name__, repr(self.title), list(map(str, self)),
                                                           repr(self.callback))

    @property
    def title(self):
        """The text displayed in a menu for this menu item. If not a string, will use the string representation of the
        object.
        """
        return self._menuitem.title()

    @title.setter
    def title(self, new_title):
        new_title = text_type(new_title)
        self._menuitem.setTitle_(new_title)

    @property
    def icon(self):
        """The path to an image displayed next to the text for this menu item. If set to ``None``, the current image
        (if any) is removed.

        .. versionchanged:: 0.2.0
           Setting icon to ``None`` after setting it to an image will correctly remove the icon. Returns the path to an
           image rather than exposing a `PyObjC` class.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        self.set_icon(icon_path, template=self._template)

    @property
    def template(self):
        """Template mode for an icon. If set to ``None``, the current icon (if any) is displayed as a color icon.
        If set to ``True``, template mode is enabled and the icon will be displayed correctly in dark menu bar mode.
        """
        return self._template

    @template.setter
    def template(self, template_mode):
        self._template = template_mode
        self.set_icon(self.icon, template=template_mode)

    def set_icon(self, icon_path, dimensions=None, template=None):
        """Sets the icon displayed next to the text for this menu item. If set to ``None``, the current image (if any)
        is removed. Can optionally supply `dimensions`.

        .. versionchanged:: 0.2.0
           Setting `icon` to ``None`` after setting it to an image will correctly remove the icon. Passing `dimensions`
           a sequence whose length is not two will no longer silently error.

        :param icon_path: a file path to an image.
        :param dimensions: a sequence of numbers whose length is two.
        :param template: a boolean who defines the template mode for the icon.
        """
        new_icon = _nsimage_from_file(icon_path, dimensions, template) if icon_path is not None else None
        self._icon = icon_path
        self._menuitem.setImage_(new_icon)

    @property
    def state(self):
        """The state of the menu item. The "on" state is symbolized by a check mark. The "mixed" state is symbolized
        by a dash.

        .. table:: Setting states

           =====  ======
           State  Number
           =====  ======
            ON      1
            OFF     0
           MIXED   -1
           =====  ======

        """
        return self._menuitem.state()

    @state.setter
    def state(self, new_state):
        self._menuitem.setState_(new_state)

    @property
    def hidden(self):
        """Indicates whether the menu item is hidden.

        .. versionadded:: 0.4.0

        """
        return self._menuitem.isHidden()

    @hidden.setter
    def hidden(self, value):
        self._menuitem.setHidden_(value)

    def hide(self):
        """Hide the menu item.

        .. versionadded:: 0.4.0

        """
        self.hidden = True

    def show(self):
        """Show the menu item.

        .. versionadded:: 0.4.0

        """
        self.hidden = False

    def set_callback(self, callback, key=None):
        """Set the function serving as callback for when a click event occurs on this menu item. When `callback` is
        ``None``, it will disable the callback function and grey out the menu item. If `key` is a string, set as the
        key shortcut. If it is ``None``, no adjustment will be made to the current key shortcut.

        .. versionchanged:: 0.2.0
           Allowed passing ``None`` as both `callback` and `key`. Additionally, passing a `key` that is neither a
           string nor ``None`` will result in a standard ``TypeError`` rather than various, uninformative `PyObjC`
           internal errors depending on the object.

        :param callback: the function to be called when the user clicks on this menu item.
        :param key: the key shortcut to click this menu item.
        """
        _internal.require_string_or_none(key)
        if key is not None:
            self._menuitem.setKeyEquivalent_(key)
        NSApp._ns_to_py_and_callback[self._menuitem] = self, callback
        self._menuitem.setAction_('callback:' if callback is not None else None)

    @property
    def callback(self):
        """Return the current callback function.

        .. versionadded:: 0.2.0

        """
        return NSApp._ns_to_py_and_callback[self._menuitem][1]

    @property
    def key(self):
        """The key shortcut to click this menu item.

        .. versionadded:: 0.2.0

        """
        return self._menuitem.keyEquivalent()


class SliderMenuItem(object):
    """Represents a slider menu item within the application's menu.

    .. versionadded:: 0.3.0

    :param value: a number for the current position of the slider.
    :param min_value: a number for the minimum position to which a slider can be moved.
    :param max_value: a number for the maximum position to which a slider can be moved.
    :param callback: the function serving as callback for when a slide event occurs on this menu item.
    :param dimensions: a sequence of numbers whose length is two, specifying the dimensions of the slider.
    """

    def __init__(self, value=50, min_value=0, max_value=100, callback=None, dimensions=(180, 15)):
        self._view = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 0, 30))
        self._slider = NSSlider.alloc().init()
        self._slider.setMinValue_(min_value)
        self._slider.setMaxValue_(max_value)
        self._slider.setDoubleValue_(value)
        self._slider.setFrameSize_(NSSize(*dimensions))
        self._slider.setTarget_(NSApp)
        self._menuitem = NSMenuItem.alloc().init()
        self._menuitem.setTarget_(NSApp)
        self._view.addSubview_(self._slider)
        self._menuitem.setView_(self._view)
        self.set_callback(callback)

    def __repr__(self):
        return '<{0}: [value: {1}; callback: {2}]>'.format(
            type(self).__name__,
            self.value,
            repr(self.callback)
        )

    def set_callback(self, callback):
        """Set the function serving as callback for when a slide event occurs on this menu item.

        :param callback: the function to be called when the user drags the marker on the slider.
        """
        NSApp._ns_to_py_and_callback[self._slider] = self, callback
        self._slider.setAction_('callback:' if callback is not None else None)

    @property
    def callback(self):
        return NSApp._ns_to_py_and_callback[self._slider][1]

    @property
    def value(self):
        """The current position of the slider."""
        return self._slider.doubleValue()

    @value.setter
    def value(self, new_value):
        self._slider.setDoubleValue_(new_value)


class SeparatorMenuItem(object):
    """Visual separator between :class:`rumps.MenuItem` objects in the application menu."""
    def __init__(self):
        self._menuitem = NSMenuItem.separatorItem()


class Timer(object):
    """
    Python abstraction of an Objective-C event timer in a new thread for application. Controls the callback function,
    interval, and starting/stopping the run loop.

    .. versionchanged:: 0.2.0
       Method `__call__` removed.

    :param callback: Function that should be called every `interval` seconds. It will be passed this
                     :class:`rumps.Timer` object as its only parameter.
    :param interval: The time in seconds to wait before calling the `callback` function.
    """
    def __init__(self, callback, interval):
        self.set_callback(callback)
        self._interval = interval
        self._status = False

    def __repr__(self):
        return ('<{0}: [callback: {1}; interval: {2}; '
                'status: {3}]>').format(type(self).__name__, repr(getattr(self, '*callback').__name__),
                                        self._interval, 'ON' if self._status else 'OFF')

    @property
    def interval(self):
        """The time in seconds to wait before calling the :attr:`callback` function."""
        return self._interval  # self._nstimer.timeInterval() when active but could be inactive

    @interval.setter
    def interval(self, new_interval):
        if self._status:
            if abs(self._nsdate.timeIntervalSinceNow()) >= self._nstimer.timeInterval():
                self.stop()
                self._interval = new_interval
                self.start()
        else:
            self._interval = new_interval

    @property
    def callback(self):
        """The current function specified as the callback."""
        return getattr(self, '*callback')

    def is_alive(self):
        """Whether the timer thread loop is currently running."""
        return self._status

    def start(self):
        """Start the timer thread loop."""
        if not self._status:
            self._nsdate = NSDate.date()
            self._nstimer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
                self._nsdate, self._interval, self, 'callback:', None, True)
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._nstimer, NSDefaultRunLoopMode)
            _TIMERS[self] = None
            self._status = True

    def stop(self):
        """Stop the timer thread loop."""
        if self._status:
            self._nstimer.invalidate()
            del self._nstimer
            del self._nsdate
            self._status = False

    def set_callback(self, callback):
        """Set the function that should be called every :attr:`interval` seconds. It will be passed this
        :class:`rumps.Timer` object as its only parameter.
        """
        setattr(self, '*callback', callback)

    def callback_(self, _):
        _log(self)
        try:
            return _internal.call_as_function_or_method(getattr(self, '*callback'), self)
        except Exception:
            traceback.print_exc()


class Window(object):
    """Generate a window to consume user input in the form of both text and button clicked.

    .. versionchanged:: 0.2.0
        Providing a `cancel` string will set the button text rather than only using text "Cancel". `message` is no
        longer a required parameter.

    .. versionchanged:: 0.3.0
        Add `secure` text input field functionality.

    :param message: the text positioned below the `title` in smaller font. If not a string, will use the string
                    representation of the object.
    :param title: the text positioned at the top of the window in larger font. If not a string, will use the string
                  representation of the object.
    :param default_text: the text within the editable textbox. If not a string, will use the string representation of
                         the object.
    :param ok: the text for the "ok" button. Must be either a string or ``None``. If ``None``, a default
               localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button will have that text. If `cancel`
                   evaluates to ``True``, will create a button with text "Cancel". Otherwise, this button will not be
                   created.
    :param dimensions: the size of the editable textbox. Must be sequence with a length of 2.
    :param secure: should the text field be secured or not. With ``True`` the window can be used for passwords.
    """

    def __init__(self, message='', title='', default_text='', ok=None, cancel=None, dimensions=(320, 160),
                 secure=False):
        message = text_type(message)
        message = message.replace('%', '%%')
        title = text_type(title)

        self._cancel = bool(cancel)
        self._icon = None

        _internal.require_string_or_none(ok)
        if not isinstance(cancel, string_types):
            cancel = 'Cancel' if cancel else None

        self._alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
            title, ok, cancel, None, message)
        self._alert.setAlertStyle_(0)  # informational style

        if secure:
            self._textfield = SecureEditing.alloc().initWithFrame_(NSMakeRect(0, 0, *dimensions))
        else:
            self._textfield = Editing.alloc().initWithFrame_(NSMakeRect(0, 0, *dimensions))
        self._textfield.setSelectable_(True)
        self._alert.setAccessoryView_(self._textfield)

        self.default_text = default_text

    @property
    def title(self):
        """The text positioned at the top of the window in larger font. If not a string, will use the string
        representation of the object.
        """
        return self._alert.messageText()

    @title.setter
    def title(self, new_title):
        new_title = text_type(new_title)
        self._alert.setMessageText_(new_title)

    @property
    def message(self):
        """The text positioned below the :attr:`title` in smaller font. If not a string, will use the string
        representation of the object.
        """
        return self._alert.informativeText()

    @message.setter
    def message(self, new_message):
        new_message = text_type(new_message)
        self._alert.setInformativeText_(new_message)

    @property
    def default_text(self):
        """The text within the editable textbox. An example would be

            "Type your message here."

        If not a string, will use the string representation of the object.
        """
        return self._default_text

    @default_text.setter
    def default_text(self, new_text):
        new_text = text_type(new_text)
        self._default_text = new_text
        self._textfield.setStringValue_(new_text)

    @property
    def icon(self):
        """The path to an image displayed for this window. If set to ``None``, will default to the icon for the
        application using :attr:`rumps.App.icon`.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will correctly be changed to the application
           icon.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = _nsimage_from_file(icon_path) if icon_path is not None else None
        self._icon = icon_path
        self._alert.setIcon_(new_icon)

    def add_button(self, name):
        """Create a new button.

        .. versionchanged:: 0.2.0
           The `name` parameter is required to be a string.

        :param name: the text for a new button. Must be a string.
        """
        _internal.require_string(name)
        self._alert.addButtonWithTitle_(name)

    def add_buttons(self, iterable=None, *args):
        """Create multiple new buttons.

        .. versionchanged:: 0.2.0
           Since each element is passed to :meth:`rumps.Window.add_button`, they must be strings.

        """
        if iterable is None:
            return
        if isinstance(iterable, string_types):
            self.add_button(iterable)
        else:
            for ele in iterable:
                self.add_button(ele)
        for arg in args:
            self.add_button(arg)

    def run(self):
        """Launch the window. :class:`rumps.Window` instances can be reused to retrieve user input as many times as
        needed.

        :return: a :class:`rumps.rumps.Response` object that contains the text and the button clicked as an integer.
        """
        _log(self)
        if NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle') == 'Dark':
            self._alert.window().setAppearance_(AppKit.NSAppearance.appearanceNamed_('NSAppearanceNameVibrantDark'))
        clicked = self._alert.runModal() % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text  # reset default text
        return Response(clicked, text)


class Response(object):
    """Holds information from user interaction with a :class:`rumps.Window` after it has been closed."""

    def __init__(self, clicked, text):
        self._clicked = clicked
        self._text = text

    def __repr__(self):
        shortened_text = self._text if len(self._text) < 21 else self._text[:17] + '...'
        return '<{0}: [clicked: {1}, text: {2}]>'.format(type(self).__name__, self._clicked, repr(shortened_text))

    @property
    def clicked(self):
        """Return a number representing the button pressed by the user.

        The "ok" button will return ``1`` and the "cancel" button will return ``0``. This makes it convenient to write
        a conditional like,

        .. code-block:: python

            if response.clicked:
                do_thing_for_ok_pressed()
            else:
                do_thing_for_cancel_pressed()

        Where `response` is an instance of :class:`rumps.rumps.Response`.

        Additional buttons added using methods :meth:`rumps.Window.add_button` and :meth:`rumps.Window.add_buttons`
        will return ``2``, ``3``, ... in the order they were added.
        """
        return self._clicked

    @property
    def text(self):
        """Return the text collected from the user."""
        return self._text


class NSApp(NSObject):
    """Objective-C delegate class for NSApplication. Don't instantiate - use App instead."""

    _ns_to_py_and_callback = {}

    def userNotificationCenter_didActivateNotification_(self, notification_center, notification):
        notifications._clicked(notification_center, notification)

    def initializeStatusBar(self):
        self.nsstatusitem = NSStatusBar.systemStatusBar().statusItemWithLength_(-1)  # variable dimensions
        self.nsstatusitem.setHighlightMode_(True)

        self.setStatusBarIcon()
        self.setStatusBarTitle()

        mainmenu = self._app['_menu']
        quit_button = self._app['_quit_button']
        if quit_button is not None:
            quit_button.set_callback(quit_application)
            mainmenu.add(quit_button)
        else:
            _log('WARNING: the default quit button is disabled. To exit the application gracefully, another button '
                 'should have a callback of quit_application or call it indirectly.')
        self.nsstatusitem.setMenu_(mainmenu._menu)  # mainmenu of our status bar spot (_menu attribute is NSMenu)

    def showMenu(self):
        self.nsstatusitem.button().performClick_(None)

    def setStatusBarTitle(self):
        self.nsstatusitem.setTitle_(self._app['_title'])
        self.fallbackOnName()

    def setStatusBarIcon(self):
        self.nsstatusitem.setImage_(self._app['_icon_nsimage'])
        self.fallbackOnName()

    def fallbackOnName(self):
        if not (self.nsstatusitem.title() or self.nsstatusitem.image()):
            self.nsstatusitem.setTitle_(self._app['_name'])

    def applicationDidFinishLaunching_(self, notification):
        workspace          = NSWorkspace.sharedWorkspace()
        notificationCenter = workspace.notificationCenter()
        notificationCenter.addObserver_selector_name_object_(
            self,
            self.receiveSleepNotification_,
            NSWorkspaceWillSleepNotification,
            None
        )
        notificationCenter.addObserver_selector_name_object_(
            self,
            self.receiveWakeNotification_,
            NSWorkspaceDidWakeNotification,
            None
        )

    def receiveSleepNotification_(self, ns_notification):
        _log('receiveSleepNotification')
        events.on_sleep.emit()

    def receiveWakeNotification_(self, ns_notification):
        _log('receiveWakeNotification')
        events.on_wake.emit()

    def applicationWillTerminate_(self, ns_notification):
        _log('applicationWillTerminate')
        events.before_quit.emit()

    @classmethod
    def callback_(cls, nsmenuitem):
        self, callback = cls._ns_to_py_and_callback[nsmenuitem]
        _log(self)
        try:
            return _internal.call_as_function_or_method(callback, self)
        except Exception:
            traceback.print_exc()


class App(object):
    """Represents the statusbar application.

    Provides a simple and pythonic interface for all those long and ugly `PyObjC` calls. :class:`rumps.App` may be
    subclassed so that the application logic can be encapsulated within a class. Alternatively, an `App` can be
    instantiated and the various callback functions can exist at module level.

    .. versionchanged:: 0.2.0
       `name` parameter must be a string and `title` must be either a string or ``None``. `quit_button` parameter added.

    :param name: the name of the application.
    :param title: text that will be displayed for the application in the statusbar.
    :param icon: file path to the icon that will be displayed for the application in the statusbar.
    :param menu: an iterable of Python objects or pairs of objects that will be converted into the main menu for the
                 application. Parsing is implemented by calling :meth:`rumps.MenuItem.update`.
    :param quit_button: the quit application menu item within the main menu. If ``None``, the default quit button will
                        not be added.
    """

    # NOTE:
    # Serves as a setup class for NSApp since Objective-C classes shouldn't be instantiated normally.
    # This is the most user-friendly way.

    #: A serializer for notification data.  The default is pickle.
    serializer = pickle

    def __init__(self, name, title=None, icon=None, template=None, menu=None, quit_button='Quit'):
        _internal.require_string(name)
        self._name = name
        self._icon = self._icon_nsimage = self._title = None
        self._template = template
        self.icon = icon
        self.title = title
        self.quit_button = quit_button
        self._menu = Menu()
        if menu is not None:
            self.menu = menu
        self._application_support = application_support(self._name)

    # Properties
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @property
    def name(self):
        """The name of the application. Determines the application support folder name. Will also serve as the title
        text of the application if :attr:`title` is not set.
        """
        return self._name

    @property
    def title(self):
        """The text that will be displayed for the application in the statusbar. Can be ``None`` in which case the icon
        will be used or, if there is no icon set the application text will fallback on the application :attr:`name`.

        .. versionchanged:: 0.2.0
           If the title is set then changed to ``None``, it will correctly be removed. Must be either a string or
           ``None``.

        """
        return self._title

    @title.setter
    def title(self, title):
        _internal.require_string_or_none(title)
        self._title = title
        try:
            self._nsapp.setStatusBarTitle()
        except AttributeError:
            pass

    @property
    def icon(self):
        """A path to an image representing the icon that will be displayed for the application in the statusbar.
        Can be ``None`` in which case the text from :attr:`title` will be used.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will correctly be removed.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = _nsimage_from_file(icon_path, template=self._template) if icon_path is not None else None
        self._icon = icon_path
        self._icon_nsimage = new_icon
        try:
            self._nsapp.setStatusBarIcon()
        except AttributeError:
            pass

    @property
    def template(self):
        """Template mode for an icon. If set to ``None``, the current icon (if any) is displayed as a color icon.
        If set to ``True``, template mode is enabled and the icon will be displayed correctly in dark menu bar mode.
        """
        return self._template

    @template.setter
    def template(self, template_mode):
        self._template = template_mode
        # resetting the icon to apply template setting
        self.icon = self._icon

    @property
    def menu(self):
        """Represents the main menu of the statusbar application. Setting `menu` works by calling
        :meth:`rumps.MenuItem.update`.
        """
        return self._menu

    @menu.setter
    def menu(self, iterable):
        self._menu.update(iterable)

    @property
    def quit_button(self):
        """The quit application menu item within the main menu. This is a special :class:`rumps.MenuItem` object that
        will both replace any function callback with :func:`rumps.quit_application` and add itself to the end of the
        main menu when :meth:`rumps.App.run` is called. If set to ``None``, the default quit button will not be added.

        .. warning::
           If set to ``None``, some other menu item should call :func:`rumps.quit_application` so that the
           application can exit gracefully.

        .. versionadded:: 0.2.0

        """
        return self._quit_button

    @quit_button.setter
    def quit_button(self, quit_text):
        if quit_text is None:
            self._quit_button = None
        else:
            self._quit_button = MenuItem(quit_text)

    # Show status item
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def showMenu(self):
        self._nsapp.showMenu()

    # Open files in application support folder
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def open(self, *args):
        """Open a file within the application support folder for this application.

        .. code-block:: python

            app = App('Cool App')
            with app.open('data.json') as f:
                pass

        Is a shortcut for,

        .. code-block:: python

            app = App('Cool App')
            filename = os.path.join(application_support(app.name), 'data.json')
            with open(filename) as f:
                pass

        """
        return open(os.path.join(self._application_support, args[0]), *args[1:])

    # Run the application
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self, **options):
        """Performs various setup tasks including creating the underlying Objective-C application, starting the timers,
        and registering callback functions for click events. Then starts the application run loop.

        .. versionchanged:: 0.2.1
            Accepts `debug` keyword argument.

        :param debug: determines if application should log information useful for debugging. Same effect as calling
                      :func:`rumps.debug_mode`.

        """
        dont_change = object()
        debug = options.get('debug', dont_change)
        if debug is not dont_change:
            debug_mode(debug)

        nsapplication = NSApplication.sharedApplication()
        nsapplication.activateIgnoringOtherApps_(True)  # NSAlerts in front
        self._nsapp = NSApp.alloc().init()
        self._nsapp._app = self.__dict__  # allow for dynamic modification based on this App instance
        nsapplication.setDelegate_(self._nsapp)
        notifications._init_nsapp(self._nsapp)

        setattr(App, '*app_instance', self)  # class level ref to running instance (for passing self to App subclasses)
        t = b = None
        for t in getattr(timer, '*timers', []):
            t.start()
        for b in getattr(clicked, '*buttons', []):
            b(self)  # we waited on registering clicks so we could pass self to access _menu attribute
        del t, b

        self._nsapp.initializeStatusBar()

        AppHelper.installMachInterrupt()
        events.before_start.emit()
        AppHelper.runEventLoop()



================================================
File: rumps/text_field.py
================================================
from AppKit import NSApplication, NSTextField, NSSecureTextField, NSKeyDown, NSCommandKeyMask


class Editing(NSTextField):
    """NSTextField with cut, copy, paste, undo and selectAll"""
    def performKeyEquivalent_(self, event):
        return _perform_key_equivalent(self, event)


class SecureEditing(NSSecureTextField):
    """NSSecureTextField with cut, copy, paste, undo and selectAll"""
    def performKeyEquivalent_(self, event):
        return _perform_key_equivalent(self, event)


def _perform_key_equivalent(self, event):
    if event.type() == NSKeyDown and event.modifierFlags() & NSCommandKeyMask:
        if event.charactersIgnoringModifiers() == "x":
            NSApplication.sharedApplication().sendAction_to_from_("cut:", None, self)
            return True
        elif event.charactersIgnoringModifiers() == "c":
            NSApplication.sharedApplication().sendAction_to_from_("copy:", None, self)
            return True
        elif event.charactersIgnoringModifiers() == "v":
            NSApplication.sharedApplication().sendAction_to_from_("paste:", None, self)
            return True
        elif event.charactersIgnoringModifiers() == "z":
            NSApplication.sharedApplication().sendAction_to_from_("undo:", None, self)
            return True
        elif event.charactersIgnoringModifiers() == "a":
            NSApplication.sharedApplication().sendAction_to_from_("selectAll:", None, self)
            return True



================================================
File: rumps/utils.py
================================================
# -*- coding: utf-8 -*-

"""
rumps.utils
~~~~~~~~~~~

Generic container classes and utility functions.

:copyright: (c) 2020 by Jared Suttles
:license: BSD-3-Clause, see LICENSE for details.
"""

from .packages.ordereddict import OrderedDict as _OrderedDict


# ListDict: OrderedDict subclass with insertion methods for modifying the order of the linked list in O(1) time
# https://gist.github.com/jaredks/6276032
class ListDict(_OrderedDict):
    def __insertion(self, link_prev, key_value):
        key, value = key_value
        if link_prev[2] != key:
            if key in self:
                del self[key]
            link_next = link_prev[1]
            self._OrderedDict__map[key] = link_prev[1] = link_next[0] = [link_prev, link_next, key]
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key][0], key_value)



================================================
File: rumps/packages/__init__.py
================================================



================================================
File: rumps/packages/ordereddict.py
================================================
# Backport of OrderedDict() class that runs on Python 2.4, 2.5, 2.6, 2.7 and pypy.
# Passes Python2.7's test suite and incorporates all the latest updates.
# Copyright 2009 Raymond Hettinger, released under the MIT License.
# http://code.activestate.com/recipes/576693/
try:
    from thread import get_ident as _get_ident
except ImportError:
    try:
        from dummy_thread import get_ident as _get_ident
    except ImportError:
        from threading import get_ident as _get_ident

try:
    from _abcoll import KeysView, ValuesView, ItemsView
except ImportError:
    pass


class OrderedDict(dict):
    'Dictionary that remembers insertion order'
    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as for regular dictionaries.

    # The internal self.__map dictionary maps keys to links in a doubly linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        '''
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []                     # sentinel node
            root[:] = [root, root, None]
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        dict_delitem(self, key)
        link_prev, link_next, key = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        try:
            for node in self.__map.values():
                del node[:]
            root = self.__root
            root[:] = [root, root, None]
            self.__map.clear()
        except AttributeError:
            pass
        dict.clear(self)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root[0]
            link_prev = link[0]
            link_prev[1] = root
            root[0] = link_prev
        else:
            link = root[1]
            link_next = link[1]
            root[1] = link_next
            link_next[0] = root
        key = link[2]
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    # -- the following methods do not depend on the internal structure --

    def keys(self):
        'od.keys() -> list of keys in od'
        return list(self)

    def values(self):
        'od.values() -> list of values in od'
        return [self[key] for key in self]

    def items(self):
        'od.items() -> list of (key, value) pairs in od'
        return [(key, self[key]) for key in self]

    def iterkeys(self):
        'od.iterkeys() -> an iterator over the keys in od'
        return iter(self)

    def itervalues(self):
        'od.itervalues -> an iterator over the values in od'
        for k in self:
            yield self[k]

    def iteritems(self):
        'od.iteritems -> an iterator over the (key, value) items in od'
        for k in self:
            yield (k, self[k])

    def update(*args, **kwds):
        '''od.update(E, **F) -> None.  Update od from dict/iterable E and F.

        If E is a dict instance, does:           for k in E: od[k] = E[k]
        If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
        Or if E is an iterable of items, does:   for k, v in E: od[k] = v
        In either case, this is followed by:     for k, v in F.items(): od[k] = v

        '''
        if len(args) > 2:
            raise TypeError('update() takes at most 2 positional '
                            'arguments (%d given)' % (len(args),))
        elif not args:
            raise TypeError('update() takes at least 1 argument (0 given)')
        self = args[0]
        # Make progressively weaker assumptions about "other"
        other = ()
        if len(args) == 2:
            other = args[1]
        if isinstance(other, dict):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, 'keys'):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwds.items():
            self[key] = value

    __update = update  # let subclasses override update without breaking __init__

    __marker = object()

    def pop(self, key, default=__marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.

        '''
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    def __repr__(self, _repr_running={}):
        'od.__repr__() <==> repr(od)'
        call_key = id(self), _get_ident()
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        'Return state information for pickling'
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, OrderedDict):
            return len(self)==len(other) and self.items() == other.items()
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    # -- the following methods are only used in Python 2.7 --

    def viewkeys(self):
        "od.viewkeys() -> a set-like object providing a view on od's keys"
        return KeysView(self)

    def viewvalues(self):
        "od.viewvalues() -> an object providing a view on od's values"
        return ValuesView(self)

    def viewitems(self):
        "od.viewitems() -> a set-like object providing a view on od's items"
        return ItemsView(self)

