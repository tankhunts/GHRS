import sys
import pandas as pd
import numpy as np
from sodapy import Socrata
import json


class DrugQuery():

    def __init__(self):
        self.client = Socrata("datadiscovery.nlm.nih.gov", None)


    def query(self, drug, lim):
        results = self.client.get("crzr-uvwg", q=drug, limit = lim)
        return self.parse_response(results, lim)


    #returns a json string with the desired fields
    def parse_response(self, data, lim):
        results_df = pd.DataFrame.from_records(data)
        
        
        strings = np.zeros(lim, dtype=('U300'))

        for i, row in results_df.iterrows():
            json_dict = dict()
            json_dict["id"] = row["id"]
            json_dict["splshape_text"] = row["splshape_text"]
            json_dict["splimprint"] = row["splimprint"]
            json_dict["splcolor_text"] = row["splcolor_text"]
            json_dict["spl_strength"] = row["spl_strength"]
            json_dict["medicine_name"] = row["medicine_name"]
            strings[i] = json.dumps(json_dict)
            
        return strings
