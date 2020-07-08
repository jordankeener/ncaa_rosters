# ncaa_rosters

Scrapes the name and hometown of all athletes for schools in the Power 5
conferences (Big Ten, Big 12, ACC, SEC, Pac-12) from rosters provided
by each school.

Rosters were scraped on October 18, 2018 and from rosters posted on
each school's athletics website at that time. This in general should be the roster
for the 2018-2019 academic year, although for some spring sports at some schools 
it may still be the team from 2017-2018.

The files that scrape the raw roster data are in the 'code' directory.
Each file is named according to the school it scrapes, and it outputs
a csv file to the output folder with all of the school's roster data.
These files have been maintained to match the layout of each school's athletics
website as of 10/18/2018.

Under the 'code' directory, there is subdirectory called 'clean'. This contains
Stata do-files that clean the raw roster data and combines the schools
to make a complete, standardized dataset. The cleaned datasets are in
the 'output/cleaned' subdirectory.

Running '\_build_ncca_rosters.py' in the code subdirectory will run each
scraping file and main data cleaning do-file.

The final datasets have been cleaned pretty extensively, but still may
contain errors. For example, right now the previous school variable mostly contains the
athlete's high school when it is not missing, but other times may show the last
college they played for or, for some of the less structured online rosters,
something completely unrelated.

This data was collected for the paper "Who Profits from Amateurism? Rent-Sharing in Modern College Athletics", 
which is joint work with Craig Garthwaite, Matt Notowidigdo, and Nicole Ozminkowski. 

This project is licensed under the terms of the MIT license.

-- Jordan Keener
