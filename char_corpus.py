# Character-level training data 
CHARACTER_PATTERNS = [
    # Common Xhosa prefixes 
    "umu", "aba", "imi", "ama", "isi", "izi", "ubu", "uku", "ili",
    "umu", "aba", "imi", "ama", "isi", "izi", "ubu", "uku", "ili",
    "umu", "aba", "imi", "ama", "isi", "izi", "ubu", "uku", "ili",
    
    # Common Xhosa suffixes  
    "ntu", "ndo", "mbi", "nci", "nca", "nka", "nga", "nqa", "nta",
    "ntu", "ndo", "mbi", "nci", "nca", "nka", "nga", "nqa", "nta",
    "ntu", "ndo", "mbi", "nci", "nca", "nka", "nga", "nqa", "nta",
    
    # Common character sequences
    "ndi", "ngu", "ku", "ba", "pha", "tha", "sha", "nya", "mba",
    "ndi", "ngu", "ku", "ba", "pha", "tha", "sha", "nya", "mba",
    "ndi", "ngu", "ku", "ba", "pha", "tha", "sha", "nya", "mba",
    
    # Verb prefixes and suffixes
    "eli", "eni", "ini", "oni", "uni", "athi", "ethi", "ithi",
    "eli", "eni", "ini", "oni", "uni", "athi", "ethi", "ithi",
    "eli", "eni", "ini", "oni", "uni", "athi", "ethi", "ithi",
    
    # Common word roots and stems
    "ando", "endo", "indo", "ondo", "undo", "anga", "enga", "inga",
    "ando", "endo", "indo", "ondo", "undo", "anga", "enga", "inga",
    "ando", "endo", "indo", "ondo", "undo", "anga", "enga", "inga",
    
    # Additional common patterns
    "ntu", "nto", "nke", "nqa", "nca", "nxa", "nka", "nda", "nte",
    "ntu", "nto", "nke", "nqa", "nca", "nxa", "nka", "nda", "nte",
    "ntu", "nto", "nke", "nqa", "nca", "nxa", "nka", "nda", "nte",
    
    # Vowel combinations and sequences
    "ae", "ei", "ou", "au", "oi", "io", "ua", "ue", "ui", "uo",
    "ae", "ei", "ou", "au", "oi", "io", "ua", "ue", "ui", "uo",
    "ae", "ei", "ou", "au", "oi", "io", "ua", "ue", "ui", "uo",
    
    # Consonant-vowel patterns
    "ma", "me", "mi", "mo", "mu", "na", "ne", "ni", "no", "nu",
    "pa", "pe", "pi", "po", "pu", "qa", "qe", "qi", "qo", "qu",
    "ra", "re", "ri", "ro", "ru", "sa", "se", "si", "so", "su",
    "ta", "te", "ti", "to", "tu", "va", "ve", "vi", "vo", "vu",
    "wa", "we", "wi", "wo", "wu", "xa", "xe", "xi", "xo", "xu",
    "ya", "ye", "yi", "yo", "yu", "za", "ze", "zi", "zo", "zu",
    
    # Double consonant patterns
    "bba", "bbe", "bbi", "bbo", "bbu", "dda", "dde", "ddi", "ddo", "ddu",
    "ffa", "ffe", "ffi", "ffo", "ffu", "gga", "gge", "ggi", "ggo", "ggu",
    "kka", "kke", "kki", "kko", "kku", "lla", "lle", "lli", "llo", "llu",
    "mma", "mme", "mmi", "mmo", "mmu", "nna", "nne", "nni", "nno", "nnu",
    "ppa", "ppe", "ppi", "ppo", "ppu", "qqa", "qqe", "qqi", "qqo", "qqu",
    "rra", "rre", "rri", "rro", "rru", "ssa", "sse", "ssi", "sso", "ssu",
    "tta", "tte", "tti", "tto", "ttu", "vva", "vve", "vvi", "vvo", "vvu",
    "wwa", "wwe", "wwi", "wwo", "wwu", "xxa", "xxe", "xxi", "xxo", "xxu",
    "yya", "yye", "yyi", "yyo", "yyu", "zza", "zze", "zzi", "zzo", "zzu",
    
    # Nasal combinations
    "mba", "mbe", "mbi", "mbo", "mbu", "nda", "nde", "ndi", "ndo", "ndu",
    "nga", "nge", "ngi", "ngo", "ngu", "nka", "nke", "nki", "nko", "nku",
    "nqa", "nqe", "nqi", "nqo", "nqu", "nxa", "nxe", "nxi", "nxo", "nxu",
    "nca", "nce", "nci", "nco", "ncu", "nza", "nze", "nzi", "nzo", "nzu",
    
    # Click sounds patterns
    "cwa", "cwe", "cwi", "cwo", "cwu", "xha", "xhe", "xhi", "xho", "xhu",
    "qha", "qhe", "qhi", "qho", "qhu", "gqa", "gqe", "gqi", "gqo", "gqu",
    
    # Common word endings
    "eni", "ini", "oni", "uni", "weni", "yeni", "kazi", "ana", "ele",
    "ile", "ise", "eka", "aku", "emi", "eni", "ini", "oni", "uni",
    "weni", "yeni", "kazi", "ana", "ele", "ile", "ise", "eka", "aku",
    "emi", "eni", "ini", "oni", "uni", "weni", "yeni", "kazi", "ana"
]

COMMON_XHOSA_WORDS = [
    "mholo", "unjani", "ndiyaphila", "enkosi", "kakhulu", "igama",
    "lam", "ngu", "thandi", "sipho", "nomsa", "vela", "phi", "ekapa",
    "egoli", "hlala", "sebenza", "funda", "skolo", "sikolo", "sapho",
    "lwam", "lulungile", "wamkelekile", "shiyeka", "hamba", "kakuhle",
    "thanda", "ntoni", "kulungile", "yazi", "thetha", "isingesi",
    "ndiya", "edolophini", "ukutya", "ixesha", "li", "shushu",
    "imvula", "itiye", "ibhola", "iminyaka", "ima", "uzalwe", "nini",
    "go", "meyi", "bazali", "bobabini", "bantwana", "babini", "bathathu",
    "babhadlile", "bathanda", "xhela", "mnike", "isipho", "fundisa",
    "khulisa", "imoto", "yakho", "yithenge", "nxiba", "yinxibe",
    "iimpahla", "ezintle", "zithengele", "zibize", "zithande", "zinxibe",
    "zihlambe", "zithengise", "zitshintshe", "zibhale", "zifunde",
    "ziyathetha", "ziyabona", "ziyava", "ziyacinga", "ziyafuna", "ziyakhonza",
    "ziyabulala", "ziyasinda", "ziyaphilisa", "ziqeqeshe", "zifundise",
    "zikhulule", "zivule", "zivale", "zibophe", "zisike", "zibambe",
    "nam", "uneminyaka", "ndineminyaka", "ndalwa", "usapho", "unabazali",
    "unabantwana", "abantwana", "bafunda", "bayathanda", "ndiyayixhela",
    "ndiyamnika", "ndiyamfundisa", "ndiyamkhulisa", "ndiyayithanda",
    "ndiyayithenga", "ndiyayinxiba", "ndiyazithengela", "ndiyazikhalela",
    "ndiyazihlamba", "ndiyazithengisa", "ndiyazitshintsha", "ndiyazibhala",
    "ndiyazifunda", "ndiyathetha", "ndizibona", "ndizokuva", "ndiyazicingela",
    "ndiyazifuna", "ndiyazikhonza", "ndiyazibulala", "ndiyakusinda", "ndiyaziphilisa",
    "ndiyaziqeqesha", "ndizifundisa", "ndizikhulula", "ndiyazivula", "ndiyazivala",
    "ndiyazibopha", "ndiyazisika", "ndiyazibamba", "andiyidlali", "andimxeleli",
    "andizithengisi", "andizikhonzi", "andizibulali", "andizisiki",
    "andizibopi", "ayibandi", "ndinomntwana", "ndinabantwana", "ndinemoto",
    "ndineempahla", "ndinesikolo", "ndinosapho", "ndinelizwe", "ndinamandla",
    "ndinamaxesha", "ndinamathuba", "ndinoluvo", "ndinamava", "ndinamanga",
    "ndinamanzi", "ndinamasi", "ndinamafutha", "ndinamalahle", "ndinesonka"
]

def get_char_corpus():
    """Get corpus for character-level N-gram training"""
    patterns_text = " ".join(CHARACTER_PATTERNS)
    words_text = " ".join(COMMON_XHOSA_WORDS)
    return patterns_text + " " + words_text

def get_char_list():
    """Get characters as list for training"""
    return list(get_char_corpus())