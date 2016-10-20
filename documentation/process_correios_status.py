#!/usr/bin/env python3.5

import re
import sys
import csv


result = []

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile)
    for raw_row in reader:
        #['Tipos', 'Status', 'Descrição', 'Detalhe', 'O que o cliente deve fazer']
        tipo, status, descr, detalhe, cliente = raw_row
        tipo = tipo.strip().replace("\n", " ")
        status = status.strip().replace("\n", " ")
        descr = descr.strip().replace("\n", " ")
        detalhe = detalhe.strip().replace("\n", " ")
        cliente = cliente.strip().replace("\n", " ")
        if status:
            row = {
                'tipo': tipo.split(),
                'status': status,
                'descr': descr,
                'detalhe': detalhe,
                'cliente': cliente,
            }
            result.append(row)
        else:
            if tipo:
                row['tipo'].append(tipo)
            row['descr'] = "{} {}".format(row['descr'], descr).strip()
            row['detalhe'] = "{} {}".format(row['detalhe'], detalhe).strip()
            row['cliente'] = "{} {}".format(row['cliente'], cliente).strip()

writer = csv.writer(sys.stdout)
for res in result:
    for tipo in res["tipo"]:
        detalhe = res["detalhe"].replace('F avor', 'Favor')
        detalhe = re.sub("<.*?>", "", detalhe).strip()

        row = [
            tipo,
            res["status"],
            res["descr"],
            detalhe,
            res["cliente"],
        ]
        writer.writerow(row)
