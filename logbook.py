import re
import os
import json
import datetime
import pyperclip
from spellchecker import SpellChecker
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
class Notebook:
    def __init__(self,source=None) -> None:
        if source is None:
            self.source = {
                'cells':[]
            } 
        else:
            self.source = source

    def __str__(self) -> str:
        return str(self.source)
    
    def addCell(self,type,sources=None,index=None):
        temp =  {
            "cell_type":type,
            "metadata":{},
            "outputs":[],
            "source":[]
            }
        temp['source'] = sources if sources is not None else ''
        if index is not None:
            try:
                self.source['cells'][index] = temp
            except Exception as e:
                print(f'error, {e}')
        else:
            self.source['cells'].append(temp)
    
    @property
    def json(self):
        return json.dumps(self.source)
            
knownword = List(['ilt','bangkit','lusi','am','pm','ml','wita','coursera','dicoding','ss','th','st','nd','rd'])
spell = SpellChecker()
filename = 'logbook.ipynb'
filepath = os.path.join(os.getcwd(),filename)

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

def addNewWeek():
    now = datetime.datetime.now()
    hari = now.weekday()
    monday = now.day - hari
    bulan = now.month

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
            

    this_monday = datetime.datetime(2023,bulan,monday).strftime('%b%d')
    if last_monday == this_monday:
        print("this week's logbook already generated")
        return
    
    next_week = int(re.search(r'[\d]+',Weeks[-1]).group()) + 1

    with open(filepath,'w') as f:
        ipymb = Notebook(json_)
        ipymb.addCell('markdown',[f'### Week {next_week}'])
        for i in range(5):
            date = datetime.datetime(2023,bulan,monday+i).strftime('%b%d')
            ipymb.addCell('code',[
                f"{date} = logbook.write(''' ''', type_='daily')"
            ])
        ipymb.addCell('code',[f"weeklyReport{next_week} = logbook.write(''' ''')"])
        f.write(ipymb.json)

if __name__ == '__main__':
    
    pass


