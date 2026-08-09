#!/usr/bin/env python3
"""
Tini Font Structure Generator - Creates empty tini4.sfd and tini5.sfd with glyph definitions.

Font specs:
  tini4: width=4px, ascent=10px above baseline, descent=2px below baseline
  tini5: width=5px, ascent=11px above baseline, descent=3px below baseline

This script generates the font project structure, glyph definitions, encoding,
metrics, and required metadata. All glyphs are created as empty placeholders.
You can draw the actual bitmap glyphs manually in FontForge.
"""

import os


# ============================================================
# Character Set Definition
# ============================================================

# Unicode character definitions with PostScript names
# Format: (codepoint, postscript_name)
CHARACTER_SET = [
    # Basic Latin (ASCII 32-126)
    (0x20, 'space'), (0x21, 'exclam'), (0x22, 'quotedbl'), (0x23, 'numbersign'),
    (0x24, 'dollar'), (0x25, 'percent'), (0x26, 'ampersand'), (0x27, 'quotesingle'),
    (0x28, 'parenleft'), (0x29, 'parenright'), (0x2A, 'asterisk'), (0x2B, 'plus'),
    (0x2C, 'comma'), (0x2D, 'hyphen'), (0x2E, 'period'), (0x2F, 'slash'),
    
    # Digits
    (0x30, 'zero'), (0x31, 'one'), (0x32, 'two'), (0x33, 'three'),
    (0x34, 'four'), (0x35, 'five'), (0x36, 'six'), (0x37, 'seven'),
    (0x38, 'eight'), (0x39, 'nine'),
    
    (0x3A, 'colon'), (0x3B, 'semicolon'), (0x3C, 'less'), (0x3D, 'equal'),
    (0x3E, 'greater'), (0x3F, 'question'), (0x40, 'at'),
    
    # Uppercase letters
    (0x41, 'A'), (0x42, 'B'), (0x43, 'C'), (0x44, 'D'), (0x45, 'E'), (0x46, 'F'),
    (0x47, 'G'), (0x48, 'H'), (0x49, 'I'), (0x4A, 'J'), (0x4B, 'K'), (0x4C, 'L'),
    (0x4D, 'M'), (0x4E, 'N'), (0x4F, 'O'), (0x50, 'P'), (0x51, 'Q'), (0x52, 'R'),
    (0x53, 'S'), (0x54, 'T'), (0x55, 'U'), (0x56, 'V'), (0x57, 'W'), (0x58, 'X'),
    (0x59, 'Y'), (0x5A, 'Z'),
    
    (0x5B, 'bracketleft'), (0x5C, 'backslash'), (0x5D, 'bracketright'),
    (0x5E, 'asciicircum'), (0x5F, 'underscore'), (0x60, 'grave'),
    
    # Lowercase letters
    (0x61, 'a'), (0x62, 'b'), (0x63, 'c'), (0x64, 'd'), (0x65, 'e'), (0x66, 'f'),
    (0x67, 'g'), (0x68, 'h'), (0x69, 'i'), (0x6A, 'j'), (0x6B, 'k'), (0x6C, 'l'),
    (0x6D, 'm'), (0x6E, 'n'), (0x6F, 'o'), (0x70, 'p'), (0x71, 'q'), (0x72, 'r'),
    (0x73, 's'), (0x74, 't'), (0x75, 'u'), (0x76, 'v'), (0x77, 'w'), (0x78, 'x'),
    (0x79, 'y'), (0x7A, 'z'),
    
    (0x7B, 'braceleft'), (0x7C, 'bar'), (0x7D, 'braceright'), (0x7E, 'asciitilde'),
    
    # Latin-1 Supplement
    (0xA0, 'nbspace'),
    
    # Latin-1 accented characters
    (0xC0, 'Agrave'), (0xC1, 'Aacute'), (0xC2, 'Acircumflex'), (0xC3, 'Atilde'),
    (0xC8, 'Egrave'), (0xC9, 'Eacute'), (0xCA, 'Ecircumflex'),
    (0xCC, 'Igrave'), (0xCD, 'Iacute'),
    (0xD2, 'Ograve'), (0xD3, 'Oacute'), (0xD4, 'Ocircumflex'), (0xD5, 'Otilde'),
    (0xD9, 'Ugrave'), (0xDA, 'Uacute'), (0xDD, 'Yacute'),
    
    (0xE0, 'agrave'), (0xE1, 'aacute'), (0xE2, 'acircumflex'), (0xE3, 'atilde'),
    (0xE8, 'egrave'), (0xE9, 'eacute'), (0xEA, 'ecircumflex'),
    (0xEC, 'igrave'), (0xED, 'iacute'),
    (0xF2, 'ograve'), (0xF3, 'oacute'), (0xF4, 'ocircumflex'), (0xF5, 'otilde'),
    (0xF9, 'ugrave'), (0xFA, 'uacute'), (0xFD, 'yacute'),
    
    # Latin Extended-A (Vietnamese)
    (0x102, 'Abreve'), (0x103, 'abreve'),
    (0x110, 'Dcroat'), (0x111, 'dcroat'),
    (0x168, 'Utilde'), (0x169, 'utilde'),
    
    # Latin Extended-B (Vietnamese)
    (0x1A0, 'Ohorn'), (0x1A1, 'ohorn'),
    (0x1AF, 'Uhorn'), (0x1B0, 'uhorn'),
    
    # Vietnamese Extended (U+1E00-1EFF)
    # A variants
    (0x1EA0, 'Adotbelow'), (0x1EA1, 'adotbelow'),
    (0x1EA2, 'Ahookabove'), (0x1EA3, 'ahookabove'),
    (0x1EA4, 'Acircumflexacute'), (0x1EA5, 'acircumflexacute'),
    (0x1EA6, 'Acircumflexgrave'), (0x1EA7, 'acircumflexgrave'),
    (0x1EA8, 'Acircumflexhookabove'), (0x1EA9, 'acircumflexhookabove'),
    (0x1EAA, 'Acircumflextilde'), (0x1EAB, 'acircumflextilde'),
    (0x1EAC, 'Acircumflexdotbelow'), (0x1EAD, 'acircumflexdotbelow'),
    (0x1EAE, 'Abreveacute'), (0x1EAF, 'abreveacute'),
    (0x1EB0, 'Abrevegrave'), (0x1EB1, 'abrevegrave'),
    (0x1EB2, 'Abrevehookabove'), (0x1EB3, 'abrevehookabove'),
    (0x1EB4, 'Abrevetilde'), (0x1EB5, 'abrevetilde'),
    (0x1EB6, 'Abrevedotbelow'), (0x1EB7, 'abrevedotbelow'),
    
    # E variants
    (0x1EB8, 'Edotbelow'), (0x1EB9, 'edotbelow'),
    (0x1EBA, 'Ehookabove'), (0x1EBB, 'ehookabove'),
    (0x1EBC, 'Etilde'), (0x1EBD, 'etilde'),
    (0x1EBE, 'Ecircumflexacute'), (0x1EBF, 'ecircumflexacute'),
    (0x1EC0, 'Ecircumflexgrave'), (0x1EC1, 'ecircumflexgrave'),
    (0x1EC2, 'Ecircumflexhookabove'), (0x1EC3, 'ecircumflexhookabove'),
    (0x1EC4, 'Ecircumflextilde'), (0x1EC5, 'ecircumflextilde'),
    (0x1EC6, 'Ecircumflexdotbelow'), (0x1EC7, 'ecircumflexdotbelow'),
    
    # I variants
    (0x1EC8, 'Ihookabove'), (0x1EC9, 'ihookabove'),
    (0x1ECA, 'Idotbelow'), (0x1ECB, 'idotbelow'),
    
    # O variants
    (0x1ECC, 'Odotbelow'), (0x1ECD, 'odotbelow'),
    (0x1ECE, 'Ohookabove'), (0x1ECF, 'ohookabove'),
    (0x1ED0, 'Ocircumflexacute'), (0x1ED1, 'ocircumflexacute'),
    (0x1ED2, 'Ocircumflexgrave'), (0x1ED3, 'ocircumflexgrave'),
    (0x1ED4, 'Ocircumflexhookabove'), (0x1ED5, 'ocircumflexhookabove'),
    (0x1ED6, 'Ocircumflextilde'), (0x1ED7, 'ocircumflextilde'),
    (0x1ED8, 'Ocircumflexdotbelow'), (0x1ED9, 'ocircumflexdotbelow'),
    (0x1EDA, 'Ohornacute'), (0x1EDB, 'ohornacute'),
    (0x1EDC, 'Ohorngrave'), (0x1EDD, 'ohorngrave'),
    (0x1EDE, 'Ohornhookabove'), (0x1EDF, 'ohornhookabove'),
    (0x1EE0, 'Ohorntilde'), (0x1EE1, 'ohorntilde'),
    (0x1EE2, 'Ohorndotbelow'), (0x1EE3, 'ohorndotbelow'),
    
    # U variants
    (0x1EE4, 'Udotbelow'), (0x1EE5, 'udotbelow'),
    (0x1EE6, 'Uhookabove'), (0x1EE7, 'uhookabove'),
    (0x1EE8, 'Uhornacute'), (0x1EE9, 'uhornacute'),
    (0x1EEA, 'Uhorngrave'), (0x1EEB, 'uhorngrave'),
    (0x1EEC, 'Uhornhookabove'), (0x1EED, 'uhornhookabove'),
    (0x1EEE, 'Uhorntilde'), (0x1EEF, 'uhorntilde'),
    (0x1EF0, 'Uhorndotbelow'), (0x1EF1, 'uhorndotbelow'),
    
    # Y variants
    (0x1EF2, 'Ygrave'), (0x1EF3, 'ygrave'),
    (0x1EF4, 'Ydotbelow'), (0x1EF5, 'ydotbelow'),
    (0x1EF6, 'Yhookabove'), (0x1EF7, 'yhookabove'),
    (0x1EF8, 'Ytilde'), (0x1EF9, 'ytilde'),

    # ── IPA Extensions (U+0250–U+02AF) ────────────────────────────
    (0x0250, 'aturned'),        (0x0251, 'ascript'),
    (0x0252, 'ascriptturned'),  (0x0253, 'bhook'),
    (0x0254, 'oopen'),          (0x0255, 'cstretchedcurl'),
    (0x0256, 'dtailretroflex'), (0x0257, 'dhook'),
    (0x0258, 'ereversed'),      (0x0259, 'schwa'),
    (0x025A, 'schwahook'),      (0x025B, 'eopen'),
    (0x025C, 'eopenreversed'),  (0x025D, 'eopenreversedhook'),
    (0x025E, 'eclosedreversed'),(0x025F, 'jdotless'),
    (0x0260, 'ghook'),          (0x0261, 'gscript'),
    (0x0262, 'Gsmall'),         (0x0263, 'ggamma'),
    (0x0264, 'ramshorns'),      (0x0265, 'hturned'),
    (0x0266, 'hhook'),          (0x0267, 'henghook'),
    (0x0268, 'istroke'),        (0x0269, 'iotalatin'),
    (0x026A, 'Ismall'),         (0x026B, 'lmiddletilde'),
    (0x026C, 'lbeltlateral'),   (0x026D, 'ltailretroflex'),
    (0x026E, 'lezh'),           (0x026F, 'mturned'),
    (0x0270, 'mlonglegturn'),   (0x0271, 'mhook'),
    (0x0272, 'nhookleft'),      (0x0273, 'ntailretroflex'),
    (0x0274, 'Nsmall'),         (0x0275, 'obarred'),
    (0x0276, 'OEsmall'),        (0x0277, 'omegaclosed'),
    (0x0278, 'phisymbol'),      (0x0279, 'rturned'),
    (0x027A, 'rlonglegturn'),   (0x027B, 'rhookturned'),
    (0x027C, 'rlongleg'),       (0x027D, 'rhooktail'),
    (0x027E, 'rfishhook'),      (0x027F, 'rfishhookreversed'),
    (0x0280, 'Rsmall'),         (0x0281, 'Rinverted'),
    (0x0282, 'shookretroflex'), (0x0283, 'esh'),
    (0x0284, 'dotlessjstroke'), (0x0285, 'eshsquiggle'),
    (0x0286, 'eshcurl'),        (0x0287, 'tturned'),
    (0x0288, 'ttailretroflex'), (0x0289, 'ubar'),
    (0x028A, 'upsilon'),        (0x028B, 'vhook'),
    (0x028C, 'vturned'),        (0x028D, 'wturned'),
    (0x028E, 'yturned'),        (0x028F, 'Ysmall'),
    (0x0290, 'zretroflex'),     (0x0291, 'zcurl'),
    (0x0292, 'ezh'),            (0x0293, 'ezhcurl'),
    (0x0294, 'glottalstop'),    (0x0295, 'glottalstopinv'),
    (0x0296, 'glottalstopreversed'), (0x0297, 'cstretched'),
    (0x0298, 'bilabialclick'),  (0x0299, 'Bsmall'),
    (0x029A, 'eopenbarred'),    (0x029B, 'Ghooktop'),
    (0x029C, 'Hsmall'),         (0x029D, 'jhook'),
    (0x029E, 'kturned'),        (0x029F, 'Lsmall'),
    (0x02A0, 'qhook'),          (0x02A1, 'glottalstopstroke'),
    (0x02A2, 'glottalstopstrokereversed'),
    (0x02A3, 'dzaltone'),       (0x02A4, 'dezh'),
    (0x02A5, 'dzcurl'),         (0x02A6, 'ts'),
    (0x02A7, 'tesh'),           (0x02A8, 'tccurl'),
    (0x02A9, 'fng'),            (0x02AA, 'lsretroflex'),
    (0x02AB, 'lzretroflex'),    (0x02AC, 'wwith'),
    (0x02AD, 'hhwith'),         (0x02AE, 'hturnedfishhook'),
    (0x02AF, 'hturnedfishhooktail'),
    # IPA suprasegmentals & modifier letters
    (0x02B0, 'hmodifier'),      (0x02B1, 'hhookmodifier'),
    (0x02B2, 'jmodifier'),      (0x02B3, 'rmodifier'),
    (0x02B4, 'rturnedmodifier'),(0x02B5, 'rhookmodifier'),
    (0x02B6, 'Rinvertedmodifier'), (0x02B7, 'wmodifier'),
    (0x02B8, 'ymodifier'),
    (0x02C8, 'vertlinelabove'), (0x02CC, 'vertlinebelow'),
    (0x02D0, 'trianglecolon'),  (0x02D1, 'halftriangcolon'),
    (0x02D8, 'breve'),          (0x02D9, 'dotaccent'),
    (0x02DA, 'ring'),           (0x02DB, 'ogonek'),
    (0x02DC, 'tildecomb'),      (0x02DD, 'hungarumlaut'),
    (0x02E0, 'ggammamodifier'), (0x02E1, 'lmodifier'),
    (0x02E2, 'smodifier'),      (0x02E3, 'xmodifier'),
    (0x02E4, 'glottalstopmodifier'),

    # ── Combining Diacritical Marks used in IPA ───────────────────
    (0x0300, 'combgrave'),      (0x0301, 'combacute'),
    (0x0302, 'combcircumflex'), (0x0303, 'combtilde'),
    (0x0304, 'combmacron'),     (0x0305, 'comboverline'),
    (0x0306, 'combbreve'),      (0x0307, 'combdotabove'),
    (0x0308, 'combdieresis'),   (0x0309, 'combhook'),
    (0x030A, 'combring'),       (0x030B, 'combhungarum'),
    (0x030C, 'combcaron'),      (0x030D, 'combvertline'),
    (0x030E, 'combdblvertline'),(0x030F, 'combdblgrave'),
    (0x0310, 'combcandrabindu'),(0x0311, 'combinvbreve'),
    (0x0316, 'combgravebel'),   (0x0317, 'combacutebel'),
    (0x031A, 'combleftangle'),  (0x031C, 'combhalfring'),
    (0x031F, 'combplus'),       (0x0320, 'combminussign'),
    (0x0324, 'combdieresisbel'),(0x0325, 'combringbel'),
    (0x0329, 'combverticline'), (0x032A, 'combbridge'),
    (0x032C, 'combcaron2'),     (0x032F, 'combinvbreve2'),
    (0x0330, 'combtildebel'),   (0x0331, 'combmacronbel'),
    (0x0334, 'combtildeovl'),   (0x0339, 'combrightring'),
    (0x033A, 'combinvbridge'),  (0x033B, 'combsqbelcomb'),
    (0x033C, 'combseagull'),    (0x033D, 'combxabove'),
    (0x0361, 'combtieabove'),

    # ── BQN primitive glyphs ──────────────────────────────────────
    (0x00A8, 'dieresis'),        (0x00AB, 'guillemotleft'),
    (0x00AC, 'logicalnot'),      (0x00AF, 'macron'),
    (0x00B0, 'degree'),          (0x00B1, 'plusminus'),
    (0x00B4, 'acute'),           (0x00B7, 'periodcentered'),
    (0x00BB, 'guillemotright'),  (0x00D7, 'multiply'),
    (0x00F7, 'divide'),          (0x03C0, 'pi'),
    (0x203F, 'undertie'),        (0x2026, 'ellipsis'),
    (0x207C, 'superscriptequal'),(0x2190, 'arrowleft'),
    (0x2191, 'arrowup'),         (0x2192, 'arrowright'),
    (0x2193, 'arrowdown'),       (0x2195, 'arrowboth'),
    (0x2196, 'arrownorthwest'),  (0x2199, 'arrowsouthwest'),
    (0x21A9, 'hookarrowleft'),   (0x21D0, 'arrowdblleft'),
    (0x220A, 'epsilonmath'),     (0x2206, 'increment'),
    (0x2207, 'gradient'),        (0x2218, 'ringoperator'),
    (0x221A, 'radical'),         (0x221E, 'infinity'),
    (0x2022, 'bullet'),          (0x2227, 'logicaland'),
    (0x2228, 'logicalor'),       (0x2229, 'intersection'),
    (0x222A, 'union'),           (0x223E, 'invertlazys'),
    (0x224D, 'asympeq'),         (0x2260, 'notequal'),
    (0x2261, 'equivalence'),     (0x2262, 'notidentical'),
    (0x2264, 'lessequal'),       (0x2265, 'greaterequal'),
    (0x2282, 'subset'),          (0x2283, 'superset'),
    (0x2286, 'subseteq'),        (0x2287, 'superseteq'),
    (0x2294, 'squareunion'),     (0x2296, 'circledminus'),
    (0x2298, 'circledivide'),    (0x228F, 'squareimage'),
    (0x2290, 'squareoriginal'),  (0x2291, 'squaresubset'),
    (0x2292, 'squaresuperset'),  (0x22A2, 'turnstile'),
    (0x22A3, 'turnstileleft'),   (0x22A4, 'top'),
    (0x22A5, 'perpendicular'),   (0x22B8, 'multimapright'),
    (0x22C4, 'diamondmath'),     (0x22C6, 'starmath'),
    (0x22C8, 'bowtie'),          (0x25CB, 'whitecircle'),
    (0x2308, 'lceil'),           (0x230A, 'lfloor'),
    (0x231C, 'topcornerleft'),   (0x233A, 'aplquadring'),
    (0x233D, 'aplcirclestile'),  (0x233E, 'aplcirclejot'),
    (0x233F, 'aplslashbar'),     (0x2336, 'aplibeam'),
    (0x2337, 'aplsquishquad'),   (0x2338, 'aplquadjot'),
    (0x2339, 'aplquaddivide'),   (0x2340, 'aplbackslashbar'),
    (0x2349, 'aplcirclebackslash'), (0x234B, 'aplupgrade'),
    (0x234E, 'aplexecute'),      (0x2352, 'apldowngrade'),
    (0x2355, 'aplformat'),       (0x2359, 'apldeltaunderbar'),
    (0x235C, 'aplcircleunderbar'), (0x235D, 'aplupshoe'),
    (0x235E, 'aplquotequad'),    (0x235F, 'aplstarring'),
    (0x2360, 'aplquadcolon'),    (0x2363, 'aplstarring2'),
    (0x2364, 'apljotdieresis'),  (0x2365, 'aplcircledieresis'),
    (0x2368, 'apltildedieresis'),(0x236A, 'aplcommabar'),
    (0x236B, 'apldeltilde'),     (0x236C, 'aplzilde'),
    (0x2371, 'aplnorcaret'),     (0x2372, 'aplnandcaret'),
    (0x2373, 'apliotasym'),      (0x2374, 'rho'),
    (0x2375, 'omega'),           (0x2377, 'aplzeta'),
    (0x2378, 'iotaunderbar'),    (0x237A, 'alpha'),
    (0x2389, 'circledring'),     (0x238A, 'circledx'),
    (0x2395, 'aplquad'),         (0x25F6, 'circleshadow'),
    (0x27DC, 'lefttriangleleft'),(0x27E8, 'anglebracketleft'),
    (0x27E9, 'anglebracketright'), (0x2A4A, 'dsjoin'),
    (0x235B, 'apljotunderbar'),  (0x2687, 'recyclesymbol'),

    # ── Box Drawing (U+2500–U+257F) ───────────────────────────────
    (0x2500, 'SF100000'), (0x2501, 'SF110000'), (0x2502, 'SF010000'), (0x2503, 'SF020000'),
    (0x2504, 'SF030000'), (0x2505, 'SF040000'), (0x2506, 'SF050000'), (0x2507, 'SF060000'),
    (0x2508, 'SF070000'), (0x2509, 'SF080000'), (0x250A, 'SF090000'), (0x250B, 'SF0A0000'),
    (0x250C, 'SF010100'), (0x250D, 'SF010200'), (0x250E, 'SF010300'), (0x250F, 'SF010400'),
    (0x2510, 'SF010500'), (0x2511, 'SF010600'), (0x2512, 'SF010700'), (0x2513, 'SF010800'),
    (0x2514, 'SF010900'), (0x2515, 'SF010A00'), (0x2516, 'SF010B00'), (0x2517, 'SF010C00'),
    (0x2518, 'SF010D00'), (0x2519, 'SF010E00'), (0x251A, 'SF010F00'), (0x251B, 'SF011000'),
    (0x251C, 'SF011100'), (0x251D, 'SF011200'), (0x251E, 'SF011300'), (0x251F, 'SF011400'),
    (0x2520, 'SF011500'), (0x2521, 'SF011600'), (0x2522, 'SF011700'), (0x2523, 'SF011800'),
    (0x2524, 'SF011900'), (0x2525, 'SF011A00'), (0x2526, 'SF011B00'), (0x2527, 'SF011C00'),
    (0x2528, 'SF011D00'), (0x2529, 'SF011E00'), (0x252A, 'SF011F00'), (0x252B, 'SF012000'),
    (0x252C, 'SF012100'), (0x252D, 'SF012200'), (0x252E, 'SF012300'), (0x252F, 'SF012400'),
    (0x2530, 'SF012500'), (0x2531, 'SF012600'), (0x2532, 'SF012700'), (0x2533, 'SF012800'),
    (0x2534, 'SF012900'), (0x2535, 'SF012A00'), (0x2536, 'SF012B00'), (0x2537, 'SF012C00'),
    (0x2538, 'SF012D00'), (0x2539, 'SF012E00'), (0x253A, 'SF012F00'), (0x253B, 'SF013000'),
    (0x253C, 'SF013100'), (0x253D, 'SF013200'), (0x253E, 'SF013300'), (0x253F, 'SF013400'),
    (0x2540, 'SF013500'), (0x2541, 'SF013600'), (0x2542, 'SF013700'), (0x2543, 'SF013800'),
    (0x2544, 'SF013900'), (0x2545, 'SF013A00'), (0x2546, 'SF013B00'), (0x2547, 'SF013C00'),
    (0x2548, 'SF013D00'), (0x2549, 'SF013E00'), (0x254A, 'SF013F00'), (0x254B, 'SF014000'),
    (0x254C, 'SF014100'), (0x254D, 'SF014200'), (0x254E, 'SF014300'), (0x254F, 'SF014400'),
    (0x2550, 'SF430000'), (0x2551, 'SF240000'), (0x2552, 'SF510000'), (0x2553, 'SF520000'),
    (0x2554, 'SF390000'), (0x2555, 'SF220000'), (0x2556, 'SF210000'), (0x2557, 'SF250000'),
    (0x2558, 'SF500000'), (0x2559, 'SF490000'), (0x255A, 'SF380000'), (0x255B, 'SF280000'),
    (0x255C, 'SF270000'), (0x255D, 'SF260000'), (0x255E, 'SF360000'), (0x255F, 'SF370000'),
    (0x2560, 'SF420000'), (0x2561, 'SF190000'), (0x2562, 'SF200000'), (0x2563, 'SF230000'),
    (0x2564, 'SF470000'), (0x2565, 'SF480000'), (0x2566, 'SF410000'), (0x2567, 'SF450000'),
    (0x2568, 'SF460000'), (0x2569, 'SF400000'), (0x256A, 'SF540000'), (0x256B, 'SF530000'),
    (0x256C, 'SF440000'), (0x256D, 'SF020100'), (0x256E, 'SF020200'), (0x256F, 'SF020300'),
    (0x2570, 'SF020400'), (0x2571, 'SF020500'), (0x2572, 'SF020600'), (0x2573, 'SF020700'),
    (0x2574, 'SF020800'), (0x2575, 'SF020900'), (0x2576, 'SF020A00'), (0x2577, 'SF020B00'),
    (0x2578, 'SF020C00'), (0x2579, 'SF020D00'), (0x257A, 'SF020E00'), (0x257B, 'SF020F00'),
    (0x257C, 'SF021000'), (0x257D, 'SF021100'), (0x257E, 'SF021200'), (0x257F, 'SF021300'),

    # ── Block Elements (U+2580–U+259F) ───────────────────────────
    (0x2580, 'uphalfblock'),     (0x2581, 'lowoneeighthblock'),
    (0x2582, 'lowtwoeighthsblock'), (0x2583, 'lowthreeeighthsblock'),
    (0x2584, 'lowhalfblock'),    (0x2585, 'lowfiveeighthsblock'),
    (0x2586, 'lowsixeighthsblock'), (0x2587, 'lowseveneighthsblock'),
    (0x2588, 'fullblock'),       (0x2589, 'leftsevenblock'),
    (0x258A, 'leftsixblock'),    (0x258B, 'leftfiveblock'),
    (0x258C, 'lefthalfblock'),   (0x258D, 'leftthreeblock'),
    (0x258E, 'lefttwoblock'),    (0x258F, 'leftoneeighthblock'),
    (0x2590, 'righthalfblock'),  (0x2591, 'lightshade'),
    (0x2592, 'mediumshade'),     (0x2593, 'darkshade'),
    (0x2594, 'uponeblock'),      (0x2595, 'righteighthblock'),
    (0x2596, 'quadrantlowerleft'), (0x2597, 'quadrantlowerright'),
    (0x2598, 'quadrantupperleft'), (0x2599, 'quadrantupperleftlowerleftlowerright'),
    (0x259A, 'quadrantupperleftlowerright'), (0x259B, 'quadrantupperleftupperright'),
    (0x259C, 'quadrantupperrightlowerright'), (0x259D, 'quadrantupperright'),
    (0x259E, 'quadrantupperleftlowerleft'), (0x259F, 'quadrantupperleftlowerrightall'),
]


# ============================================================
# SFD Font Structure Generator
# ============================================================

def make_sfd_header(font_name: str, ascent_em: int, descent_em: int,
                    ascent_px: int, descent_px: int, n_chars: int) -> str:
    """Generate the SFD header for a bitmap-only font."""
    return f"""SplineFontDB: 3.0
FontName: {font_name}
FullName: {font_name}
FamilyName: {font_name}
Weight: Medium
Copyright: Copyright 2026, Tini Font Project
UComments: "2026-08-06: Tiny pixel font with Vietnamese support"
Version: 001.000
ItalicAngle: 0
UnderlinePosition: -1
UnderlineWidth: 1
Ascent: {ascent_em}
Descent: {descent_em}
InvalidEm: 0
LayerCount: 2
Layer: 0 0 "Back" 1
Layer: 1 0 "Fore" 0
OS2Version: 0
OS2_WeightWidthSlopeOnly: 0
OS2_UseTypoMetrics: 1
CreationTime: 1785960576
ModificationTime: 1785960576
OS2TypoAscent: 0
OS2TypoAOffset: 1
OS2TypoDescent: 0
OS2TypoDOffset: 1
OS2TypoLinegap: 0
OS2WinAscent: 0
OS2WinAOffset: 1
OS2WinDescent: 0
OS2WinDOffset: 1
HheadAscent: 0
HheadAOffset: 1
HheadDescent: 0
HheadDOffset: 1
OS2Vendor: 'PfEd'
MarkAttachClasses: 1
DEI: 91125
Encoding: UnicodeBmp
UnicodeInterp: none
NameList: AGL For New Fonts
DisplaySize: {ascent_px + descent_px}
AntiAlias: 1
FitToEm: 0
WinInfo: 0 68 18
OnlyBitmaps: 1
BeginPrivate: 0
EndPrivate
BeginChars: 65536 {n_chars}
"""


def make_char_outline(name: str, cp: int, glyph_idx: int, width_em: int) -> str:
    """Generate the outline (vector) section for a bitmap-only char."""
    return f"""
StartChar: {name}
Encoding: {cp} {cp} {glyph_idx}
Width: {width_em}
VWidth: 0
Flags: W
LayerCount: 2
EndChar
"""


def make_bitmap_font_header(pixel_size: int, n_chars: int,
                            ascent_px: int, descent_px: int,
                            font_name: str) -> str:
    """Generate the BitmapFont section header."""
    return f"""BitmapFont: {pixel_size} {n_chars} {ascent_px} {descent_px} 1 {font_name}
BDFStartProperties: 13
FONT_ASCENT 18 {ascent_px}
FONT_DESCENT 18 {descent_px}
PIXEL_SIZE 18 {pixel_size}
RESOLUTION_X 19 75
RESOLUTION_Y 19 75
SPACING 16 "C"
FONT_NAME 16 "{font_name}"
WEIGHT_NAME 16 "medium"
SLANT 16 "r"
SETWIDTH_NAME 16 "normal"
CHARSET_REGISTRY 16 "ISO10646"
CHARSET_ENCODING 16 "1"
DEFAULT_CHAR 18 32
BDFEndProperties
Resolution: 75
"""


def make_empty_bdfchar(bdf_idx: int, cp: int, width_px: int) -> str:
    """Generate an empty BDFChar entry (no bitmap drawn)."""
    # Empty glyph: bounding box is zero-sized
    return f"BDFChar: {bdf_idx} {cp} {width_px} 0 0 0 -1\nz\n"


# ============================================================
# SFD File Generator
# ============================================================

def generate_sfd(font_name: str, width_px: int, ascent_px: int, descent_px: int,
                 output_path: str):
    """Generate an SFD file for a bitmap-only font with empty glyphs."""
    
    # Em units calculation: scale pixels to 1000 em units
    total_px = ascent_px + descent_px
    em_total = 1000
    ascent_em = round(ascent_px / total_px * em_total)
    descent_em = em_total - ascent_em
    
    # Width in em units
    width_em = round(width_px / total_px * em_total)
    
    # Sort glyphs by code point
    n_chars = len(CHARACTER_SET)
    
    lines = []
    
    # Header
    lines.append(make_sfd_header(font_name, ascent_em, descent_em,
                                  ascent_px, descent_px, n_chars))
    
    # Outline character sections (vector, required even for bitmap-only fonts)
    for glyph_idx, (cp, name) in enumerate(CHARACTER_SET):
        lines.append(make_char_outline(name, cp, glyph_idx, width_em))
    
    lines.append('EndChars\n')
    
    # Bitmap font section
    pixel_size = ascent_px + descent_px
    lines.append(make_bitmap_font_header(pixel_size, n_chars, ascent_px, descent_px, font_name))
    
    # BDFChar entries (all empty)
    for bdf_idx, (cp, name) in enumerate(CHARACTER_SET):
        lines.append(make_empty_bdfchar(bdf_idx, cp, width_px))
    
    lines.append('EndBitmapFont\n')
    lines.append('EndSplineFont\n')
    
    # Write with CRLF line endings
    content = ''.join(lines)
    # Normalize to CRLF
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    content_bytes = content.encode('utf-8').replace(b'\n', b'\r\n')
    
    with open(output_path, 'wb') as f:
        f.write(content_bytes)
    
    print(f"Generated: {output_path}")
    print(f"  Characters: {n_chars}")
    print(f"  Size: {len(content_bytes)} bytes")
    print(f"  All glyphs are empty - draw them manually in FontForge")


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    out_dir = r'C:\Users\Son\.sources\tini\src'
    os.makedirs(out_dir, exist_ok=True)
    
    print("Tini Font Structure Generator")
    print("=" * 60)
    print()
    
    # Generate tini5.sfd (5px wide, 10 ascent + 3 descent)
    print("Generating tini5.sfd...")
    generate_sfd(
        font_name='tini5',
        width_px=5,
        ascent_px=11,
        descent_px=3,
        output_path=os.path.join(out_dir, 'tini5.sfd')
    )
    print()
    
    # Generate tini4.sfd (4px wide, 10 ascent + 2 descent)
    print("Generating tini4.sfd...")
    generate_sfd(
        font_name='tini4',
        width_px=4,
        ascent_px=10,
        descent_px=2,
        output_path=os.path.join(out_dir, 'tini4.sfd')
    )
    
    print()
    print("=" * 60)
    print("Done! Generated empty font structures.")
    print("Open the .sfd files in FontForge to draw the glyphs manually.")
