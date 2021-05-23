import pandas
import csv
import random
import matplotlib.pyplot as plt
import numpy as np

from base64 import b64decode


def decode(code):
    try:
        return b64decode(code).decode('utf-8')
    except Exception:
        return ""


stopWords = ['continue', 'pass',  'else' , 'if ', 'if(', 'for ', 'for   ', 'break', 'while']

def contains_stopWord(line):
    for sw in stopWords:
        if sw in line:
            return True
    return False

df = pandas.read_csv('solutions-ipython.csv', sep=';', encoding='utf-8')
df.program64 = df.program64.apply(decode)
dlist = df.to_dict('records')

counter_2 = 0
counter_3 = 0
tasks_3_lines = {}
tasks_2_lines = {}


def show_graph(tasks):
    names = list(tasks.keys())
    values = list(tasks.values())
    plt.bar(range(len(tasks)),values,tick_label=names)
    plt.title('Duplicate code')
    plt.xlabel('task ID')
    plt.show()


def show_comparison(tasks_2_lines, tasks_3_lines):
    missing_keys = set(tasks_2_lines.keys()) - set(tasks_3_lines.keys())
    for k in missing_keys:
        tasks_3_lines[k] = 0
    missing_keys = set(tasks_3_lines.keys()) - set(tasks_2_lines.keys())
    for k in missing_keys:
        tasks_2_lines[k] = 0


    tasks_3_lines = dict(sorted(tasks_3_lines.items()))
    tasks_2_lines = dict(sorted(tasks_2_lines.items()))


    X_axis = np.arange(len(tasks_2_lines))
    
    plt.bar(X_axis - 0.2, tasks_3_lines.values(), 0.4, label = '3 line repetition')
    plt.bar(X_axis + 0.2, tasks_2_lines.values(), 0.4, label = '2 line repetition')

    plt.xticks(X_axis, tasks_2_lines.keys())
    plt.xlabel("task ID")
    plt.ylabel("Detected instances")
    plt.title("Duplicate code lines detection")
    plt.legend()
    plt.show()

def debug_print(lines_num, dlist, lines, iterated):
    print(dlist[record]['log_id'])
    print(lines)
    print('\n')
    print(iterated)
    print('\n')
    if lines_num == 3:
        print(lines[i-2])
    print(lines[i-1])
    print(lines[i])
    print('\n')


# dva riadky po sebe
for record in range(len(dlist)):
    try:
        iterated = ['']
        lines = dlist[record]['program64'].splitlines()
        lines = [l.strip() for l in lines]
        lines = [i for i in lines if i != '']

        for i in range(len(lines)): 
           
            if contains_stopWord(lines[i]):
                iterated.append('#combo_breaker')
                continue

            if lines[i] in iterated:
                if i > 2:
                    index = iterated.index(lines[i])
                    if iterated[index] == lines[i] and iterated[index-1] == lines[i-1]:

                        #debug_print(2, dlist, lines, iterated)
                        counter_2 += 1

                        if dlist[record]['task_id'] in tasks_2_lines:
                            tasks_2_lines[dlist[record]['task_id']] += 1
                        else:
                            tasks_2_lines[dlist[record]['task_id']] = 1

            iterated.append(lines[i])

    except:
        pass

# tri riadky po sebe
for record in range(len(dlist)):
    try:
        iterated = ['']
        lines = dlist[record]['program64'].splitlines()
        lines = [l.strip() for l in lines]
        lines = [i for i in lines if i != '']

        for i in range(len(lines)): 

            if contains_stopWord(lines[i]):
                iterated.append('#combo_breaker %d' % (i))
                continue

            if lines[i] in iterated:
                if len(iterated) > 3:
                    index = iterated.index(lines[i])
                    if iterated[index] == lines[i] and iterated[index-1] == lines[i-1] and iterated[index-2] == lines[i-2]:

                        #debug_print(3, dlist, lines, iterated)
                        counter_3 += 1

                        if dlist[record]['task_id'] in tasks_3_lines:
                            tasks_3_lines[dlist[record]['task_id']] += 1
                        else:
                            tasks_3_lines[dlist[record]['task_id']] = 1
                    
            iterated.append(lines[i])

    except:
        pass


print(counter_2)
print(counter_3)

show_graph(tasks_3_lines)
show_graph(tasks_2_lines)

show_comparison(tasks_2_lines, tasks_3_lines)
