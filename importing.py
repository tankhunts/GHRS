import csv
import pymongo

def readFile(filename):
    if str(filename[0]) == '':
        return
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["GHRS"]
    mycol = mydb["PatientData"]
    patientList = []
    with open(str(filename[0]), mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            patientList.append(row)
    mycol.insert_many(patientList)