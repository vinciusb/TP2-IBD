import re
import random as rd
import os

def substitui(arquivo):
    os.system('cd ..')
    prodsPorSec = {}

    with open(r'{0}'.format(arquivo), 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()

        with  open(r'{0}'.format('./inserts/produtos.sql'), 'r+') as prods:
            prodLines = prods.readlines()
            prods.seek(0)
            prods.truncate()

            numSecao = 0
            posGeral = 0

            for lineId in range(len(prodLines)):
                if prodLines[lineId].replace('\n', '').isnumeric(): 
                    numSecao = int(prodLines[lineId])             
                else:
                    posGeral += 1
                    nomeProd = prodLines[lineId].replace('\n', '')
                    
                    #Escreve 50 desse produto
                    for i in range(50):
                        marca = "{0}{1}".format(chr(ord('A') + i // 10) ,chr(ord('A') + i % 10))
                        idx = i + (posGeral - 1) * 50
                        lines[idx] = re.sub("\('[A-Za-z]'", '(' + nomeProd, lines[idx])
                        lines[idx] = re.sub(",\d,'", ",{0},'".format(numSecao), lines[idx])
                        lines[idx] = re.sub("'[A-Za-z]{2}'\)", "'{0}')".format(marca), lines[idx])

            prods.writelines(prodLines)

        fp.writelines(lines)
        


substitui("./inserts/prods.txt")