set more off
cap log close



global homedir "~/Documents/GitHub/ncaa_rosters"


global indata ${homedir}/output
global outdata ${homedir}/output/cleaned
global code ${homedir}/code/clean

cd "${code}"

log using clean.log", text replace


run ancillary_data/state_abbrevs.do
run _clean_functions.do


// clean raw roster data
******************************************************************************
// build local with schools and make schools dataset
import excel using ${homedir}/notes/schools.xlsx, clear firstrow
drop if missing(scrape_date)
gen dset = subinstr(filename, ".py", "", 1)
local schools ""
local N = _N
forvalues i = 1/`N' {
	local x = dset[`i']
	local schools = "`schools' `x'"
}

// make school summary dataset
rename school 	school_full_name
rename dset 	school
assert table + ul + grid == 1
gen scrape_type = "table" if table==1
replace scrape_type = "ul" if ul==1
replace scrape_type = "grid" if grid==1
local keepvars school school_full_name conference scrape_date football_url scrape_type
keep  `keepvars'
order `keepvars'

// school lists by scrape type
foreach stype in table ul grid {
	local schools_`stype' = ""
	forvalues i = 1/`N' {
		local is_`stype' = scrape_type[`i'] == "`stype'"
		if `is_`stype'' {
			local x = school[`i']
			local schools_`stype'= "`schools_`stype'' `x'"
		}
	}
	disp "`schools_`stype''"
}


la var school 				"College"
la var school_full_name 	"Full College Name"
la var conference 			"Conference"
la var scrape_date 			"Date rosters scraped"
la var football_url 		"URL of football roster"

rename school college
rename school_full_name college_full_name

export delimited using ${outdata}/schools.csv, replace
save ${outdata}/schools, replace

******************************************************************************
// loop through schools and combine by scrape type

foreach grp in table ul grid {
	clear
	tempfile `grp's
	local i = 0
	foreach school in `schools_`grp'' {
		import delimited using ${indata}/`school'_rosters.csv, clear varnames(1)
		cap drop v1

		if `i'>0 {
			append using ``grp's'
		}
		save ``grp's', replace

		local ++i

	}
}

// unordered lists - easy
use `uls', clear
replace highschool = "" if highschool == "N/A"
replace highschool = stritrim(highschool)
tempfile full
save `full'

// grids - easy
use `grids', clear
rename high_school highschool
assert !missing(highschool) & highschool != "N/A"
replace highschool = stritrim(highschool)
// fix sport name in cases where gender specified
replace sport = subinstr(sport, "mixed", "mens", 1) if gender == "Men"
replace sport = subinstr(sport, "mixed", "womens", 1) if gender == "Women"
drop gender
append using `full'
save `full', replace

// tables - harder but more structured
use `tables', clear
foreach v of varlist *text {
	replace `v' = upper(`v')
}
tab hometowntext
tab highschooltext
gen ht_hs_same = hometowntext == highschooltext
tab ht_hs_same

** basic cases
gen ht_clean = hometown if hometowntext == "HOMETOWN"
gen hs_clean = highschool if highschooltext == "HIGH SCHOOL"

replace ht_clean = strtrim(substr(hometown, strpos(hometown, "-") + 1, .)) ///
					if hometowntext == "LAST SCHOOL - HOMETOWN"

** hometown is always first other than the one above
local chr_list "(" "-" "/"
foreach chr in "`chr_list'" {
	replace ht_clean = strtrim(substr(hometown, 1, strpos(hometown, "`chr'")-1)) ///
		if missing(ht_clean) & strpos(hometowntext, "`chr'") != 0 & hometowntext != "N/A"

	replace ht_clean = hometown if strpos(hometowntext, "`chr'") > 0 & ///
		strpos(hometown, "`chr'") == 0 & missing(ht_clean)
}

** if hometown not in high school field, high school is always first
** same approach as with hometown above
local chr_list "(" "/"
foreach chr in "`chr_list'" {
	replace hs_clean = strtrim(substr(highschool, 1, strpos(highschool, "`chr'")-1)) ///
		if strpos(highschooltext, "HOMETOWN") == 0 & missing(hs_clean) & highschooltext != "N/A"

	replace hs_clean = highschool if strpos(highschooltext, "HOMETOWN") == 0 & ///
		missing(hs_clean) & highschooltext != "N/A" & ///
		strpos(highschool, "`chr'") == 0 & strpos(highschooltext, "`chr'") > 0
}

** cases where hometown and high school need to be separated
tempvar x
gen `x' = strpos(highschool, "(") + 1
replace hs_clean = strtrim(substr(highschool, `x', strlen(highschool) - `x')) ///
	if highschooltext == "HOMETOWN (HIGH SCHOOL)" & strpos(highschool, "(") > 0
drop `x'

tempvar x
gen `x' = strpos(highschool, "/") + 1
replace hs_clean = strtrim(substr(highschool, `x', .)) ///
	if inlist(highschooltext, "HOMETOWN / HIGH SCHOOL", "HOMETOWN/HIGH SCHOOL") & `x' > 1

** high school if between /
replace hs_clean = strtrim(substr(highschool, `x', strrpos(highschool, "/") - `x')) ///
	if strrpos(highschool, "/") > strpos(highschool, "/") & strrpos(highschool, "/") > 0 & ///
	inlist(highschooltext, "HOMETOWN/HIGH SCHOOL/COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/LAST COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/LAST SCHOOL", ///
						   "HOMETOWN/HIGH SCHOOL/PREV. COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/PREVIOUS COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/PREVIOUS SCHOOL")

** high school if no other/previous school
replace hs_clean = strtrim(substr(highschool, `x', .)) ///
	if strrpos(highschool, "/") == strpos(highschool, "/") & strrpos(highschool, "/") > 0 & ///
	inlist(highschooltext, "HOMETOWN/HIGH SCHOOL/COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/LAST COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/LAST SCHOOL", ///
						   "HOMETOWN/HIGH SCHOOL/PREV. COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/PREVIOUS COLLEGE", ///
						   "HOMETOWN/HIGH SCHOOL/PREVIOUS SCHOOL")
drop `x'


** now need to use "school" field where highschooltext == "N/A"
gen ls_clean = ""
la var ls_clean "Last/Previous School"
// list school if missing(hs_clean) & schooltext == "HOMETOWN (LAST SCHOOL)"

replace ls_clean = school if inlist(schooltext, "LAST SCHOOL", "PREV SCHOOL", "PREVIOUS SCHOOL")

tempvar x
gen `x' = strpos(school, "(") + 1
replace ls_clean = strtrim(substr(school, `x', strlen(school) - `x')) ///
	if inlist(schooltext, "HOMETOWN (LAST SCHOOL)", "HOMETOWN (PREV SCHOOL)") & strpos(school, "(") > 0
drop `x'

tempvar x
gen `x' = strpos(school, "-") + 1
replace ls_clean = strtrim(substr(school, `x', strlen(school) - `x')) ///
	if inlist(schooltext, "HOMETOWN - LAST SCHOOL") & strpos(school, "-") > 0
replace ls_clean = strtrim(substr(school, 1, `x' - 1)) ///
	if schooltext == "LAST SCHOOL - HOMETOWN" & strpos(school, "-") > 0
drop `x'

tempvar x
gen `x' = strpos(school, "/") + 1
replace ls_clean = strtrim(substr(school, `x', strlen(school) - `x')) ///
	if inlist(schooltext, "HOMETOWN / LAST SCHOOL", "HOMETOWN / PREVIOUS SCHOOL", ///
	"HOMETOWN/LAST SCHOOL", "HOMETOWN/PREVIOUS SCHOOL") & strpos(school, "/") > 0
drop `x'

// converting these + high school to "prevschool" variable
replace hs_clean = ls_clean if missing(hs_clean)

replace ht_clean = strtrim(stritrim(ht_clean))
replace hs_clean = strtrim(stritrim(hs_clean))

keep name ht_clean hs_clean sport college
rename ht_clean hometown
rename hs_clean highschool

append using `full'

rename highschool prevschool

compress
save `full', replace


*******************************************************************************
use `full', clear
//  clean hometown variable and match to correct state variable
parse_hometown, hometown(hometown) city(city) state(state)
do _match_state_abbrev.do
gen nonUS = missing(desired_state)
rename state state_country_raw
order state_country_raw, after(hometown)
rename desired_state state
replace city = "" if missing(state)

rename nonUS nonUSmatch

// check false positives
preserve
	drop if missing(state)
	levelsof state, local(states)
	foreach state in `states' {
		disp "`state'"
		tab state_country_raw if state=="`state'"
		disp ""
		disp "***************************"
	}
restore


// merge conference
merge m:1 college using ${outdata}/schools, assert(3) nogen keepusing(conference)

// cleanup
la var name "Athlete Name (as scraped)"
la var hometown "Athlete Hometown (as scraped)"
la var prevschool "Athlete Previous School (as scraped)"
la var sport "Sport (by gender)"
la var college "College"
la var city "City (if US)"
la var state "State"
la var nonUS "Hometown not matched to US state"

drop state_country_raw
order nonUSmatch, last

// assert no complete duplicates (there is just one for some reason)
bysort *: gen N = _N
count if N > 1
local x = r(N)
assert `x' == 6
duplicates drop
drop N

// make sure cross-sport duplicates are truly multi-sport
// i.e. make sure didn't scrape mens or womens roster twice and apply to other
preserve
	bysort name college hometown: gen N = _N
	tab N
	keep if N>1
	gen gender = "M" if regexm(sport,"mens")
	replace gender = "F" if regexm(sport,"womens")
	drop if missing(gender)
	keep name college hometown sport gender
	bysort name college hometown: egen maxF = max(gender=="F")
	bysort name college hometown: egen minF = min(gender=="F")
	assert maxF == minF
restore

tab nonUSmatch
count if !nonUSmatch
count if !nonUSmatch & !missing(city)
count if !nonUSmatch & !missing(city) & !missing(prevschool)

export delimited using ${outdata}/rosters.csv, replace
save ${outdata}/rosters, replace

log close

exit, STATA clear
