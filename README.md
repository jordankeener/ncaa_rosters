# ncaa_rosters

Scrapes the name and hometown of all athletes for schools in the Power 5
conferences (Big Ten, Big 12, ACC, SEC, Pac-12) from rosters provided
by each school.

Rosters were scraped in April/May 2018 and correspond to the roster posted on
each schools athletics website at that time. This is generally the roster
for the 2017-2018 academic year, although some fall sports already had the
2018 roster posted.

The files that scrape the raw roster data are in the 'code' directory.
Each file is named according to the school it scrapes, and it outputs
a .csv file to the output folder with all of the school's roster data.

Under the 'code' directory, there is subdirectory called 'clean'. This contains
Stata do-files that clean the raw roster data and combines the schools
to make a complete, standardized dataset. The cleaned datasets are in
the 'output/cleaned' subdirectory. Running clean.do is sufficient
to generate the cleaned dataset for all schools that have been
scraped according to the scrape log in the 'notes' subdirectory. 
