// dummy example

// // make crosswalk
// clear
// set obs 2
// forvalues i = 1/3 {
// 	gen x`i' = ""
// }
//
// replace x1 = "IN" in 1
// replace x1 = "IL" in 2
// replace x2 = "Ind." in 1
// replace x2 = "Ill." in 2
// replace x3 = "Indiana" in 1
// replace x3 = "Illinois" in 2
//
// tempfile crosswalk
// save `crosswalk', replace
//
// // make data
// clear
// set obs 8
// gen state = ""
// replace state = "Ind." in 1
// replace state = "Ill." in 2
// replace state = "IN" in 3
// replace state = "Illinois" in 4
// replace state = "Ind." in 5
// replace state = "Ill." in 6
// replace state = "IN" in 7
// replace state = "Illi" in 8
//
// // algorithm
// gen desired_state = ""
// forval j = 1/3 {
// 	gen x`j' = state
// 	merge m:1 x`j' using `crosswalk', keep(1 3) keepusing(x1)
// 	replace desired_state = x1 if _merge==3
// 	drop x`j' _merge
// 	cap drop x1
// }

****************************************************************************
// _match_state_abbrev
* attempts to merge the state variable with all possible types in state_abbrevs
quietly {
	preserve

	cd "~/Documents/GitHub/ncaa_rosters/code/clean"
	use "ancillary_data/state_abbrevs", clear
	local i = 1
	foreach v of varlist _all {
		rename `v' x`i'
		local ++i
	}
	local numvars = `i' - 1
	disp `i'
	tempfile crosswalk
	save `crosswalk'

	restore

	// algorithm
	gen desired_state = ""
	forval j = 1/`numvars' {
		gen x`j' = state
		merge m:1 x`j' using `crosswalk', keep(1 3) keepusing(x1)
		replace desired_state = x1 if _merge==3
		drop x`j' _merge
		cap drop x1
	}
}
