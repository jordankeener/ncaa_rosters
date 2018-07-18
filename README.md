# ncaa_rosters

Scrapes the name and hometown of all athletes for schools in the Power 5
conferences (Big Ten, Big 12, ACC, SEC, Pac-12) from rosters provided
by each school.

Rosters were scraped in July 2018 and correspond to the roster posted on
each schools athletics website at that time. This is generally the roster
for the 2017-2018 academic year, although some fall sports already had the
2018 roster posted.

The files that scrape the raw roster data are in the 'code' directory.
Each file is named according to the school it scrapes, and it outputs
a .csv file to the output folder with all of the school's roster data.
These files have been maintained to match the layout of each school's athletics
website as of 7/17/2018.

Under the 'code' directory, there is subdirectory called 'clean'. This contains
Stata do-files that clean the raw roster data and combines the schools
to make a complete, standardized dataset. The cleaned datasets are in
the 'output/cleaned' subdirectory.

Running '\_build_ncca_rosters.py' in the code subdirectory will run each
scraping file and main data cleaning do-file.

The final datasets have been cleaned pretty extensively, but still undoubtedly
contain errors. For example, right now the previous school variable mostly contains the
athlete's high school when it is not missing, but other times may show the last
college they played for or, for some of the more unstructured online rosters,
something completely unrelated.

I am working on additional data processing to match player's
hometowns to other geographic variables and previous schools to public high
schools in the United States, but I am not making these publicly available at
this stage of the project.

This project is licensed under the terms of the MIT license.

-- Jordan Keener - Kellogg School of Management, Northwestern University
