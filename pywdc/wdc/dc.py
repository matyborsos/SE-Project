import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

class DatabaseConnection:
    # inside of __init__ we initialize the connection to the WCPS server
    #Establishes a connection to the WCPS server.
    def __init__(self, url):
        self.url = url
        try:
            # Attempt to establish a connection to the WCPS server
            requests.get(self.url)
        except requests.exceptions.RequestException as e:
            # Handle connection errors by raising an exception
            raise ConnectionError(f"Error connecting to the server: {e}")

class Datacube:
    def __init__(self, dbc):
    #Database connection object ~ responsible for the connection to the server of a datacube.
    #Represents a data cube and provides methods for interacting with it.
        self.dbc = dbc
        self.operations = []
        
 # Queries sourced from "https://ows.rasdaman.org/rasdaman/ows"   
   
    def add_operation(self, operation):
        #Adds an operation to the list of operations to be performed.
        self.operations.append(operation)
    
    def to_wcps(self, operation):
        #Generates a WCPS query string from an operation tuple.
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
        #Performs a subset operation on the data cube.
        '''Args:
            coverage (str): The coverage to subset.
            time (str): The time range.
            E1 (float): The starting longitude.
            E2 (float): The ending longitude.
            N1 (float): The starting latitude.
            N2 (float): The ending latitude.'''
            
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
        
    def basic(self):
        #Performs a basic Operations which returns 1 
        wcps_query = f'''
        for $c in (AvgLandTemp) 
        return 
            1
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
            print("Basic:", result)
            
    def get_1d_subset(self,lat, long):
        #Transforms a 3D subset into a
        #fetches a subset of data covering a time period.Each value in the list corresponds to a specific time interval 
        # within the range from January 2014 to December 2014.
        wcps_query = f'''
        for $c in (AvgLandTemp)
        return 
            encode($c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")],"text/csv")
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
        else:
            print("Error fetching plot data.") 
            
    #Aggregation function such as min, max, avg 
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
            
    def when_temp_more_than_15(self, lat, long):
        wcps_query = f'''
        for $c in ({self.coverage})
        return 
        count($c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")]
            > 15)
        '''
        result = self.execute_query(wcps_query)
        if result:
            return result
            print("Temp is more than 15: ", result)
            
    """def plot(self, lat, long): 
        wcps_query = f'''for $c in (AvgLandTemp) 
                        return encode(
                                $c[Lat({lat}), Long({long}), ansi("2014-01":"2014-12")]
                                , "application/json")
                        '''
        plot_data = self.execute_query(wcps_query)
        if plot_data:
            try:
                # Open the image from the response content
                img = Image.open(BytesIO(plot_data.content))
                # Display the image
                img.show()
            except IOError as e:
                print("Error opening image:", e)"""

