# ObjectSqlLib

This package contains libraries which relate to Object Oriented Programming of SQL relational databases (DB).

Notice: some of the listed sub-package below are not currently under development and will be implemented later.


## ObjectSqlInterface
This is a generic interface for every library that relates to SQL Databases. It conforms to PEP 249 -- Python Database API Specification v2.0. See [https://www.python.org/dev/peps/pep-0249/](https://www.python.org/dev/peps/pep-0249/).

It will finally be part of further project **PySqlLib**.


## PyPostgreSQLLib
This package implements interface `ObjectSqlInterface`.  
It is an OOP implementation that uses library `psycopg2` - [https://www.psycopg.org/](https://www.psycopg.org/).

It will finally be part of further project **PySqlLib**.


## PySQLiteLib
This package implemenst interface `ObjectSqlInterface`.  
It is an OOP implementation that uses built-in library `sqlite3`.

It will finally be part of further project **PySqlLib**.
