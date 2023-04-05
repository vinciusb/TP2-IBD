import re
import random as rd
import os

def substitui(regex, arquivo, newSize, eCPF):
    os.system('cd ..')
    with open(r'{0}'.format(arquivo), 'r+') as fp:
        # read an store all lines into list
        lines = fp.readlines()
        # move file pointer to the beginning of a file
        fp.seek(0)
        # truncate the file
        fp.truncate()

        decider = 2 if eCPF else 10
        for lineId in range(len(lines)):
            novo = "9" if (rd.randint(0, decider) > 5) else ""
            for i in range(newSize):
                novo += str(rd.randint(0, 9))

            lines[lineId] = re.sub(regex, novo, lines[lineId])

        fp.writelines(lines)

substitui("\d{3}-\d{2}-\d{4}", "./newInsert/CLIENTE.sql", 11, True)