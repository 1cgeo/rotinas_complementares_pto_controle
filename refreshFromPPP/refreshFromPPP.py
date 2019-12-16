import os
import re
from datetime import datetime, date
from pathlib import Path

import psycopg2
import PyPDF2

class RefreshFromPPP():

    def __init__(self, folder):
        self.folder = Path(folder)
        self.conn = psycopg2.connect("host='localhost' port='5432' dbname='pto_controle' user='postgres' password='postgres'")

    def readPPP(self):
        files = [x for x in self.folder.rglob('*.pdf') if '6_Processamento_PPP' in x.parts]
        for item in files:
             with item.open(mode='rb') as pdffile:
                read_pdf = PyPDF2.PdfFileReader(pdffile)
                page = read_pdf.getPage(0)
                page_content = page.extractText()
                page_pdf = page_content.replace('\n', '')
                aElip, n, e = re.findall(
                    r'([0-9]{1,},[0-9]{1,2})([0-9]{7}[.][0-9]{3})([0-9]{6}[.][0-9]{3})', page_pdf)[1]
                point = re.findall(r'domarco:(.+)Início', page_pdf)[0]
                self.updateDB(point, n, e, aElip.replace(',', '.'))

    def updateDB(self, point, n, e, aElip):
        with self.conn.cursor() as cursor:
            cursor.execute(u'''
            UPDATE bpc.ponto_controle_p
            SET n='{0}', e='{1}', aElip='{2}'
            WHERE cod_ponto='{3}'
            '''.format(n, e, aElip, point))
            return cursor.commit()