Document: sql_tables_structures.txt
Author: Schmouk
Revision: 0.1
Date: 2020-08-16



# Specification of tables structure for the PostgreSQL data base WomenCyclingDB


## 1. Rationale

Data has been downloaded from the UCI (*Union Cycliste Internationale*) official Web site and has been prepared to conform with CSV format.

From this whole data, we can now specify SQL tables structures that will contain this CSV data for it to be available for statistics use, data browsing and the like from the related DB (Data Base).


## 2. Data presentation

The downloaded data is present in directory `UseCases/WomenCyclingDatabase/data/RoadRaces`. It is split into three sub-directories:
- `Calendars`
- `Results`
- `Teams`

In each of these three sub-directories, data are grouped by year. Up today, the sole season 2020 is present in the data directory. This is far enough to play with our code.


## 3. SQL tables structures
These tables structures are a result of the analysis of the CSV files content.

Remember, we currently deal with the sole elite women road races. Meanwhile, we introduce `rr` and `we` in table names as often as possible. This way, it should be easy to later extend the database to elite men road races, to U23 women and men road races, to junior woment and mes road races, and to track races, VTT, BMX, etc.

### 3.1 Calendars
The CSV header of data is :

    Date From,Date To,Name,Venue,Country,Category,Calendar,Class,EMail,WebSite

In the CSV files:
- `Date To` may be the same as `Date From` which means that the road race is organized on a single day.
- `Venue` may be empty, as may be `Calendar`, `EMail` and `WebSite`.
- we do not store `Calendar`, `EMail` and `WebSite` data - no use for them here.

	CREATE TABLE calendar_rr_we (
	    id          SERIAL        PRIMARY KEY,
	    year        integer       NOT NULL,
	    name        varchar(126)  NOT NULL,
	    day         date          NOT NULL,
	    day_end     date,
	    venue       varchar(62),
	    country_id  char(4)       REFERENCES uci_members(id) NOT NULL,
	    category    char(4)       NOT NULL, 
	    class       char(8)       NOT NULL
	);
	
	CREATE INDEX calendar_we_ndx ON calendar_we {
	    name, year
	};

### 3.2 Countries - UCI members
These are the 'members' of the UCI.

	CREATE TABLE uci_members {
	    id              char(4)      PRIMARY KEY,
	    continental_id  smallint     REFERENCES uci_continents(id) NOT NULL,
	    name            varchar(56)  NOT NULL
	}

### 3.3 Continental Federations affiliated to the UCI

    CREATE TABLE uci_continents {
        id   char(8)      PRIMARY KEY,
        name varchar(54)  NOT NULL
    }

### 3.4 Results

    CREATE TABLE results_rr_we {
        race_id            integer   NOT NULL REFERENCES calendar_rr_we(id),
        classification_id  char(4)   NOT NULL REFERENCES classification_types_rr(id),
        ranking            smallint,
        bib                smallint  NOT NULL REFERENCES start_lists_rr_we(bib),
        we_cyclist_id      integer   NOT NULL REFERENCES cyclists_we(id),
        result             char(8)
    }
    
    CREATE INDEX cyclists_rr_we_ndx ON results_rr_we {
        we_cyclist_id
    }
    
    CREATE INDEX races_rr_we_ndx ON results_rr_we {
        race_id, classification_id
    }
    
    
    CREATE TABLE classification_types_rr {
        id    char(4)      NOT NULL UNIQUE,
        name  varchar(26)  NOT NULL
    }
    
### 3.5 Start lists

    CREATE TABLE start_lists_rr_we {
        race_id      integer   NOT NULL REFERENCES calendar_rr_we(id),
        team_id      integer   NOT NULL REFERENCES teams_we(id),
        bib          smallint  NOT NULL,
        cyclist_age  smallint,
        cyclist_id   integer   NOT NULL REFERENCES cyclists_we(id),
        PRIMARY KEY( race_id, bib )
    }

### 3.6 Teams
The CSV headr of data is:

    Code,Name,Team Category,Country,Continent,Format,Email,Website,,

We do not store format, e-mail and website data - no use for this use case.

    CREATE TABLE teams_we {
        id          SERIAL       PRIMARY KEY,
        code        char(4)      NOT NULL,
        name        varchar(58)  NOT NULL,
        categ       char(4)      NOT NULL REFERENCES teams_categories(categ),
        country_id  char(4)      NOT NULL REFERENCES uci_members(id),
        continent   char(4)
    }
    
    CREATE TABLE teams_categories {
        categ  char(4)      PRIMARY KEY,
        name   varchar(34)  NOT NULL
    }

### 3.7 Cyclists
Up today, stored information is extracted from results, not from teams compositions (which are harder to collect on the UCI web site).

    CREATE TABLE cyclists_we {
        id      SERIAL   PRIMARY KEY,
        f_name  varchar  NOT NULL,  -- caution: not limited varchar is a PostgreSQL extension
        l_name  varchar  NOT NULL,  -- caution: not limited varchar is a PostgreSQL extension
    }
    
    CREATE INDEX cyclsits_we_ndx ON cyclists_we {
        l_name
    }



## A. Appendix

See [www.postgresql.org/docs/](https://www.postgresql.org/docs) to access PostgrSQL full documentation

See [www.postgresql.org/docs/12/index.html](https://www.postgresql.org/docs/12/index.html) to get access to the documentation of version 12 of PostgreSQL, the one we are currently using, waiting for release 13 to be available.

See [www.postgresql.org/docs/12/datatype.html](https://www.postgresql.org/docs/12/datatype.html) to get access more specifically to PostgreSQL data types.



## History

0.1 - draft - Schmouk - 2020-08-16 - Creation.  
0.2 - draft - Schmouk - 2020-08-22 - Largely augmented section 3 - SQL tables structures.
