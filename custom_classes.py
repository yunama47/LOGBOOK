import json
import datetime

class Datetime(datetime.datetime):
    def next_day(self):
        '''return the next day'''
        year = self.year
        month = self.month
        day = self.day
        try:
            return Datetime(year,month,day + 1)
        except ValueError:
            return Datetime(year,month+1,1)
        
    def max_day(year,month, day=31):
        '''return the maximum day of the month'''
        try:
            Datetime(year,month, day)
            return day
        except ValueError:
            return Datetime.max_day(year,month, day-1)
        
    def week_monday(self):
        '''return monday date of the week'''
        hari = self.weekday()
        senin = self.day - hari
        if hari == 0:
            return self
        else:
            if senin > 0:
                return Datetime(self.year,self.month,senin)
            elif senin <= 0:
                max_day = Datetime.max_day(self.year,self.month-1)
                return Datetime(self.year,self.month-1,max_day+senin)
        
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