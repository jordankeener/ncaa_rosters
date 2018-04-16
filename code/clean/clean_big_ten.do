set more off
cap log close

global homedir "~/Documents/GitHub/ncaa_rosters"
global indata ${homedir}/output
global outdata ${homedir}/output/cleaned
global code ${homedir}/code/clean

cd ${code}

run _clean_functions.do

// cleans Big Ten rosters
* output: big_ten.dta and big_ten.csv

tempfile full

local schools "illinois indiana iowa maryland michigan michigan_state minnesota nebraska northwestern ohio_state penn_state purdue rutgers wisconsin"

local i = 0
foreach school in `schools' {
import delimited using ${indata}/`school'_rosters.csv, clear varnames(1)
	cap drop v1

	parse_hometown, hometown(hometown) city(city) state(state)
	do _match_state_abbrev.do
	gen nonUS = missing(desired_state)
	rename state state_country_raw
	order state_country_raw, after(hometown)
	rename desired_state state
	replace city = "" if missing(state)

	if `i'>0 {
		append using `full'
	}
	save `full', replace
	
	local ++i
}

tab school


// // Illinois
// import delimited using ${indata}/illinois_rosters.csv, clear varnames(1)
// cap drop v1
//
// // rename name name_raw
// // parse_name, name_var(name_raw) newvar(name)
//
// parse_hometown, hometown(hometown) city(city) state(state)
// do _match_state_abbrev.do
// gen nonUS = missing(desired_state)
// rename state state_country_raw
// order state_country_raw, after(hometown)
// rename desired_state state
// replace city = "" if missing(state)
//
// save `full', replace
//
// // Indiana
// import delimited using ${indata}/indiana_rosters.csv, clear varnames(1)
// cap drop v1
//
// rename name name_raw
// parse_name, name_var(name_raw) newvar(name)
//
// parse_hometown, hometown(hometown) city(city) state(state)
// do _match_state_abbrev.do
// gen nonUS = missing(desired_state)
// rename state state_country_raw
// order state_country_raw, after(hometown)
// rename desired_state state
// replace city = "" if missing(state)
//
// append using `full'
// save `full', replace
//
// // Purdue
// import delimited using ${indata}/purdue_rosters.csv, clear varnames(1)
// cap drop v1
