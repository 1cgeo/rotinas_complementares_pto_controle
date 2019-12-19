import os
import re
import sys
from datetime import datetime, date
from pathlib import Path

import psycopg2
import PyPDF2

class RefreshFromPPP():

    def __init__(self, path, host, port, db_name, user, password):
        self.folder = Path(path)
        self.conn = psycopg2.connect("host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(host, port, db_name, user, password))

    def readPPP(self):
        # Possibility : update the timestamp of measure's beginning from PPP and orbita(has domain)
        files = [x for x in self.folder.rglob('*.pdf') if '6_Processamento_PPP' in x.parts]
        for item in files:
             with item.open(mode='rb') as pdffile:
                point = {}
                read_pdf = PyPDF2.PdfFileReader(pdffile)
                page = read_pdf.getPage(0)
                page_content = page.extractText()
                page_pdf = page_content.replace('\n', '')
                point['altitude_geometrica'], point['norte'], point['leste'] = re.findall(
                    r'([0-9]{1,},[0-9]{1,2})([0-9]{7}[.][0-9]{3})([0-9]{6}[.][0-9]{3})', page_pdf)[1]
                point['altitude_geometrica'] = point['altitude_geometrica'].replace(',', '.')
                point['altitude_ortometrica'] = re.findall(r'Ortométrica\(m\)(.{1,7})Precis', page_pdf)[0].replace(',', '.')
                point['cod_ponto'] = re.findall(r'domarco:(.+)Início', page_pdf)[0]
                point['orbita'] = re.findall(r'dossatélites:\d(\w+)Frequ', page_pdf)[0].capitalize()
                point['freq_processada'] = re.findall(r'Frequênciaprocessada:(\w+)Interva', page_pdf)[0]
                data = re.findall(r'Processadoem:(\d\d/\d\d/\d\d\d\d)', page_pdf)[0]
                point['data_processamento'] = datetime.strptime(data, '%d/%m/%Y')
                lat, lon = re.findall(r'levantamento5(.{2,3}°.{2}´.{7}).(.{2,3}°.{2}´.{7})', page_pdf)[0]
                point['latitude'], point['longitude'] = self.evaluateCoords(lat, lon)
                print(point)
                self.updateDB(point)

    def updateDB(self, point):
        with self.conn.cursor() as cursor:
            cursor.execute(u'''
            UPDATE bpc.ponto_controle_p
            SET norte='{norte}', leste='{este}', altitude_geometrica='{altitude_geometrica}', altitude_ortometrica='{altitude_ortometrica}',
            freq_processada='{freq_processada}', latitude='{latitude}', longitude='{longitude}', geom=ST_GeomFromText('POINT({latitude} {longitude})', 4674),
            data_processamento='{data_processamento}'
            WHERE cod_ponto='{cod_ponto}'
            '''.format(**point))
            self.conn.commit()
    
    @staticmethod
    def evaluateCoords(lat, lon):
        lat_deg, lat_min, lat_seg = re.findall(r'(.{2,3})°(\d\d)´(.{7})', lat)[0]
        new_lat = float(lat_deg) + float(lat_min)/60 + float(lat_seg.replace(',', '.'))/3600
        lon_deg, lon_min, lon_seg = re.findall(r'(.{2,3})°(\d\d)´(.{7})', lon)[0]
        new_lon = float(lon_deg) + float(lon_min)/60 + float(lon_seg.replace(',', '.'))/3600
        return new_lat, new_lon


if __name__ == "__main__":
    test = RefreshFromPPP*sys.argv[1:])
    test.readPPP()