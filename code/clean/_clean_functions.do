// _clean_functions.do

*******************************************************************************
// parse_name

// splits names into first and last, works on name formats
// 1) John Smith --> JOHN, SMITH
// 2) Smith, John --> JOHN, SMITH
// 3) Karl Anthony-Towns --> KARL, ANTHONY-TOWNS
// 4) Anthony-Towns, Karl --> KARL, ANTHONY-TOWNS
// 5) Jordan Robert Keener --> JORDAN ROBERT, KEENER
// 6) Keener, Jordan Robert --> JORDAN ROBERT, KEENER

cap program drop parse_name
program define parse_name
	// takes namevar, returns first(middle) and last name
	syntax, name_var(varname) newvar(name)
	
	tempvar first_name last_name
	gen `first_name' = ""
	gen `last_name' = ""
	
	tempvar comma_pos space_pos space_pos_last
	gen `comma_pos' = strpos(`name_var', ",")
	gen `space_pos' = strpos(`name_var', " ")
	gen `space_pos_last' = strrpos(`name_var', " ")
	
	replace `first_name' = upper(strtrim(substr(`name_var', 1, `space_pos_last' - 1))) ///
		if `comma_pos' == 0
	replace `last_name' = upper(strtrim(substr(`name_var', `space_pos_last' + 1, .))) ///
		if `comma_pos' == 0
		
	replace `first_name' = upper(strtrim(substr(`name_var', `comma_pos' + 1, .))) ///
		if `comma_pos' != 0
	replace `last_name' = upper(strtrim(substr(`name_var', 1, `comma_pos' - 1))) ///
		if `comma_pos' != 0
	
	gen `newvar' = `first_name' + " " + `last_name'
	

end


// test of parse_name
quietly {
	clear
	set obs 6
	gen name = ""
	replace name = "John Smith" in 1
	replace name = "Smith, John" in 2
	replace name = "Karl Anthony-Towns" in 3
	replace name = "Anthony-Towns, Karl" in 4
	replace name = "Jordan Robert Keener" in 5
	replace name = "Keener, Jordan Robert" in 6

	parse_name, name_var(name) newvar(name_clean)

	assert name_clean == "JOHN SMITH" in 1/2
	assert name_clean == "KARL ANTHONY-TOWNS" in 3/4
	assert name_clean == "JORDAN ROBERT KEENER" in 5/6
	
	clear
}

*******************************************************************************
// parse_name_reverse

cap program drop parse_name_reverse
program define parse_name_reverse
	syntax, name_var(varname) newvar(name)
	
	tempvar first_name last_name space_pos
	
	gen `space_pos' = strpos(`name_var', " ")
	gen `first_name' = ""
	gen `last_name' = ""
	
	replace `last_name' = upper(strtrim(substr(`name_var', 1, `space_pos' - 1)))
	replace `first_name' = upper(strtrim(substr(`name_var', `space_pos' + 1, .)))
	
	gen `newvar' = `first_name' + " " + `last_name'
	
end

*******************************************************************************

// parse_hometown

// parses hometown variable and gives city, state

cap program drop parse_hometown
program define parse_hometown
	// takes hometown (can have other info after), returns city and state
	syntax, hometown(varname) city(name) state(name)
	
	tempvar ht
	gen `ht' = `hometown'
	
	replace `ht' = strtrim(substr(`ht',1,strpos(`ht',"(")-1)) ///
		if strpos(`ht',"(") != 0
	replace `ht' = strtrim(substr(`ht',1,strpos(`ht',"/")-1)) ///
		if strpos(`ht',"/") != 0
	replace `ht' = strtrim(substr(`ht',1,strpos(`ht',"-")-1)) ///
		if strpos(`ht',"-") != 0
						
	gen `city' = upper(strtrim(substr(`ht', 1, strpos(`ht',",")-1)))
	gen `state' = strtrim(substr(`ht',strpos(`ht',",")+1,.))

end

// test parse_hometown
quietly {
	clear
	set obs 4
	gen town = ""
	replace town = "Greenfield, Ind. (Greenfield)" in 1
	replace town = "Bloomington, IN / Bloomington North" in 2
	replace town = "Evanston, Illinois / (Evanston Township)" in 3
	replace town = "Kokomo, Ind." in 4

	parse_hometown, hometown(town) city(city) state(state)

	assert city == "GREENFIELD" & state == "Ind." in 1
	assert city == "BLOOMINGTON" & state == "IN" in 2
	assert city == "EVANSTON" & state == "Illinois" in 3
	assert city == "KOKOMO" & state == "Ind." in 4

	clear
}

*******************************************************************************
