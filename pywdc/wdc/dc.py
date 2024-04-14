#!/usr/bin/python
__author__ = 'Matheas-Roland Borsos'

import requests
from PIL import Image
from io import BytesIO


class DatabaseConnection:
    def __init__(self, url):
        self.url = url

class Datacube:
    def __init__(self, dbc):
        self.dbc = dbc
        self.operations = []
        
    def add_operation(self, operation):
        self.operations.append(operation)
    
    def to_wcps(self, operation):
        return f"$c[ansi(\"{operation[1]}\"), E({operation[2]}:{operation[3]}),N({operation[4]}:{operation[5]})],"

    def generate_query(self):
        unique_operations = set(op[0] for op in self.operations)
        query = f"for $c in ({', '.join(unique_operations)})\n"
        query += "return\n encode(\n"
        query += " ".join(self.to_wcps(op) for op in self.operations)
        query += "\n  \"image/png\" )"
        self.operations = []
        return query    

    def subset(self, coverage, time, E1, E2, N1, N2):
        operation = (coverage, time, E1, E2, N1, N2)
        self.add_operation(operation)
        wcps_query = self.generate_query()
        print("Executing WCPS query:", wcps_query)
        response = requests.post(self.dbc.url, data={'query': wcps_query}, verify=True)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.show()
            return response, wcps_query
        else:
            print("Error:", response.status_code)
            return response, wcps_query


    def execute_query(self, wcps_query):
        response = requests.post(self.dbc.url, data={"query": wcps_query}, verify=True)
        if response.status_code == 200:
            return response.content.decode()
        else:
            print("Error:", response.status_code)
            return None

    def avg(self, lat, long):
        wcps_query = f'''
        for $c in (AvgLandTemp)
        return 
            avg($c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")])
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
            print("Average:", result)
        
    def min(self, lat, long):
        wcps_query = f'''
        for $c in (AvgLandTemp)
        return 
            min($c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")])
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
            print("Minimum:", result)
        
    def max(self, lat, long):
        wcps_query = f'''
        for $c in (AvgLandTemp)
        return 
            max($c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")])
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
            print("Maximum:", result)

