set more off
capture log close

cd "~/Documents/GitHub/ncaa_rosters/code/clean/ancillary_data"

import delimited using state_abbrevs.csv, clear varnames(1)

// replace missing with something so each column is unique ID for merge
foreach v of varlist _all {
	gen lil_n = _n
	replace `v' = string(lil_n) if missing(`v')
	drop lil_n
	replace `v' = strtrim(`v')
	replace `v' = strltrim(`v')
}

// make upper, lower, proper case versions and strip "."
foreach v of varlist statename gpo ap alt* {
	gen `v'U = upper(`v')
	gen `v'L = lower(`v')
	gen `v'P = proper(`v')
	gen `v'S = subinstr(`v', ".", "", .)
}
assert strlen(usps2) == 2

save state_abbrevs, replace
