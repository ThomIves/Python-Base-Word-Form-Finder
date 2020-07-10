from word_forms.word_forms import get_word_forms
import pprint

pp = pprint.PrettyPrinter(indent=2)

w_list = [
    'chemical', 'chemically', 'electricals', 'electrical', 'fda', 'ul',
    'processability', 'resistant', 'processing', 'resistance',
    'resistivity', 'thermally', 'thermodynamics', 'thermodynamic',
    'flammability', 'gubber', 'recyclable', 'compostable',
    "softening", "processed", "divided", "light", "park", "contained",
    "reduce", "human", "entrust", "personnel", 'entrustable', 'reduceable',
    'thermodynamically']

for w in w_list:
    print(f'{w}:')
    aD = get_word_forms(w)
    aL = []
    for k in aD.keys():
        aL += list(aD[k])
    # pp.p
    print(aL)
