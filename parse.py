import csv
import re
import pdb
import json

# R34234: R\d+
# address: \d+[a-zA-Z]+\sST

parcel_list = []
name_list = []
new_list = []
data_list = []
with open('data.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    # new_list = [row for row in spamreader if 'Parcel' in row]
    index = -1
    for row in spamreader:
        if not row:
            continue
        try:
            if re.search(r"R\d+", row[0]): # the line starts with R90909 - APN
                index += 1
                data_list.append({'ParcelID': -1, 'Name': None, 'APN': None})
        except:
            pdb.set_trace()
        if row and ('Parcel' in row[0] or re.search("\\A[A-Z]\\d+", row[0])):
            if row[0].startswith('Parcel'):
                parcel = row[0].split('Parcel:')[1].strip()
                if parcel != '':
                    parcel_list.append([parcel])
                    data_list[index]['ParcelID'] = parcel
            else:
                try:
                    parcel = row[0].split('Parcel:')[1].strip().split(' ')[0].strip()
                    name = ' '.join(row[0].split('Parcel:')[0].strip().split(' ')[1:])
                    apn = row[0].split('Parcel:')[0].strip().split(' ')[0]
                    data_list[index]['APN'] = apn
                    if [name] not in name_list:
                        name_list.append([name])
                        data_list[index]['Name'] = name
                    if parcel != '':
                        parcel_list.append([parcel])
                        data_list[index]['ParcelID'] = parcel
                except:
                    pass
  
with open('parcel.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerows(parcel_list)
    
with open('value.csv', 'w', newline='') as csvfile:
    spamwriter = csv.DictWriter(csvfile, fieldnames=['Name', 'ParcelID', 'APN'])
    spamwriter.writeheader()
    spamwriter.writerows(data_list)