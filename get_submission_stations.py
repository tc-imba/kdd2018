import csv

colName = None
arr = []
dic = {}

f = open('sample_submission.csv')
for row in csv.reader(f):
    if not colName:
        colName = row
    else:
        index = row[0].find('#')
        name = row[0][0:index]
        if not dic.__contains__(name):
            dic[name] = True
            arr.append(name)

print(arr)
