# Enhanced fake Xhosa dataset
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
    """Return corpus for character-level training"""
    corpus = get_training_data()
    return list(corpus)