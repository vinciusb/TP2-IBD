import re
import random as rd
import os

pathOrg = "./newInsert/organiza.sql"
pathFuncs = "./newInsert/funcs.sql"

os.system('cd ..')
prodsPorSec = {}


with open(r'{0}'.format(pathOrg), 'r+') as fileOrg:
    linesOrg = fileOrg.readlines()
    fileOrg.seek(0)
    fileOrg.truncate()

    with  open(r'{0}'.format(pathFuncs), 'r+') as fileFunc:
        linesFunc = fileFunc.readlines()
        fileFunc.seek(0)
        fileFunc.truncate()

        cpfOrganizadores = []

        for line in range(len(linesFunc)):
            if(re.search("1,null,null\)", linesFunc[line])):
                cpf = re.search("\d{11}", linesFunc[line])
                cpfOrganizadores.append(cpf.group())
        
        i = 0
        numOrganizadores = len(cpfOrganizadores)
        for i in range(numOrganizadores):
            linesOrg[i] = re.sub("\d{3}-\d{2}-\d{4}", cpfOrganizadores[i], linesOrg[i])

        for k in range(i, len(linesOrg)):
            randIdx = rd.randint(0, numOrganizadores -1)
            linesOrg[k] = re.sub("\d{3}-\d{2}-\d{4}", cpfOrganizadores[randIdx], linesOrg[k])


        fileFunc.writelines(linesFunc)

    fileOrg.writelines(linesOrg)