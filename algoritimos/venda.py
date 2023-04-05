# (ID_VENDA, COD_PROD, CPF_CLIENTE, CPF_FUNC, QNT)
"""
Pega a lista de cpfs dos caixas e de clientes. Faz um rand nos dois e define pra
venda I. Fazer isso pra todas as vendas. Pra isso eu tenho que saber quais são 
toda as vendas. Iterar por todo o arquivo e descobrir.
Para cada [ID_VENDA]: {CPF_CLIENTE, CPF_FUNC}
"""

import re
import random as rd
import os

pathVenda = "./newInsert/venda.sql"
pathFuncs = "./newInsert/funcs.sql"
pathCliente = "./newInsert/cliente.sql"

os.system('cd ..')
venda = {}


with open(r'{0}'.format(pathVenda), 'r+') as fileVenda:
    linesVenda = fileVenda.readlines()
    fileVenda.seek(0)
    fileVenda.truncate()

    with  open(r'{0}'.format(pathFuncs), 'r+') as fileFunc:
        linesFunc = fileFunc.readlines()
        fileFunc.seek(0)
        fileFunc.truncate()

        with  open(r'{0}'.format(pathCliente), 'r+') as fileCliente:
            linesCliente = fileCliente.readlines()
            fileCliente.seek(0)
            fileCliente.truncate()

            # Obtem todos ID de venda
            for i in range(len(linesVenda)):
                vendaID = re.search("\(\d+", linesVenda[i]).group()[1:]
                venda[vendaID] = ['','']

            cpfCaixa = []
            for i in range(len(linesFunc)):
                matches = re.findall(",\d+", linesFunc[i])
                tipoFunc = int(matches[1][1:])

                if tipoFunc == 2:
                    cpf = re.search("\d{11}", linesFunc[i]).group()
                    cpfCaixa.append(cpf)

            cpfCliente = []
            for i in range(len(linesCliente)):
                cpf = re.search("\d{11}", linesCliente[i]).group()
                cpfCliente.append(cpf)
            
            vendas = {}
            # Assimila CPFs pra compra
            for key in venda:
                idCaixa = rd.randint(0, len(cpfCaixa) - 1)
                idCliente = rd.randint(0, len(cpfCliente) - 1)

                venda[key] = [cpfCliente[idCliente], cpfCaixa[idCaixa]]
                vendas[key] = []

            # [ID_VENDA] : []
            for i in range(len(linesVenda)):
                matches = re.findall("\d+", linesVenda[i])
                idVenda = int(matches[0])
                idProduto = int(matches[1])
                newIdProduto = idProduto

                funciona = False
                while not funciona:
                    if vendas[str(idVenda)].count(newIdProduto) > 0:
                        newIdProduto = rd.randint(1, 2500)
                    else:
                        funciona = True
                        linesVenda[i] = re.sub("{0}".format(idProduto), "{0}".format(newIdProduto), linesVenda[i])

                vendas[str(idVenda)].append(newIdProduto)

                linesVenda[i] = re.sub("-1", "'{0}'".format(venda[str(idVenda)][0]), linesVenda[i])
                linesVenda[i] = re.sub("-2", "'{0}'".format(venda[str(idVenda)][1]), linesVenda[i])

            fileCliente.writelines(linesCliente)

        fileFunc.writelines(linesFunc)

    fileVenda.writelines(linesVenda)