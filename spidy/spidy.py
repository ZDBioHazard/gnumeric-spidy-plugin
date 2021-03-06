"""GW2Spidy Gnumeric plugin
This Python plugin for Gnumeric provides a way to fetch Guild Wars 2
item data from the GW2Spidy web API and store it in a specially named
and formatted sheet for use in your calculations.

For help installing or using this plugin, check out the README.rst file.

COPYRIGHT INFO

By Ryan "BioHazard" Turner <zdbiohazard2@gmail.com>
Copyright (c) 2013

LICENSE

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>

"""

import urllib2
import json
import re


def spidy_update(gui):
    """Update the "Spidy" sheet with fresh data."""
    url = "http://www.gw2spidy.com/api/v0.9/json/item/"

    # Try to find a sheet named "Spidy".
    for sheet in gui.get_workbook().sheets():
        if sheet.get_name_unquoted().lower() == "spidy":
            break
    else:  # Create a "Spidy" sheet if one isn't found.
        print("spidy: No \"Spidy\" sheet. Creating one.")
        sheet = gui.get_workbook().sheet_add()
        sheet.rename("Spidy")

        # Create the default columns.
        for col, name in enumerate([("ID", 'data_id'), ("Name", 'name'),
                                    ("Buy", 'max_offer_unit_price'),
                                    ("Sell", 'min_sale_unit_price')]):
            sheet[col, 0].set_text('=spidy_col("%s", "%s")' % name)
        return  # This is an empty sheet, so there's no point updating it.

    # Find the data columns.
    cols = {}
    extent = sheet.get_extent()
    regex = re.compile(r'^=spidy_col\("(?:.+?)","(.+?)"\)$')
    for col in range(extent.start.col, extent.end.col + 1):
        match = regex.match(sheet[col, extent.start.row].get_entered_text())
        try:  # `match` might be NoneType, so catch AttributeError here too.
            cols[match.group(1).lower()] = col
        except (IndexError, AttributeError):
            pass  # Skip unknown columns so we can have a semi-freeform layout.

    # Make sure there's a 'data_id' column.
    # TODO: Pop-up some kind of error dialog.
    if 'data_id' not in cols:
        print("spidy: No data_id column found.")
        return

    # Iterate through the items and update them.
    # TODO: Spawn some kind of progress dialog, as this can take a while.
    for row in range(extent.start.row + 1, extent.end.row + 1):
        try:  # TODO: ID should be optional. Search by name otherwise.
            data_id = int(sheet[int(cols['data_id']), row].get_value())
        except (TypeError, ValueError) as error:
            print("spidy: Row %d has no ID: %r" % (row, error))
            continue

        try:  # Oh so many things that can go wrong here. >.>
            print("spidy: Fetching item #%d" % (data_id))
            data = json.load(urllib2.urlopen(url + str(data_id)))['result']
        except (urllib2.HTTPError, ValueError, KeyError) as error:
            print("spidy: Error fetching %d: [%d] %r" % (row, data_id, error))
            continue

        # Put the loaded data into the cells.
        for key, col in cols.items():
            sheet[col, row].set_text(str(data.get(key, "Unknown")))


def spidy_col(display, field):
    ("""@GNM_FUNC_HELP_NAME@SPIDY_COL:Define a GW2Spidy data colmun.\n"""
     """@GNM_FUNC_HELP_ARG@display:Display this in this cell\n"""
     """@GNM_FUNC_HELP_ARG@field:GW2Spidy API data field\n"""
     """@GNM_FUNC_HELP_EXAMPLES@=SPIDY_COL('Buy', 'max_offer_unit_price')""")
    return display  # Wow, wasn't that easy? ;)


spidy_ui_actions = {'spidy_update': spidy_update}
spidy_functions = {'spidy_col': ('ss', 'display, field', spidy_col)}
