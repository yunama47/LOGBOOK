import re
import os
import json
import pyperclip
from spellchecker import SpellChecker
from custom_classes import Datetime, List, String, Notebook
            
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

def addNewWeek(filename:str='logbook.ipynb',monday:Datetime=None):
    filepath = os.path.join(os.getcwd(),filename)
    now = Datetime.now()
    with open(filepath,'r') as f:
        json_ = json.load(f)
        Weeks = list(filter(lambda x: x['cell_type']=='markdown', json_['cells']))
        Weeks = list(map(lambda x: x['source'][0],Weeks))
        code_cells = list(filter(lambda x: x['cell_type']=='code', json_['cells']))
        code_cells = list(map(lambda x: x['source'],code_cells))
        last_monday = ''
        for i in range(-2,-10,-1): 
            if 'weeklyReport' in (code_cells[i][0]):
                last_monday = code_cells[i+1][0][:5]
                break
    start_day = now.week_monday() if monday is None else monday #start from monday
    this_monday = start_day.strftime('%b%d') 
    next_week = int(re.search(r'[\d]+',Weeks[-1]).group()) + 1
    if last_monday == this_monday:
        print("this week's logbook already generated")
        return start_day,next_week, json_, (last_monday == this_monday)
    with open(filepath,'w') as f:
        ipymb = Notebook(json_)
        ipymb.addCell('markdown',[f'### Week {next_week}'])
        for i in range(5):
            ipymb.addCell('code',[
                f"{start_day.strftime('%b%d')} = logbook.write(''' ''', type_='daily')"
            ])
            start_day = start_day.next_day()
        ipymb.addCell('code',[f"weeklyReport{next_week} = logbook.write(''' ''')"])
        f.write(ipymb.json)

if __name__ == '__main__':
    
    pass


