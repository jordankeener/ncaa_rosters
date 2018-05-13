set more off
cap log close

global homedir "~/Documents/GitHub/ncaa_rosters"
global indata ${homedir}/output
global outdata ${homedir}/output/cleaned
global code ${homedir}/code/clean

run ${code}/ancillary_data/state_abbrevs.do
cd ${code}
run _clean_functions.do

// cleans raw roster data

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
rename school school_full_name
rename dset 	school
local keepvars school school_full_name conference scrape_date football_url
keep  `keepvars'
order `keepvars'

la var school 					"School"
la var school_full_name "Full School Name"
la var conference 			"Conference"
la var scrape_date 			"Date rosters scraped"
la var football_url 		"URL of football roster"

export excel using ${outdata}/schools.csv, replace
save ${outdata}/schools, replace

******************************************************************************
// loop through schools and combine
clear
tempfile full
local i = 0
foreach school in `schools' {
import delimited using ${indata}/`school'_rosters.csv, clear varnames(1)
	cap drop v1

	if `i'>0 {
		append using `full'
	}
	save `full', replace

	local ++i

}

//  clean hometown variable and match to correct state variable
parse_hometown, hometown(hometown) city(city) state(state)
do _match_state_abbrev.do
gen nonUS = missing(desired_state)
rename state state_country_raw
order state_country_raw, after(hometown)
rename desired_state state
replace city = "" if missing(state)

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

// fix sport name in cases where gender specified
replace sport = subinstr(sport, "mixed", "mens", 1) if gender == "Men"
replace sport = subinstr(sport, "mixed", "womens", 1) if gender == "Women"
drop gender

// merge conference
merge m:1 school using ${outdata}/schools, assert(3) nogen keepusing(conference)

// cleanup
rename hometown hometown_raw
la var name "Athlete Name (as scraped)"
la var hometown_raw "Athlete Hometown (as scraped)"
la var state_country_raw "Simple State/Country extraction"
la var sport "Sport (by gender)"
la var school "School"
la var city "City (if US)"
la var state "State"
la var nonUS "Hometown not matched to US state"

// assert no complete duplicates (there is just one for some reason)
bysort *: gen N = _N
qui count if N > 1
local x = r(N)
assert `x' == 2
duplicates drop
drop N

// make sure cross-sport duplicates are truly multi-sport
// i.e. make sure didn't scrape mens or womens roster twice and apply to other
preserve
	bysort name school hometown_raw: gen N = _N
	tab N
	keep if N>1
	gen gender = "M" if regexm(sport,"mens")
	replace gender = "F" if regexm(sport,"womens")
	drop if missing(gender)
	keep name school hometown sport gender
	bysort name school hometown: egen maxF = max(gender=="F")
	bysort name school hometown: egen minF = min(gender=="F")
	assert maxF == minF
restore

export delimited using ${outdata}/rosters.csv, replace
save ${outdata}/rosters, replace
