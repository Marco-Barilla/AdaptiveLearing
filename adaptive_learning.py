import pandas
import csv
import random
import matplotlib.pyplot as plt

from base64 import b64decode


def decode(code):
    try:
        return b64decode(code).decode('utf-8')
    except Exception:
        return ""



df = pandas.read_csv('solutions.csv', sep=';', encoding='utf-8')
df.program64 = df.program64.apply(decode)
dlist = df.to_dict('records')

counter = 0
#print(dlist[1])
tasks = {}
for record in range(len(dlist)):
    try:
        #f.write(dlist[record])
        iterated = ['']
        lines = dlist[record]['program64'].splitlines()
        lines = [l.strip() for l in lines]
        lines = [i for i in lines if i != '']

        for i in range(len(lines)):   
            if lines[i] == 'continue' or lines[i] == 'pass' or lines[i] == 'else:' or 'for' in lines[i] or lines[i] == 'break':
                continue
            if lines[i] == 'print()' or lines[i] == 'print("")':
                continue
             
            if lines[i] in iterated:
                if len(iterated) > 1:
                    index = iterated.index(lines[i])
                    if iterated[index] == lines[i] and iterated[index-1] == lines[i-1]:
                        
                        print(dlist[record]['log_id'])
                        print(lines)
                        print('\n')
                        print(iterated)
                        print('\n')
                        print(lines[i])
                        print('\n')
                        
                        #print(dlist[record]['task_id'])
                        if dlist[record]['task_id'] in tasks:
                            tasks[dlist[record]['task_id']] += 1
                        else:
                            tasks[dlist[record]['task_id']] = 1
                        counter += 1

                iterated.append(lines[i])
            else:
                iterated.append(lines[i])

    except:
        pass
'''        
print('*')
for t in tasks:
    print(t)
print(tasks)
print('*')
print(counter)
'''
tasks = dict(sorted(tasks.items()))

names = list(tasks.keys())
values = list(tasks.values())
plt.bar(range(len(tasks)),values,tick_label=names)

plt.show()
#f.close()
