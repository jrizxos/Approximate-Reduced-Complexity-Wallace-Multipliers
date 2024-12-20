set_db init_lib_search_path {<dir>} -quiet
read_lib gf180mcu.lib 

set_db init_hdl_search_path {<dir>} -quiet 
read_hdl -language vhdl {axc_wallace_32.vhd  Full_Adder_II.vhd  Full_Adder_27.vhd  Full_Adder_III.vhd  \
                         Full_Adder_10.vhd  Full_Adder_1.vhd   Full_Adder_2.vhd	  Full_Adder_I.vhd     \
                         Full_Adder_11.vhd  Full_Adder_20.vhd  Full_Adder_3.vhd	  Full_Adder.vhd       \
                         Full_Adder_12.vhd  Full_Adder_21.vhd  Full_Adder_4.vhd	  half_adder.vhd       \
                         Full_Adder_13.vhd  Full_Adder_22.vhd  Full_Adder_5.vhd	  in_reg_32.vhd        \
                         Full_Adder_14.vhd  Full_Adder_23.vhd  Full_Adder_6.vhd	  main_32.vhd          \
                         Full_Adder_15.vhd  Full_Adder_24.vhd  Full_Adder_7.vhd	  out_reg_32.vhd       \
                         Full_Adder_16.vhd  Full_Adder_25.vhd  Full_Adder_8.vhd                        \
                         Full_Adder_17.vhd  Full_Adder_26.vhd  }       

elaborate
vcd design:main_32

set_time_unit -nanoseconds
create_clock [get_ports CLK] -name main_clk -period 33

set_db syn_generic_effort high -quiet 
set_db syn_map_effort high -quiet 
set_db syn_opt_effort high -quiet 

syn_generic
syn_map
syn_opt

report_timing > /tcl_out/<name>_timing.rpt
report_power > /tcl_out/<name>_power.rpt
report_area > /tcl_out/<name>_area.rpt

#puts "RUNTIME : [get_db real_runtime]"

exit