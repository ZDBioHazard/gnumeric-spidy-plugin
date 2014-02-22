============================
GW2Spidy Plugin for Gnumeric
============================

So, what is this?
=================

This Python_ plugin for Gnumeric_ provides a way to fetch `Guild Wars 2`_
item data from the GW2Spidy_ web API and store it in a specially named and
formatted sheet for use in your calculations.

.. _Python: http://www.python.org/
.. _Gnumeric: http://projects.gnome.org/gnumeric/
.. _`Guild Wars 2`: http://www.guildwars2.com/
.. _GW2Spidy: http://www.gw2spidy.com/

Installation
============

Just drop the ``spidy/`` folder in your Gnumeric plugins directory [1]_,
enable it in the Gnumeric plugins interface, and there you go.

Someday I'll figure out how to use setuptools so EasyInstall_ or PIP_
or whatever can install it the new-fangled way. ;P

.. _EasyInstall: https://pypi.python.org/pypi/setuptools
.. _PIP: http://www.pip-installer.org

.. [1] Usually ``~/.gnumeric/<version>/plugins``

How to use this plugin
======================

To get started using this GW2Spidy plugin with your spreadsheet, a special
"Spidy sheet" must be created.

Using the "Update GW2Spidy Data" command in the "Data -> Get External Data"
menu will create an empty "Spidy sheet" for you if it does not exist.

The "Spidy sheet" looks like this:

======== ============== ===== ======
   ID         Name       Buy   Sell
======== ============== ===== ======
  19699   Iron Ore       181    203
  19702   Platinum Ore   192    197
  19700   Mithril Ore     37     38
======== ============== ===== ======

The column headers use a special function called ``spidy_col(str,str)`` which
is called with two string arguments: ``display``, which is simply the text
that will be displayed in the cell, and ``field``, which corresponds to an item
data field in a `GW2Spidy Item Data API`_ response dictionary.

You must include a ``data_id`` column.

When this plugin creates a new "Spidy sheet" for you, it will have some
predefined columns you can take a look at.

.. _GW2Spidy Item Data API:
   https://github.com/rubensayshi/gw2spidy/wiki/API-v0.9#wiki-item-data

Once you have your ``spidy_col()`` columns set-up, all you have to do is input
GW2Spidy item IDs [2]_ into the ``data_id`` column of your Spidy table, and the
other information will be fetched from GW2Spidy automatically the next time you
use "Update GW2Spidy Data".

.. note:: Whenever you update the GW2Spidy data, you will likely need to
          manually recalculate the workbook. This can be done by selecting
          "Recalculate" from the "Edit" menu, or by simply pressing ``F9``.

.. [2] The item ID can be found by looking at the end of an item URL on
       the GW2Spidy website, such as ``http://gw2spidy.com/item/19700``

Limitations
===========

I'm not aware of any way to get the plugin to query data in a background
thread, and all items are refreshed synchronously, so if you have a lot
of items to refresh, the UI can hang for a very surprising amount of time
until it's finished. I'll see if I can at least get some sort of progress
dialog working at some point.
