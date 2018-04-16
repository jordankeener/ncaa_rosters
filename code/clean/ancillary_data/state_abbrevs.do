set more off
capture log close

cd "~/Documents/GitHub/ncaa_rosters/code/clean/ancillary_data"

import delimited using state_abbrevs.csv, clear varnames(1)
foreach v of varlist _all {	
	gen lil_n = _n
	replace `v' = string(lil_n) if missing(`v')
	drop lil_n
	replace `v' = strtrim(`v')
	replace `v' = strltrim(`v')
}
foreach v of varlist statename gpo ap alt* {
	gen `v'U = upper(`v')
	gen `v'L = lower(`v')
}
assert strlen(usps2) == 2

save state_abbrevs, replace
