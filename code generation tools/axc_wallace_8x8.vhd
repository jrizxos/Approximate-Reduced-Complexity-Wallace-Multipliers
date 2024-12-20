signal s1012,s1011,s1010,s1009,s1008,s1007,s1006,s1005,s1004,s1003,
s1002,s1109,s1108,s1107,s1106,s1105,s2013,s2011,s2010,s2009,s2008,
s2007,s2006,s2005,s2004,s2003,s2108,s2107,s3012,s3010,s3009,s3008,
s3007,s3006,s3004,s4005,s0002,s4006,s4007,s4008,s4009,s4010,s4011 : std_logic;

prodA(0)  <= p(0);
prodA(1)  <= p(1);
prodA(2)  <= s1002;
prodA(3)  <= s2003;
prodA(4)  <= s3004;
prodA(5)  <= s4005;
prodA(6)  <= s4006;
prodA(7)  <= s4007;
prodA(8)  <= s4008;
prodA(9)  <= s4009;
prodA(10) <= s4010;
prodA(11) <= s4011;
prodA(12) <= s3012;
prodA(13) <= s2013;
prodA(14) <= p(63);

prodB(0)  <= '0';
prodB(1)  <= p(8);
prodB(2)  <= '0';
prodB(3)  <= '0';
prodB(4)  <= '0';
prodB(5)  <= '0';
prodB(6)  <= c4005;
prodB(7)  <= c4006;
prodB(8)  <= c4007;
prodB(9)  <= c4008;
prodB(10) <= c4009;
prodB(11) <= c4010;
prodB(12) <= c4011;
prodB(13) <= c3012;
prodB(14) <= c2013;



--first stage (16FA, 0HA)
----GROUP 0
fa1002 : full_adder_III port map(p(2),p(9),p(16),s1002,c1002);
fa1003 : full_adder_III port map(p(3),p(10),p(17),s1003,c1003);
fa1004 : full_adder_III port map(p(4),p(11),p(18),s1004,c1004);
fa1005 : full_adder_III port map(p(5),p(12),p(19),s1005,c1005);
fa1006 : full_adder_III port map(p(6),p(13),p(20),s1006,c1006);
fa1007 : full_adder_III port map(p(7),p(14),p(21),s1007,c1007);
fa1008 : full_adder_III port map(p(15),p(22),p(29),s1008,c1008);
fa1009 : full_adder_III port map(p(23),p(30),p(37),s1009,c1009);
fa1010 : full_adder_III port map(p(31),p(38),p(45),s1010,c1010);
fa1011 : full_adder_III port map(p(39),p(46),p(53),s1011,c1011);
fa1012 : full_adder_III port map(p(47),p(54),p(61),s1012,c1012);
----GROUP 1
fa1105 : full_adder_III port map(p(26),p(33),p(40),s1105,c1105);
fa1106 : full_adder_III port map(p(27),p(34),p(41),s1106,c1106);
fa1107 : full_adder_III port map(p(28),p(35),p(42),s1107,c1107);
fa1108 : full_adder_III port map(p(36),p(43),p(50),s1108,c1108);
fa1109 : full_adder_III port map(p(44),p(51),p(58),s1109,c1109);


--second stage
----GROUP 0
fa2003 : full_adder_III port map(s1003,c1002,p(24),s2003,c2003);
fa2004 : full_adder_III port map(s1004,c1003,p(25),s2004,c2004);
fa2005 : full_adder_III port map(s1005,c1004,s1105,s2005,c2005);
fa2006 : full_adder_III port map(s1006,c1005,s1106,s2006,c2006);
fa2007 : full_adder_III port map(s1007,c1006,s1107,s2007,c2007);
fa2008 : full_adder_III port map(s1008,c1007,s1108,s2008,c2008);
fa2009 : full_adder_III port map(s1009,c1008,s1109,s2009,c2009);
fa2010 : full_adder_III port map(s1010,c1009,p(52),s2010,c2010);
fa2011 : full_adder_III port map(s1011,c1010,p(60),s2011,c2011);
fa2013 : full_adder_III port map(p(55),c1012,p(62),s2013,c2013);
----GROUP 1
fa2107 : full_adder_III port map(c1106,p(49),p(56),s2107,c2107);
ha2108 : half_adder port map(c1107,p(57),s2108,c2108);


--third stage
----GROUP 0
fa3004 : full_adder_III port map(s2004,c2003,p(32),s3004,c3004);
fa3006 : full_adder_III port map(s2006,c2005,c1105,s3006,c3006);
fa3007 : full_adder_III port map(s2007,c2006,s2107,s3007,c3007);
fa3008 : full_adder_III port map(s2008,c2007,s2108,s3008,c3008);
fa3009 : full_adder_III port map(s2009,c2008,c1108,s3009,c3009);
fa3010 : full_adder_III port map(s2010,c2009,c1109,s3010,c3010);
fa3012 : full_adder_III port map(s1012,c2011,c1011,s3012,c3012);


--fourth stage
----GROUP 0
fa4005 : full_adder_III port map(s2005,c2004,c3004,s4005,c4005);
ha4006 : half_adder port map(s3006,p(48),s4006,c4006);
ha4007 : half_adder port map(s3007,c3006,s4007,c4007);
fa4008 : full_adder_III port map(s3008,c3007,c2107,s4008,c4008);
fa4009 : full_adder_III port map(s3009,c3008,c2108,s4009,c4009);
fa4010 : full_adder_III port map(s3010,c3009,p(59),s4010,c4010);
fa4011 : full_adder_III port map(s2011,c2010,c3010,s4011,c4011);


end Behavioral;