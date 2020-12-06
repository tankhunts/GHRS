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
        
        all_ingredients = []
        strings = []

        for i, row in results_df.iterrows():
            json_dict = dict()
            ingredients = row["spl_ingredients"].split(";")
            ingredients.pop(len(ingredients)-1)
            for i in range(len(ingredients)):
                ingredients[i] = ingredients[i][ingredients[i].find("[")+1:ingredients[i].find("]")]
            try:
                ingredients.extend(row["spl_inactive_ing"].split(";"))
                ingredients.pop(len(ingredients)-1)
            except AttributeError:
                pass
            json_dict["id"] = row["id"]
            json_dict["splshape_text"] = row["splshape_text"]
            json_dict["splimprint"] = row["splimprint"]
            json_dict["splcolor_text"] = row["splcolor_text"]
            json_dict["spl_strength"] = row["spl_strength"]
            json_dict["medicine_name"] = row["medicine_name"]
            all_ingredients.append(ingredients)
            strings.append(json_dict)

        return (strings, all_ingredients)
