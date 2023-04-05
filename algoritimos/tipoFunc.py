import re
import random as rd
import os

pathOrg = "./newInsert/funcs.sql"

os.system('cd ..')
prodsPorSec = {}


with open(r'{0}'.format(pathOrg), 'r+') as file:
    lines = file.readlines()
    file.seek(0)
    file.truncate()

    for i in range(len(lines)):
        matches = re.findall(",\d+", lines[i])

        tipoFunc = int(matches[1][1:])
        numCaixa = int(matches[2][1:])
        codSecao = int(matches[3][1:])

        novoCaixa = numCaixa
        novoSecao = codSecao

        if tipoFunc == 1:
            novoCaixa = 'null'
            novoSecao = 'null'
        elif tipoFunc == 2:
            novoSecao = 'null'
        else:
            novoCaixa = 'null'

        lines[i] = re.sub(",{0},{1}".format(numCaixa, codSecao), ",{0},{1}".format(novoCaixa, codSecao), lines[i])
        lines[i] = re.sub(",{0}\)".format(codSecao), ",{0})".format(novoSecao), lines[i])


    file.writelines(lines)

#(cpf_func, salario, nome, sobrenome, telefone_func, tipo_func, numero_caixa, cod_secao_auxiliada)