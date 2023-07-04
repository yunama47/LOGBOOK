import re
import json
import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf(filename, title, additional_info, table_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [
                ('GRID', (0,0), (-1,-1), 0.75, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('VALIGN', (0,0), (0,-1), 'MIDDLE'),
                ('ALIGN', (0,0), (0,-1), 'CENTER'),
                ('ALIGN', (1,0), (-1,-1), 'LEFT'),
                ('ALIGN', (1,0), (-1,-1), 'LEFT')
                ]
  report_table = Table(data=table_data, style=table_style, hAlign="LEFT")
  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table])


with open('logbook.ipynb') as f:
    J = json.load(f)

iterator = enumerate(J['cells'])
pattern = r"(^[A-Za-z]+[0-9]{1,2}) = logbook.write\(('''[A-Za-z 0-9!\"#$%&\'()*+,-./:;<=>?@^_`{|}~]+''')"
bulan = {
    'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7
}

next(iterator)
logbook_harian = [['Tanggal','Logbook']]
logbook_mingguan = [['Minggu','Logbook']]
for i,cell in iterator:
    if cell['cell_type']=='markdown':
        print('[INFO] skipped markdown cell at',i)
        continue
    try:
        text = '<br/>'.join([s.strip() for s in cell['source']])
        petik = '\'\'\''
        key, logbook = re.search(pattern,text).groups()
        logbook = logbook.strip(petik)
        if 'weekly' in key:
            logbook_mingguan.append([f"Minggu {key[-2:]}",Paragraph(logbook)])
        else:
            month = bulan[key[:3]]
            day = int(key[3:])
            logbook_harian.append([datetime.date(2023,month,day).strftime('%d-%m-%Y'),
                                   Paragraph(logbook)])
    except Exception as e:
        print('[ERROR]',e,'at',i)

generate_pdf('logbook harian.pdf',
             'Kampus Merdeka Logbook',
             'Gede Wahyu Purnama <br/> 2015101014 <br/> Ilmu Komputer Universitas Pendidikan Ganesha',
             logbook_harian
             )