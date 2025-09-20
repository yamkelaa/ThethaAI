XHOSA_GREETINGS = [
    "Molo", "Molo unjani", "Ninjani", "Molweni", "Unjani", "Ndiphilile", 
    "Ndiyaphila", "Enkosi", "Wena unjani", "Kulungile", "Ewe", "Hayi",
    "Sawubona", "Hallo", "Lotjhani", "Avuxeni"
]

XHOSA_QUESTIONS = [
    "Uvela phi", "Uhlala phi", "Uyasebenza", "Ufunda phi", "Usapho lwakho ulungile",
    "Ixesha lantoni", "Kuyabanda", "Kushushu", "Uyathanda imidlalo", "Igama lakho ngubani",
    "Uyaxoka", "Uyayithanda imvula", "Uyadlala ibhola", "Uyasela itiye"
]

XHOSA_RESPONSES = [
    "Ndivela eKapa", "Ndivela eGoli", "Ndihlala eKapa", "Ewe ndiyasebenza", 
    "Hayi andisebenzi", "Ndiyafunda eYunivesithi", "Ewe usapho luthi", 
    "Ixesha li", "Ewe kuyabanda", "Hayi akubandanga", "Ewe kushushu", 
    "NdinguThandi", "NdinguSipho", "NdinguZanele", "NginguBongani",
    "Andixoki", "Ewe ndiyayithanda imvula", "Hayi andiyithandi imvula",
    "Ewe ndiyayidlala ibhola", "Ewe ndiyasela itiye"
]

XHOSA_CONVERSATIONS = [
    ["Molo", "Molo unjani", "Ndiphilile enkosi wena unjani", "Ndiyaphila enkosi"],
    ["Unjani", "Ndiyaphila enkosi wena unjani", "Ndiyaphila"],
    ["Igama lakho ngubani", "NginguThandi wena", "NginguSipho"],
    ["Uvela phi", "Ndivela eKapa wena uvela phi", "Ndivela eGoli"],
    ["Uyasebenza", "Ewe ndiyasebenza wena", "Hayi andisebenzi"],
    ["Ufunda phi", "Ndiyafunda eYunivesithi wena", "Andifundi"],
    ["Usapho lwakho ulungile", "Ewe usapho luthi enkosi"],
    ["Ixesha lantoni", "Ixesha li-3", "Enkosi"],
    ["Kuyabanda namhlanje", "Hayi akubandanga kakhulu"],
    ["Uyathanda imidlalo", "Ewe ndiyayithanda wena", "Hayi andiyithandi"],
    ["Sawubona", "Sawubona unjani", "Ngikhona wena", "Ngikhona"],
    ["Hallo", "Hallo unjani", "Ndiphilile wena", "Ndiyaphila"]
]


XHOSA_CHARACTER_PATTERNS = [
    "ndi", "ngu", "ku", "ba", "pha", "tha", "sha", "nya", "mba", "ntu",
    "mfu", "nqa", "nca", "nxa", "nka", "nga", "nza", "nwa", "nja", "eli",
    "eni", "ini", "oni", "uni", "athi", "ethi", "ithi", "othi", "uthi",
    "ando", "endo", "indo", "ondo", "undo", "anga", "enga", "inga", "onga",
    "unga", "abo", "ebo", "ibo", "obo", "ubo", "aka", "eka", "ika", "oka",
    
    "ni", "phi", "thi", "la", "sa", "za", "wa", "ja", "ka", "bo",
    "go", "ho", "ko", "lo", "ma", "na", "pa", "qa", "ra", "ta",
    
    "umu", "aba", "imi", "ama", "isi", "izi", "ubu", "uku", "ili", "iwi",
    
    "ntu", "nto", "nke", "nqa", "nca", "nxa", "nka", "nda", "nte", "nse"
]

def get_training_data():
    """Return all training data as a single text corpus"""
    all_text = []
    
    # Add individual words and phrases
    all_text.extend(XHOSA_GREETINGS)
    all_text.extend(XHOSA_QUESTIONS)
    all_text.extend(XHOSA_RESPONSES)
    
    # Add conversation lines
    for conv in XHOSA_CONVERSATIONS:
        all_text.extend(conv)
    
    return " ".join(all_text)

def get_word_level_corpus():
    """Return corpus for word-level training"""
    corpus = get_training_data()
    return corpus.split()

def get_char_level_corpus():
    """Return corpus for character-level training - enhanced with Xhosa patterns"""
    corpus = get_training_data()
    
    # Convert to character list
    char_corpus = list(corpus)
    
    # Add Xhosa character patterns multiple times to reinforce learning
    for pattern in XHOSA_CHARACTER_PATTERNS:
        # Add each pattern 3 times to increase its weight in training
        char_corpus.extend(list(pattern))
        char_corpus.extend(list(pattern))
        char_corpus.extend(list(pattern))
    
    # Add common punctuation and whitespace patterns
    punctuation = ['.', ',', '?', '!', ' ', ' ']  # Extra spaces for better separation
    char_corpus.extend(punctuation)
    
    return char_corpus