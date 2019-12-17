# coding=utf-8

import csv
import os
import re
from datetime import datetime, date
from pathlib import Path

import psycopg2
import psycopg2.extras
import PyPDF2
from secretary import Renderer

class GenerateMonograpy():

    def __init__(self):
        self.conn = psycopg2.connect("host='localhost' port='5432' dbname='pto_controle' user='postgres' password='postgres'")
        self.path = Path('C:\\Users\\Eliton\\Desktop\\2018-05-01')
        self.points = []
        super().__init__()
    
    def fetchAll(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(u'''
            SELECT * FROM bpc.ponto_controle_p
            ''')
            return cursor.fetchall()

    def fetchOne(self, point):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(u'''
            SELECT *,
            dominios.tipo_ref.code_name as tipo_ref1, 
            dominios.tipo_situacao.nome as tipo_situacao1,
            dominios.tipo_pto_ref_geod_topo.code_name as tipo_pto_ref_geod_topo1,
            dominios.tipo_medicao_altura.code_name as tipo_medicao_altura1,
            dominios.tipo_marco_limite.code_name as tipo_marco_limite1,
            dominios.situacao_marco.code_name as situacao_marco1,
            dominios.sistema_geodesico.code_name as sistema_geodesico1,
            dominios.referencial_grav.code_name as referencial_grav1,
            dominios.referencial_altim.code_name as referencial_altim1,
            dominios.referencia_medicao_altura.code_name as referencia_medicao_altura1,
            dominios.rede_referencia.code_name as rede_referencia1,
            dominios.orbita.code_name as orbita1,
            dominios.metodo_posicionamento.code_name as metodo_pos,
            dominios.classificacao_ponto.nome as classificacao_ponto1
            FROM bpc.ponto_controle_p
            INNER JOIN dominios.tipo_ref on dominios.tipo_ref.code = bpc.ponto_controle_p.tipo_ref
            INNER JOIN dominios.tipo_situacao on dominios.tipo_situacao.code = bpc.ponto_controle_p.tipo_situacao
            INNER JOIN dominios.tipo_pto_ref_geod_topo on dominios.tipo_pto_ref_geod_topo.code = bpc.ponto_controle_p.tipo_pto_ref_geod_topo
            INNER JOIN dominios.tipo_medicao_altura on dominios.tipo_medicao_altura.code = bpc.ponto_controle_p.tipo_medicao_altura
            INNER JOIN dominios.tipo_marco_limite on dominios.tipo_marco_limite.code = bpc.ponto_controle_p.tipo_marco_limite
            INNER JOIN dominios.situacao_marco on dominios.situacao_marco.code = bpc.ponto_controle_p.situacao_marco
            INNER JOIN dominios.sistema_geodesico on dominios.sistema_geodesico.code = bpc.ponto_controle_p.sistema_geodesico
            INNER JOIN dominios.referencial_grav on dominios.referencial_grav.code = bpc.ponto_controle_p.referencial_grav
            INNER JOIN dominios.referencial_altim on dominios.referencial_altim.code = bpc.ponto_controle_p.referencial_altim
            INNER JOIN dominios.referencia_medicao_altura on dominios.referencia_medicao_altura.code = bpc.ponto_controle_p.referencia_medicao_altura
            INNER JOIN dominios.rede_referencia on dominios.rede_referencia.code = bpc.ponto_controle_p.rede_referencia
            INNER JOIN dominios.orbita on dominios.orbita.code = bpc.ponto_controle_p.orbita
            INNER JOIN dominios.metodo_posicionamento on dominios.metodo_posicionamento.code = bpc.ponto_controle_p.metodo_posicionamento
            INNER JOIN dominios.classificacao_ponto on dominios.classificacao_ponto.code = bpc.ponto_controle_p.classificacao_ponto
            WHERE cod_ponto='{}'
            '''.format(point))
            return cursor.fetchone()

    def getDataFromStrucuture(self):
        folders = [x for x in self.path.rglob('*') if x.is_dir() and x.name in self.points]
        for folder in folders:
            self.executeProcess(folders.pop())
        
    def getListOfPoints(self):
        data = self.fetchAll()
        self.points = list(map(lambda x: x['cod_ponto'], data))

    def executeProcess(self, folder):
        pto = self.fetchOne(folder.name)
        print(pto)

        pto['dataMono'] = date.today()
        pto['freq'] = pto['freq_processada']
        # por algum bug na secretary durante a inserção das imagens é necessário duas imagens idênticas
        pto['signature'] = 'C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\generateMono\\hqdefault.jpg'
        pto['signature1'] = 'C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\generateMono\\hqdefault.jpg'
        pto['signature2'] = 'C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\generateMono\\hqdefault.jpg'
        pto['signature3'] = 'C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\generateMono\\hqdefault.jpg'
        pto['mc'] = pto['meridiano_central']
        pto['mascara'] = pto['mascara_elevacao']
        pto['taxa'] = pto['taxa_gravacao']
        pto['sigmaXY'] = u'0,11'
        pto['sigmaZ'] = u'0,18'
        pto['isGrounded'] = 'teste'
        pto['durRast'] = pto["fim_rastreio"] - pto["inicio_rastreio"]
        pto['inicio_rastreio'] = pto['inicio_rastreio'].strftime('%d/%m/%Y %H:%M:%S')
        pto['data_processamento'] = pto['data_processamento'].strftime('%d/%m/%Y')

        # Fotos do ponto
        photosPt = [str(f) for f in Path(folder / '3_Foto_Rastreio').iterdir() if f.match('*.jpg')]
        pto['photoPt1'] = photosPt[0]
        pto['photoPt2'] = photosPt[1]
        pto['photoPt3'] = photosPt[2]
        pto['photoPt4'] = photosPt[3]

        # Need to generate aerial views
        pto['photoCroqui'] = [str(f) for f in Path(folder / '4_Croqui').iterdir() if f.match('*.jpg')][0]
        pto['photoAerView'] = [str(f) for f in Path(folder / '4_Croqui').iterdir() if f.match('*.jpg')][0]
        pto['photoView1'] = [str(f) for f in Path(folder / '4_Croqui').iterdir() if f.match('*.jpg')][0]
        pto['photoView2'] = [str(f) for f in Path(folder / '4_Croqui').iterdir() if f.match('*.jpg')][0]

        # print pto['nome']

        engine = Renderer()

        # Path do template
        result = engine.render(
            template='C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\modelo2.odt', pto=pto)

        with open('C:\\Users\\Eliton\\Documents\\ferramentas_pto_controle_2\\generateMono\\results\\{}.odt'.format(pto['cod_ponto']), 'wb') as output:
          output.write(result)
