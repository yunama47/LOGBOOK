import re
import string
from spellchecker import SpellChecker

spell = SpellChecker()

def words_counter(text,type_='weekly'):
    '''
    This function used to count the number of words in the text given on the parameter.
    '''
    assert isinstance(text,str) ,"parameter must be string"
    maxw = 150 if (type_ == 'weekly') else 50
    minw = 100 if (type_ == 'weekly') else 20

    text = text.translate(str.maketrans("","",string.punctuation 
                                            + string.digits))
    words = re.findall(r'\w+',text)
    misspelled = spell.unknown(words) or "None"
    print(f'number of words is {len(words)} ,should be between {minw} - {maxw} words')
    print('words that may be misspelled : ',misspelled)
    return words


    