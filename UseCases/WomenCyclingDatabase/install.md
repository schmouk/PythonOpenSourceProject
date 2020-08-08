# Women Cycling Database

Installation instructions for the mandatory external libraries.

## `pylightxl`
The collected data containing results, calendars and teams (names, compositions) come from the official UCI web site. They are provided as Excel files. To be able to prepare these data before their parsing, we expect to get them in a CSV format. The Microsoft  Excel application allows for the export of XLS sheets to `.csv` files, but this is too much tedious to do by hand, one file after the other. So, for the sole purpose of the automation of the transformation of data format, from XLS to CSV, we developed a small script and take benefit of external library `pylightxl`.

To be able to run this script, you must install this external library in your Python environment. In a console window, whatever your preferred Operating System, just type:

    > pip -install pylightxl

or, if this doesn't work, just type:

    > python -m pip install pylightxl

## That's it!
Up today, there is no other external library that is mandatory for use case `WomenCyclingDatabase`.