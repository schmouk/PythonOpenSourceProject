# Sub-project PostgreSQL

This document explains what are the library and tools that must be downloaded and installed to be able to use our related Open Source code.


## PostgreSQL
This open source object-relational database system gets a nice Web site at [www.postgresql.org/](https://www.postgresql.org/).

Downloads are easily available at [www.postgresql.org/download/}(https://www.postgresql.org/download/). Installation is then easy once you've downloaded an installer.

The source code is available here: [git.postgresql.org/gitweb](https://git.postgresql.org/gitweb/?p=postgresql.git;a=summary) and instruction for its building are available in the documentation. This is not the way we recommend to install PostgreSQL, unless you're a pro.


## Psycopg2
This GNU Lesser General Public License code is a Python adapter to PostgreSQL. We will use it to develop code that uses PostgreSQL.
Their Web site is [https://www.psycopg.org/](https://www.psycopg.org/). To download and install this library, open a console window and just type

    > pip install psycopg2
    
If this does not work properly, have a look at [https://www.psycopg.org/docs/install.html](https://www.psycopg.org/docs/install.html).


## That's it!
Up today, nothing more is mandatory to play our code.
