import pymongo
import random
import datetime
import string
# Text files taken from https://github.com/dominictarr/random-name


myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["GHRS"]
blood = ["A+", "AB+", "B+", "O+", "A-", "AB-", "B-", "O-"]
gender = ['Male', 'Female', 'Transgender', 'Gender Neutral', "Non-binary", 'Agender', 'Pangender', 'Genderqueer', 'Genderfluid', 'Perfer not to say']
Race = ["American Indian", "Asian", "Black", "Hispanic", "Native Hawiian", "White"]
insurance = ["Anthem", "Aetna", "United", "Cigna", "Medicare"]
mycol = mydb["PatientData"]
first = open("first-names.txt", "r")
last = open("names.txt", "r")
firstNames = []
lastNames = []
for name in first:
    firstNames.append(name[0:-1])
for name in last:
    lastNames.append(name[0:-1])
firstSize = len(firstNames)
lastSize = len(lastNames)

print("Enter how many records you want to generate.")
toGen = input()
toGen = int(toGen)

startDate = datetime.date(1980, 1, 1)
endDate = datetime.date(2010, 1, 1)
days = (endDate-startDate).days

i = 0
while i < toGen:
    myDict = {}
    myDict["First Name"] = firstNames[random.randrange(firstSize)]
    myDict["Last Name"] = lastNames[random.randrange(lastSize)]
    myDict["DOB"] = str(startDate + datetime.timedelta(days=random.randrange(days)))
    myDict["Insurance"] = insurance[random.randrange(5)]
    myDict["ID"] = ''.join(random.choices(string.ascii_letters+string.digits, k=random.randrange(4)+8))
    myDict["Race"] = Race[random.randrange(6)]
    myDict['Blood Type'] = blood[random.randrange(8)]
    myDict['Gender'] = gender[random.randrange(10)]
    myDict["Conditions"] = ""
    myDict["Perscriptions"] = []
    myDict["Notes"] = []
    mycol.insert_one(myDict)
    i+=1



