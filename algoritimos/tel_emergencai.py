import re
import random as rd
import os

pathTel = "./newInsert/telefones.sql"
pathFuncs = "./newInsert/funcs.sql"

os.system('cd ..')
prodsPorSec = {}


with open(r'{0}'.format(pathTel), 'r+') as fileTel:
    linesTel = fileTel.readlines()
    fileTel.seek(0)
    fileTel.truncate()

    with  open(r'{0}'.format(pathFuncs), 'r+') as fileFunc:
        linesFunc = fileFunc.readlines()
        fileFunc.seek(0)
        fileFunc.truncate()
                
        numTel = len(linesTel)
        numFunc = len(linesFunc)

        for line in range(numTel):
            i = rd.randint(0, numFunc - 1)
            cpf = re.search("\d{11}", linesFunc[i]).group()


            linesTel[line] = re.sub("\d{3}-\d{2}-\d{4}", cpf, linesTel[line])

        fileFunc.writelines(linesFunc)

    fileTel.writelines(linesTel)