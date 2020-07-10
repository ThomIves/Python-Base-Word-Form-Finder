import nltk

ENGLISH_WORDS = nltk.corpus.words.words()

ml = [
    "processability",
    "resistant",
    "processing",
    "resistance",
    "resistivity",
    "thermally",
    "thermodynamics",
    "thermodynamic",
    "flammability"]

for word in ml:
    found = word in ENGLISH_WORDS
    if found:
        case = ''
    else:
        case = 'NOT '
    print(f'{word} is {case}an English word.')
