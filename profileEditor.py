import pymongo
from bson.objectid import ObjectId
from datetime import date

#TODO add note sections later on
class ProfileEditor:
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["GHRS"]
    mycol = mydb["PatientData"]
    def saveProfile(self, identifier, record):
       firstLast = record[0].split()
       self.mycol.update({'_id': ObjectId(identifier)}, 
                                  {'$set': { 
                                  'First Name' : firstLast[0], 
                                  'Last Name'  : firstLast[1],
                                  'DOB'        : record[1],
                                  'Insurance'  : record[5],
                                  'ID'         : record[6],
                                  'Race'       : record[2],
                                  'Blood Type' : record[4],
                                  'Gender'     : record[3]}})

    #TODO link with add patient page
    def addPatient(self, record):
        firstLast = record[0].split()
        addDict = {}
        addDict["First Name"] = firstLast[0]
        addDict["Last Name"] = firstLast[1]
        addDict["DOB"] = record[1]
        addDict["Insurance"] = record[5]
        addDict["ID"] = record[6]
        addDict["Race"] = record[2]
        addDict['Blood Type'] = record[4]
        addDict['Gender'] = record[3]
        addDict["Conditions"] = record[7]
        addDict["Perscriptions"] = ""
        if (record[8] != "" and record[9] != ""):
            addDict["Notes"] = [{"Date": str(date.today()), "Note": record[9], "Subject": record[8]}]
        #addDict["Notes"] = record[8]
        #addDict["Note"] = record[9]
        self.mycol.insert_one(addDict)

    #TODO link with a delete option in the GUI
    def deleteProfile(self, identifier):
        self.mycol.delete_one({'_id': ObjectId(identifier)})

