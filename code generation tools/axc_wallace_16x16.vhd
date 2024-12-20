s10028,s10027,s10026,s10025,s10024,s10023,s10022,s10021,s10020,--STAGE1
s10019,s10018,s10017,s10016,s10015,s10014,s10013,s10012,s10011,s10010,
s10009,s10008,s10007,s10006,s10005,s10004,s10003,s10002,s10125,s10124,
s10123,s10122,s10121,s10120,s10119,s10118,s10117,s10116,s10115,s10114,
s10113,s10112,s10111,s10110,s10109,s10108,s10107,s10106,s10105,s10222,
s10221,s10220,s10219,s10218,s10217,s10216,s10215,s10214,s10213,s10212,
s10211,s10210,s10209,s10208,s10319,s10318,s10317,s10316,s10315,s10314,
s10313,s10312,s10311,s10416,s10415,s10414,

s20029,s20027,s20026,s20025,s20024,s20023,s20022,s20021,s20020,s20019,--STAGE2
s20018,s20017,s20016,s20015,s20014,s20013,s20012,s20011,s20010,s20009,
s20008,s20007,s20006,s20005,s20004,s20003,s20123,s20122,s20121,s20120,
s20119,s20118,s20117,s20116,s20115,s20114,s20113,s20112,s20111,s20110,
s20109,s20107,s20220,s20218,s20217,s20216,s20215,s20214,s20213,s20212,

s30028,s30026,s30025,s30024,s30023,s30022,s30021,s30020,s30019,s30018,--STAGE3
s30017,s30016,s30015,s30014,s30013,s30012,s30011,s30010,s30009,s30008,
s30007,s30006,s30004,s30121,s30119,s30118,s30117,s30116,s30115,s30114,
s30113,s30110,

s40027,s40026,s40024,s40023,s40022,s40021,s40020,s40019,s40018,s40017,--STAGE4
s40016,s40015,s40014,s40013,s40012,s40011,s40010,s40009,s40008,s40005,
s40117,s40116,s40115,

s50025,s50024,s50023,s50022,s50020,s50019,s50018,s50017,s50016,s50015,--STAGE5
s50014,s50013,s50012,s50011,s50006,

s60021,s60020,s60019,s60018,s60017,s60016,s60015,s60014,s60013,s60012,--STAGE6
s60011,s60010,s60009,s60008,s60007

prodA(0)  <= p(0);
prodA(1)  <= p(1);
prodA(2)  <= s10002;
prodA(3)  <= s20003;
prodA(4)  <= s30004;
prodA(5)  <= s40005;
prodA(6)  <= s50006;
prodA(7)  <= s60007;
prodA(8)  <= s60008;
prodA(9)  <= s60009;
prodA(10) <= s60010;
prodA(11) <= s60011;
prodA(12) <= s60012;
prodA(13) <= s60013;
prodA(14) <= s60014;
prodA(15) <= s60015;
prodA(16) <= s60016;
prodA(17) <= s60017;
prodA(18) <= s60018;
prodA(19) <= s60019;
prodA(20) <= s60020;
prodA(21) <= s60021;
prodA(22) <= s50022;
prodA(23) <= s50023;
prodA(24) <= s50024;
prodA(25) <= s50025;
prodA(26) <= s40026;
prodA(27) <= s40027;
prodA(28) <= s30028;
prodA(29) <= s20029;
prodA(30) <= p(255);


prodB(0)  <= '0';
prodB(1)  <= p(16);
prodB(2)  <= '0';
prodB(3)  <= '0';
prodB(4)  <= '0';
prodB(5)  <= '0';
prodB(6)  <= '0';
prodB(7)  <= '0';
prodB(8)  <= c60007;
prodB(9)  <= c60008;
prodB(10) <= c60009;
prodB(11) <= c60010;
prodB(12) <= c60011;
prodB(13) <= c60012;
prodB(14) <= c60013;
prodB(15) <= c60014;
prodB(16) <= c60015;
prodB(17) <= c60016;
prodB(18) <= c60017;
prodB(19) <= c60018;
prodB(20) <= c60019;
prodB(21) <= c60020;
prodB(22) <= c60021;
prodB(23) <= c50022;
prodB(24) <= c50023;
prodB(25) <= c50024;
prodB(26) <= c50025;
prodB(27) <= c40026;
prodB(28) <= c40027;
prodB(29) <= c30028;
prodB(30) <= c20029;



--STAGE 1 -  FULL ADDERS:75 | HALF ADDERS:0
--GROUP 00
fa10002 : full_adder port map(p(2),p(17),p(32),s10002,c10002);
fa10003 : full_adder port map(p(3),p(18),p(33),s10003,c10003);
fa10004 : full_adder port map(p(4),p(19),p(34),s10004,c10004);
fa10005 : full_adder port map(p(5),p(20),p(35),s10005,c10005);
fa10006 : full_adder port map(p(6),p(21),p(36),s10006,c10006);
fa10007 : full_adder port map(p(7),p(22),p(37),s10007,c10007);
fa10008 : full_adder port map(p(8),p(23),p(38),s10008,c10008);
fa10009 : full_adder port map(p(9),p(24),p(39),s10009,c10009);
fa10010 : full_adder port map(p(10),p(25),p(40),s10010,c10010);
fa10011 : full_adder port map(p(11),p(26),p(41),s10011,c10011);
fa10012 : full_adder port map(p(12),p(27),p(42),s10012,c10012);
fa10013 : full_adder port map(p(13),p(28),p(43),s10013,c10013);
fa10014 : full_adder port map(p(14),p(29),p(44),s10014,c10014);
fa10015 : full_adder port map(p(15),p(30),p(45),s10015,c10015);

fa10016 : full_adder port map(p(31),p(46),p(61),s10016,c10016);
fa10017 : full_adder port map(p(47),p(62),p(77),s10017,c10017);
fa10018 : full_adder port map(p(63),p(78),p(93),s10018,c10018);
fa10019 : full_adder port map(p(79),p(94),p(109),s10019,c10019);
fa10020 : full_adder port map(p(95),p(110),p(125),s10020,c10020);
fa10021 : full_adder port map(p(111),p(126),p(141),s10021,c10021);
fa10022 : full_adder port map(p(127),p(142),p(157),s10022,c10022);
fa10023 : full_adder port map(p(143),p(158),p(173),s10023,c10023);
fa10024 : full_adder port map(p(159),p(174),p(189),s10024,c10024);
fa10025 : full_adder port map(p(175),p(190),p(205),s10025,c10025);
fa10026 : full_adder port map(p(191),p(206),p(221),s10026,c10026);
fa10027 : full_adder port map(p(207),p(222),p(237),s10027,c10027);
fa10028 : full_adder port map(p(223),p(238),p(253),s10028,c10028);


--STAGE 1 GROUP 01
fa10105 : full_adder port map(p(50),p(65),p(80),s10105,c10105);
fa10106 : full_adder port map(p(51),p(66),p(81),s10106,c10106);
fa10107 : full_adder port map(p(52),p(67),p(82),s10107,c10107);
fa10108 : full_adder port map(p(53),p(68),p(83),s10108,c10108);
fa10109 : full_adder port map(p(54),p(69),p(84),s10109,c10109);
fa10110 : full_adder port map(p(55),p(70),p(85),s10110,c10110);
fa10111 : full_adder port map(p(56),p(71),p(86),s10111,c10111);
fa10112 : full_adder port map(p(57),p(72),p(87),s10112,c10112);
fa10113 : full_adder port map(p(58),p(73),p(88),s10113,c10113);
fa10114 : full_adder port map(p(59),p(74),p(89),s10114,c10114);
fa10115 : full_adder port map(p(60),p(75),p(90),s10115,c10115);
fa10116 : full_adder port map(p(76),p(91),p(106),s10116,c10116);
fa10117 : full_adder port map(p(92),p(107),p(122),s10117,c10117);
fa10118 : full_adder port map(p(108),p(123),p(138),s10118,c10118);
fa10119 : full_adder port map(p(124),p(139),p(154),s10119,c10119);
fa10120 : full_adder port map(p(140),p(155),p(170),s10120,c10120);
fa10121 : full_adder port map(p(156),p(171),p(186),s10121,c10121);
fa10122 : full_adder port map(p(172),p(187),p(202),s10122,c10122);
fa10123 : full_adder port map(p(188),p(203),p(218),s10123,c10123);
fa10124 : full_adder port map(p(204),p(219),p(234),s10124,c10124);
fa10125 : full_adder port map(p(220),p(235),p(250),s10125,c10125);


--STAGE 1 GROUP 02
fa10208 : full_adder port map(p(98),p(113),p(128),s10208,c10208);
fa10209 : full_adder port map(p(99),p(114),p(129),s10209,c10209);
fa10210 : full_adder port map(p(100),p(115),p(130),s10210,c10210);
fa10211 : full_adder port map(p(101),p(116),p(131),s10211,c10211);
fa10212 : full_adder port map(p(102),p(117),p(132),s10212,c10212);
fa10213 : full_adder port map(p(103),p(118),p(133),s10213,c10213);
fa10214 : full_adder port map(p(104),p(119),p(134),s10214,c10214);
fa10215 : full_adder port map(p(105),p(120),p(135),s10215,c10215);
fa10216 : full_adder port map(p(121),p(136),p(151),s10216,c10216);
fa10217 : full_adder port map(p(137),p(152),p(167),s10217,c10217);
fa10218 : full_adder port map(p(153),p(168),p(183),s10218,c10218);
fa10219 : full_adder port map(p(169),p(184),p(199),s10219,c10219);
fa10220 : full_adder port map(p(185),p(200),p(215),s10220,c10220);
fa10221 : full_adder port map(p(201),p(216),p(231),s10221,c10221);
fa10222 : full_adder port map(p(217),p(232),p(247),s10222,c10222);


--STAGE 1 GROUP 03
fa10311 : full_adder port map(p(146),p(161),p(176),s10311,c10311);
fa10312 : full_adder port map(p(147),p(162),p(177),s10312,c10312);
fa10313 : full_adder port map(p(148),p(163),p(178),s10313,c10313);
fa10314 : full_adder port map(p(149),p(164),p(179),s10314,c10314);
fa10315 : full_adder port map(p(150),p(165),p(180),s10315,c10315);
fa10316 : full_adder port map(p(166),p(181),p(196),s10316,c10316);
fa10317 : full_adder port map(p(182),p(197),p(212),s10317,c10317);
fa10318 : full_adder port map(p(198),p(213),p(228),s10318,c10318);
fa10319 : full_adder port map(p(214),p(229),p(244),s10319,c10319);


--STAGE 1 GROUP 04
fa10414 : full_adder port map(p(194),p(209),p(224),s10414,c10414);
fa10415 : full_adder port map(p(195),p(210),p(225),s10415,c10415);
fa10416 : full_adder port map(p(211),p(226),p(241),s10416,c10416);


-----------------------------------------------------------------

--STAGE 2 -  FULL ADDERS:50 | HALF ADDERS:0
--GROUP 00
fa20003 : full_adder port map(s10003,c10002,p(48),s20003,c20003);
fa20004 : full_adder port map(s10004,c10003,p(49),s20004,c20004);
fa20005 : full_adder port map(s10005,c10004,s10105,s20005,c20005);
fa20006 : full_adder port map(s10006,c10005,s10106,s20006,c20006);
fa20007 : full_adder port map(s10007,c10006,s10107,s20007,c20007);
fa20008 : full_adder port map(s10008,c10007,s10108,s20008,c20008);
fa20009 : full_adder port map(s10009,c10008,s10109,s20009,c20009);
fa20010 : full_adder port map(s10010,c10009,s10110,s20010,c20010);
fa20011 : full_adder port map(s10011,c10010,s10111,s20011,c20011);
fa20012 : full_adder port map(s10012,c10011,s10112,s20012,c20012);
fa20013 : full_adder port map(s10013,c10012,s10113,s20013,c20013);
fa20014 : full_adder port map(s10014,c10013,s10114,s20014,c20014);
fa20015 : full_adder port map(s10015,c10014,s10115,s20015,c20015);

fa20016 : full_adder port map(s10016,c10015,s10116,s20016,c20016);
fa20017 : full_adder port map(s10017,c10016,s10117,s20017,c20017);
fa20018 : full_adder port map(s10018,c10017,s10118,s20018,c20018);
fa20019 : full_adder port map(s10019,c10018,s10119,s20019,c20019);
fa20020 : full_adder port map(s10020,c10019,s10120,s20020,c20020);
fa20021 : full_adder port map(s10021,c10020,s10121,s20021,c20021);
fa20022 : full_adder port map(s10022,c10021,s10122,s20022,c20022);
fa20023 : full_adder port map(s10023,c10022,s10123,s20023,c20023);
fa20024 : full_adder port map(s10024,c10023,s10124,s20024,c20024);
fa20025 : full_adder port map(s10025,c10024,s10125,s20025,c20025);
fa20026 : full_adder port map(s10026,c10025,p(236),s20026,c20026);
fa20027 : full_adder port map(s10027,c10026,p(252),s20027,c20027);
fa20029 : full_adder port map(p(239),p(254),c10028,s20029,c20029);


--STAGE 2 GROUP 01
fa20107 : full_adder port map(c10106,p(97),p(112),s20107,c20107);
fa20109 : full_adder port map(c10108,s10209,c10208,s20109,c20109);
fa20110 : full_adder port map(c10109,s10210,c10209,s20110,c20110);
fa20111 : full_adder port map(c10110,s10211,c10210,s20111,c20111);
fa20112 : full_adder port map(c10111,s10212,c10211,s20112,c20112);
fa20113 : full_adder port map(c10112,s10213,c10212,s20113,c20113);
fa20114 : full_adder port map(c10113,s10214,c10213,s20114,c20114);
fa20115 : full_adder port map(c10114,s10215,c10214,s20115,c20115);
fa20116 : full_adder port map(c10115,s10216,c10215,s20116,c20116);
fa20117 : full_adder port map(c10116,s10217,c10216,s20117,c20117);
fa20118 : full_adder port map(c10117,s10218,c10217,s20118,c20118);
fa20119 : full_adder port map(c10118,s10219,c10218,s20119,c20119);
fa20120 : full_adder port map(c10119,s10220,c10219,s20120,c20120);
fa20121 : full_adder port map(c10120,s10221,c10220,s20121,c20121);
fa20122 : full_adder port map(c10121,s10222,c10221,s20122,c20122);
fa20123 : full_adder port map(c10122,p(233),p(248),s20123,c20123);


--STAGE 2 GROUP 02
fa20212 : full_adder port map(s10312,c10311,p(192),s20212,c20212);
fa20213 : full_adder port map(s10313,c10312,p(193),s20213,c20213);
fa20214 : full_adder port map(s10314,c10313,s10414,s20214,c20214);
fa20215 : full_adder port map(s10315,c10314,s10415,s20215,c20215);
fa20216 : full_adder port map(s10316,c10315,s10416,s20216,c20216);
fa20217 : full_adder port map(s10317,c10316,p(227),s20217,c20217);
fa20218 : full_adder port map(s10318,c10317,p(243),s20218,c20218);
fa20220 : full_adder port map(p(230),p(245),c10319,s20220,c20220);

-----------------------------------------------------------------

--STAGE 3 -  FULL ADDERS:32 | HALF ADDERS:0
--GROUP 00
fa30004 : full_adder port map(s20004,c20003,p(64),s30004,c30004);
fa30006 : full_adder port map(s20006,c20005,c10105,s30006,c30006);
fa30007 : full_adder port map(s20007,c20006,s20107,s30007,c30007);
fa30008 : full_adder port map(s20008,c20007,c10107,s30008,c30008);
fa30009 : full_adder port map(s20009,c20008,s20109,s30009,c30009);
fa30010 : full_adder port map(s20010,c20009,s20110,s30010,c30010);
fa30011 : full_adder port map(s20011,c20010,s20111,s30011,c30011);
fa30012 : full_adder port map(s20012,c20011,s20112,s30012,c30012);
fa30013 : full_adder port map(s20013,c20012,s20113,s30013,c30013);
fa30014 : full_adder port map(s20014,c20013,s20114,s30014,c30014);
fa30015 : full_adder port map(s20015,c20014,s20115,s30015,c30015);
fa30016 : full_adder port map(s20016,c20015,s20116,s30016,c30016);
fa30017 : full_adder port map(s20017,c20016,s20117,s30017,c30017);
fa30018 : full_adder port map(s20018,c20017,s20118,s30018,c30018);
fa30019 : full_adder port map(s20019,c20018,s20119,s30019,c30019);
fa30020 : full_adder port map(s20020,c20019,s20120,s30020,c30020);
fa30021 : full_adder port map(s20021,c20020,s20121,s30021,c30021);
fa30022 : full_adder port map(s20022,c20021,s20122,s30022,c30022);
fa30023 : full_adder port map(s20023,c20022,s20123,s30023,c30023);
fa30024 : full_adder port map(s20024,c20023,c10123,s30024,c30024);
fa30025 : full_adder port map(s20025,c20024,c10124,s30025,c30025);
fa30026 : full_adder port map(s20026,c20025,p(251),s30026,c30026);
fa30028 : full_adder port map(s10028,c10027,c20027,s30028,c30028);

--STAGE 3 GROUP 01
fa30110 : full_adder port map(c20109,p(145),p(160),s30110,c30110);
fa30113 : full_adder port map(c20112,s20213,c20212,s30113,c30113);
fa30114 : full_adder port map(c20113,s20214,c20213,s30114,c30114);
fa30115 : full_adder port map(c20114,s20215,c20214,s30115,c30115);
fa30116 : full_adder port map(c20115,s20216,c20215,s30116,c30116);
fa30117 : full_adder port map(c20116,s20217,c20216,s30117,c30117);
fa30118 : full_adder port map(c20117,s20218,c20217,s30118,c30118);
fa30119 : full_adder port map(c20118,s10319,c10318,s30119,c30119);
fa30121 : full_adder port map(c20120,p(246),c20220,s30121,c30121);

-----------------------------------------------------------------

--STAGE 4 -  FULL ADDERS:22 | HALF ADDERS:1
--GROUP 00
fa40005 : full_adder port map(s20005,c20004,c30004,s40005,c40005);
fa40008 : full_adder port map(s30008,c30007,s10208,s40008,c40008);
fa40009 : full_adder port map(s30009,c30008,p(144),s40009,c40009);
fa40010 : full_adder port map(s30010,c30009,s30110,s40010,c40010);
fa40011 : full_adder port map(s30011,c30010,c20110,s40011,c40011);
fa40012 : full_adder port map(s30012,c30011,c20111,s40012,c40012);
fa40013 : full_adder port map(s30013,c30012,s30113,s40013,c40013);
fa40014 : full_adder port map(s30014,c30013,s30114,s40014,c40014);
fa40015 : full_adder port map(s30015,c30014,s30115,s40015,c40015);
fa40016 : full_adder port map(s30016,c30015,s30116,s40016,c40016);
fa40017 : full_adder port map(s30017,c30016,s30117,s40017,c40017);
fa40018 : full_adder port map(s30018,c30017,s30118,s40018,c40018);
fa40019 : full_adder port map(s30019,c30018,s30119,s40019,c40019);
fa40020 : full_adder port map(s30020,c30019,c20119,s40020,c40020);
fa40021 : full_adder port map(s30021,c30020,s30121,s40021,c40021);
fa40022 : full_adder port map(s30022,c30021,c20121,s40022,c40022);
fa40023 : full_adder port map(s30023,c30022,c20122,s40023,c40023);
fa40024 : full_adder port map(s30024,c30023,p(249),s40024,c40024);
fa40026 : full_adder port map(s30026,c30025,c10125,s40026,c40026);
fa40027 : full_adder port map(s20027,c20026,c30026,s40027,c40027);

--STAGE 4 GROUP 01
fa40115 : full_adder port map(c30114,c10414,p(240),s40115,c40115);
ha40116 : half_adder port map(c30115,c10415,s40116,c40116);
fa40117 : full_adder port map(c30116,p(242),c10416,s40117,c40117);

-----------------------------------------------------------------

--STAGE 5 -  FULL ADDERS:15 | HALF ADDERS:0
--GROUP 00
fa50006 : full_adder port map(s30006,p(96),c40005,s50006,c50006);
fa50011 : full_adder port map(s40011,c40010,s10311,s50011,c50011);
fa50012 : full_adder port map(s40012,c40011,s20212,s50012,c50012);
fa50013 : full_adder port map(s40013,c40012,p(208),s50013,c50013);
fa50014 : full_adder port map(s40014,c40013,c30113,s50014,c50014);
fa50015 : full_adder port map(s40015,c40014,s40115,s50015,c50015);
fa50016 : full_adder port map(s40016,c40015,c30115,s50016,c50016);
fa50017 : full_adder port map(s40017,c40016,c30116,s50017,c50017);
fa50018 : full_adder port map(s40018,c40017,c30117,s50018,c50018);
fa50019 : full_adder port map(s40019,c40018,c30118,s50019,c50019);
fa50020 : full_adder port map(s40020,c40019,s20220,s50020,c50020);
fa50022 : full_adder port map(s40022,c40021,c30121,s50022,c50022);
fa50023 : full_adder port map(s40023,c40022,c10222,s50023,c50023);
fa50024 : full_adder port map(s40024,c40023,c20123,s50024,c50024);
fa50025 : full_adder port map(s30025,c30024,c40024,s50025,c50025);


-----------------------------------------------------------------

--STAGE 6 -  FULL ADDERS:7 | HALF ADDERS:8
--GROUP 00
fa60007 : full_adder port map(s30007,c30006,c50006,s60007,c60007);
ha60008 : half_adder port map(s40008,c20107,s60008,c60008);
ha60009 : half_adder port map(s40009,c40008,s60009,c60009);
ha60010 : half_adder port map(s40010,c40009,s60010,c60010);
ha60011 : half_adder port map(s50011,c30110,s60011,c60011);
ha60012 : half_adder port map(s50012,c50011,s60012,c60012);
ha60013 : half_adder port map(s50013,c50012,s60013,c60013);
ha60014 : half_adder port map(s50014,c50013,s60014,c60014);
ha60015 : half_adder port map(s50015,c50014,s60015,c60015);
fa60016 : full_adder port map(s50016,c50015,c40115,s60016,c60016);
fa60017 : full_adder port map(s50017,c50016,c40116,s60017,c60017);
fa60018 : full_adder port map(s50018,c50017,c40117,s60018,c60018);
fa60019 : full_adder port map(s50019,c50018,c20218,s60019,c60019);
fa60020 : full_adder port map(s50020,c50019,c30119,s60020,c60020);
fa60021 : full_adder port map(s40021,c40020,c50020,s60021,c60021);