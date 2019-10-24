import csv
import re
import pdb

parcel_list = []
name_list = []
new_list = []
with open('data.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    # new_list = [row for row in spamreader if 'Parcel' in row]
    for row in spamreader:
        if row and ('Parcel' in row[0] or re.search("\\A[A-Z]\\d+", row[0])):
            if row[0].startswith('Parcel'):
                parcel = row[0].split('Parcel:')[1].strip()
                if parcel != '':
                    parcel_list.append([parcel])
            else:
                try:
                    parcel = row[0].split('Parcel:')[1].strip().split(' ')[0].strip()
                    name = ' '.join(row[0].split('Parcel:')[0].strip().split(' ')[1:])
                    if [name] not in name_list:
                        name_list.append([name])
                    if parcel != '':
                        parcel_list.append([parcel])
                except:
                    pass
        
with open('parcel.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(parcel_list)
    
with open('value.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Name'])
    spamwriter.writerows(name_list)