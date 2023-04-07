import re
from spellchecker import SpellChecker
import pyperclip

from tkinter import *
from tkinter import messagebox

class List (list):
    def __sub__(self,other_list):
        for x in other_list:
            if x in self:
                self.remove(x)
        return self
class String(str):
    def flatten(self):
        return " ".join([line.strip() for line in self.splitlines()])
    def typograf(self):
        return "\n".join([line.strip() for line in self.splitlines()])
        
knownword = List(['ilt','bangkit','lusi','am','pm','ml','wita','coursera','dicoding','ss','th','st','nd','rd'])
spell = SpellChecker()

def write(text,type_='weekly'):
    '''
    This function used to count the number of words in the text given on the parameter.
    '''
    assert isinstance(text,str) ,"parameter must be string"
    maxw = 150 if (type_ == 'weekly') else 50
    minw = 100 if (type_ == 'weekly') else 20
    text = String(text)
    words = re.findall(r'[^0-9!"#$%&\'()*+,-./:;<=>?@^_`{|}~\\\[\] ]+',text.flatten())
    misspelled = List(spell.unknown(words)) - knownword or "None"
    res = f'number of words is {len(words)} ,should be between {minw} - {maxw} words\nwords that may be misspelled : {misspelled}'
    pyperclip.copy(text.flatten())
    print(res)
    return res

if __name__ == '__main__':
    Text_ = String('''Today i have 2 activity from bangkit. One is mandatory and the other one is not mandatory
                        10:00-11:00(WITA) - [Mandatory] I did the english pre-test from bangkit.
                        16:30-18:00(WITA) - [Non-Mandatory] I joined guest speaker session #1 at bangkit youtube channel''')

    # print(spell.split_words(Text_))
    print(Text_.typograf())
    print(re.findall(r'[^0-9!"#$%&\'()*+,-./:;<=>?@^_`{|}~\\\[\] ]+',Text_.typograf()))
    pass


