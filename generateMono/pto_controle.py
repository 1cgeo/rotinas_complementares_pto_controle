# coding=utf-8

import csv
import os
import re
from datetime import datetime
from pathlib import Path

import psycopg2
import psycopg2.extras
import PyPDF2
from secretary import Renderer

class GenerateMonograpy():

    def __init__(self):
        self.conn = psycopg2.connect("host='localhost' port='5433' dbname='pto_controle' user='postgres' password='postgres'")
        self.path = Path('C:\\Users\\eliton.1CGEO\\Desktop\\2018-05-01')
        self.points = []
        super().__init__()
    
    def fetch(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(u'''
            SELECT * FROM bpc.ponto_controle_p
            ''')
            # for result in cursor:
            #     print(result)
            return cursor.fetchall()

    def getDataFromStrucuture(self):
        for dirpath, dirname, filename in os.walk(self.path):
            pass


    def executeProcess(self):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', self.path.name):
            pass
        
    def getListOfPoints(self):
        data = self.fetch()
        self.points.append(map(lambda x: item['cod_ponto'] for item in x), data)
        for point in self.points:
            print(point)
    # CSV exportado do banco, atentar para o índice da coluna (row[])
    # with open('C:\\Users\\eliton.1CGEO\\Desktop\\test\\final.csv') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     for row in reader:
    #         pto = {}
    #         pto['nome'] = row[0]
    #         pto['medidor'] = row[1]
    #         if '3 Sgt' or '2 Sgt' or '1 Sgt' in pto['medidor']:
    #             pto['medidor'] = pto['medidor'].replace(' Sgt', u'° Sgt')

            # ######### FIX NAMES ###############
            # if 'Joao' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Joao', u'João')
            # if 'Glenio' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Glenio', u'Glênio')
            # if 'Mendonca' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Mendonca', u'Mendonça')
            # if 'Marcio' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Marcio', u'Márcio')
            # if 'Andre' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Andre', u'André')
            # if 'Cesar' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Cesar', u'César')
            # if 'Aurelio' in pto['medidor']:
            #     pto['medidor'] = pto['medidor'].replace('Aurelio', u'Aurélio')

            # pto['dataMono'] = '21/10/2019'
            # if row[6] == 'Medição B' or row[6] == 'Treinamento B':
            #     pto['chCampo'] = u'José Eliton Albuquerque Filho - 1º TEN QEM'
            #     pto['chCampoCREA'] = u'RS231681'
            #     # por algum bug na secretary durante a inserção das imagens é necessário duas imagens idênticas
            #     pto['signature'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\eliton2.jpg'
            #     pto['signature1'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\eliton.jpg'
            #     pto['signature2'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\eliton.jpg'
            #     pto['signature3'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\eliton.jpg'
            # if row[6] == 'Medição A' or row[6] == 'Treinamento A':
            #     pto['chCampo'] = u'Diogo Oliveira Nascimento - CAP QEM'
            #     pto['chCampoCREA'] = u'RJ12129041'
            #     pto['signature'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\diogo_sign.jpg'
            #     pto['signature1'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\diogo_sign.jpg'
            #     pto['signature2'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\diogo_sign.jpg'
            #     pto['signature3'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\diogo_sign.jpg'

            # with open(u'C:\\Users\\eliton.1CGEO\\Desktop\\Pontos_Medidos\\_points\\{0}\\6_Processamento_PPP\\{0}.18o.pdf'.format(pto['nome']), 'rb') as pdffile:
            #     read_pdf = PyPDF2.PdfFileReader(pdffile)
            #     page = read_pdf.getPage(0)
            #     page_content = page.extractText()
            #     page_pdf = page_content.encode('utf-8').replace('\n', '')

            # #     # Altitude elipsoidal, N e E on 2 => 0,1,2
            #     pto['aElip'], pto['n'], pto['e'] = re.findall(
            #         r'([0-9]{1,},[0-9]{1,2})([0-9]{7}[.][0-9]{3})([0-9]{6}[.][0-9]{3})', page_pdf)[1]
            #     pto['n'] = pto['n'].replace('.', ',')
            #     pto['e'] = pto['e'].replace('.', ',')

            #     # Altitude ortometrica on 1
            #     pto['aOrt'] = re.findall(
            #         r'(trica\(m\))([0-9]{1,},[0-9]{2})', page_pdf)[0][1]

            #     # Sigmas on 1 e 2
            #     # pto['sigmaXY'], pto['sigmaZ'] = re.findall(
            #     #     r'(Sigma\(95%\)6\(m\))(\d,\d{3})(\d,\d{3})', page_pdf)[0][1:3]

            #     pto['sigmaXY'] = u'0,11'
            #     pto['sigmaZ'] = u'0,18'

            #     # Data e hora do processamento em 1 e 2
            #     pto['dataPPP'] = re.findall(
            #         r'(Processadoem:)(\d\d/\d\d/[0-9]{4})(\d\d:\d\d:\d\d)', page_pdf)[0][1]

            # with open(u'C:\\Users\\eliton.1CGEO\\Desktop\\Pontos_Medidos\\_points\\{0}\\2_RINEX\\{0}.18o'.format(pto['nome']), 'rb') as rinex:
            #     lines = rinex.readlines()
            #     rinex_info = {}
            #     pto['nRec'] = lines[6].split(' ')[0]
            #     pto['nAnt'] = lines[7].split(' ')[0].strip()
            #     pto['altAntAux'] = "{0:.2f}".format(
            #         float(lines[9].strip().split(' ')[0]))
            #     pto['altAnt'] = pto['altAntAux'].replace('.', ',')
            #     pto['isGrounded'] = not bool(float(pto['altAntAux']) > 0)
            #     aux_inicio = [x for x in lines[12].strip().split(' ') if x]
            #     rinex_info["data_rastreio_1"] = "{0}-{1}-{2}".format(
            #         aux_inicio[0], aux_inicio[1].zfill(2), aux_inicio[2].zfill(2))
            #     rinex_info["hora_inicio_rastreio"] = "{0}:{1}".format(
            #         aux_inicio[3], aux_inicio[4])
            #     aux_fim = [x for x in lines[13].strip().split(' ') if x]
            #     rinex_info["hora_fim_rastreio"] = "{0}:{1}".format(
            #         aux_fim[3], aux_fim[4])
            #     rinex_info['durRast'] = datetime.strptime(
            #         rinex_info["hora_fim_rastreio"], '%H:%M') - datetime.strptime(rinex_info["hora_inicio_rastreio"], '%H:%M')
            #     pto['durRast'] = int(
            #         rinex_info['durRast'].total_seconds()/60)
            #     pto['dateRast'] = u"{2}/{1}/{0}".format(
            #         aux_inicio[0], aux_inicio[1].zfill(2), aux_inicio[2].zfill(2))
            #     pto['timeRast'] = "{0}:{1}".format(
            #         aux_inicio[3].zfill(2), aux_inicio[4].zfill(2))

            # # Fotos do ponto
            # photosPt = [f for f in os.listdir('{}\\{}\\3_Foto_Rastreio'.format(
            #     path, pto['nome'])) if re.match(r'RS-HV-[0-9]{3,4}_[0-9]{1,3}_FOTO.[Jj][Pp][Gg]', f)]
            # pathPhotosPt = []
            # pathPhotosPt.append(
            #     [os.path.join(path, pto['nome'], '3_Foto_Rastreio', f) for f in photosPt])
            # [[pto['photoPt1'], pto['photoPt2'], pto['photoPt3'],
            #     pto['photoPt4']]] = pathPhotosPt

            # # Foto do croqui, regex utilizado por causa da extensao JPG ou jpg
            # [photoCroqui] = [f for f in os.listdir('{}\\{}\\4_Croqui'.format(
            #     path, pto['nome'])) if re.match(r'RS-HV-[0-9]{3,4}_CROQUI.[Jj][Pp][Gg]', f)]
            # pto['photoCroqui'] = os.path.join(
            #     path, pto['nome'], '4_Croqui', photoCroqui)

            # # Foto vista aerea
            # pto['photoAerView'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\aer_view\\' + \
            #     pto['nome'] + '_aerView.png'
            # pto['photoView1'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\imagens_view\\Nova Pasta\\' + \
            #     pto['nome'] + '_view1.png'
            # pto['photoView2'] = 'C:\\Users\\eliton.1CGEO\\Desktop\\imagens_view\\' + \
            #     pto['nome'] + '_view2.png'

            # print pto['nome']

            # engine = Renderer()

            # # Path do template
            # result = engine.render(
            #     template='C:\\Users\\eliton.1CGEO\\Desktop\\test\\modelo2.odt', pto=pto)

            # Path do output
            # output = open('E:\\monografia\\{}.odt'.format(pto['nome']), 'wb')
            # output.write(result)


            # with open('C:\\Users\\eliton.1CGEO\\Desktop\\teste.csv', mode='ab') as employee_file:
            #     employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     employee_writer.writerow([pto['nome'], pto['n'], pto['e'], pto['aOrt']])
