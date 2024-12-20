--------------------------------------------------------------------------------------
-- Company Name: Department of Computer Science & Engineering / University of Ioannina 

-- Engineer: Georgios Papatheodorou

-- Module: MAIN_8

-- Module Name: main_8

-- Revisions:
-- 
-- Additional Comments: 
--
--------------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity main_8 is
    port ( 	IN_A 	 		: in  	STD_LOGIC_VECTOR (7 downto 0);  	--MULTIPLICAND
           	IN_B 	 		: in  	STD_LOGIC_VECTOR (7 downto 0);  	--MULTIPLIER
				IN_WR			: in 	STD_LOGIC;						--INPUT REGISTER WRITE ENABLE
				IN_RST			: in 	STD_LOGIC;						--INPUT REGISTER RESET
				CLK				: in 	STD_LOGIC;						--CLOCK
           	OUTPUT		 	: out 	STD_LOGIC_VECTOR (14 downto 0); 	--OUTPUT 1st line
			OUT_WR			: in 	STD_LOGIC;							--OUTPUT REGISTER WRITE ENABLE
			OUT_RST			: in 	STD_LOGIC);							--OUTPUT REGISTER RESET
end main_8;


architecture Behavioral of main_8 is


component in_reg_8 is
	port ( 	in_reg_wr	: in 	std_logic; 
		in_reg_rst	: in 	std_logic; 
		clk		: in 	std_logic;
		in_reg_input 	: in 	std_logic_vector(7 downto 0) ;
		in_reg_output	: out 	std_logic_vector(7 downto 0));
end component;



component axc_wallace_8 is
	port  ( A0 	: in  std_logic_vector (7 downto 0);
		B0 	: in  std_logic_vector (7 downto 0);
           	prodA 	: out std_logic_vector (14 downto 0);
		prodB 	: out std_logic_vector (14 downto 0));
end component;



component out_reg_8 is
	port ( 	out_reg_wr	: in 	std_logic; 
		out_reg_rst	: in 	std_logic; 
		clk		: in 	std_logic;
		out_reg_input  	: in  	std_logic_vector(14 downto 0) ;
		out_reg_output 	: out 	std_logic_vector(14 downto 0));
end component;

signal in_regA_output, in_regB_output   		: std_logic_vector(7 downto 0);
signal wallace_outputA, wallace_outputB, sum_A_B  	: std_logic_vector(14 downto 0);

begin

in_reg_A : in_reg_8   port map (in_reg_input=>IN_A, in_reg_wr=>IN_WR, in_reg_rst=>IN_RST, clk=>CLK, in_reg_output=>in_regA_output);
in_reg_B : in_reg_8   port map (in_reg_input=>IN_B, in_reg_wr=>IN_WR, in_reg_rst=>IN_RST, clk=>CLK, in_reg_output=>in_regB_output);

wallace_mult  : axc_wallace_8  port map (A0=>in_regA_output, B0=>in_regB_output, prodA=>wallace_outputA, prodB=>wallace_outputB);

sum_A_B <= std_logic_vector(UNSIGNED(wallace_outputA) + UNSIGNED(wallace_outputB));

output_reg_A  : out_reg_8 port map (out_reg_input=>sum_A_B, out_reg_wr=>OUT_WR, out_reg_rst=>OUT_RST, clk=>CLK, out_reg_output=>OUTPUT);

end Behavioral;
