import json
import pandas as pd
import os
from dotenv import load_dotenv


def getCredentials():
    """Gets credentials from .env file
    
    :return: credentials
    """
    load_dotenv()
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    return f"mysql+pymysql://{user}:{password}@db:3306/dashmote"


def openFile(fileName):
    """Opens json file
    
    :param fileName: directory with file
    :return: file data in json format
    """
    with open(fileName) as f:
        file = json.load(f)
    return file


def priceRange(priceRange):
    """Adds new column to table with staring price
    
    :param priceRange: row with price range
    :return: staring price
    """
    if type(priceRange) == str:
        price = priceRange.split(' - ')[0][1:]
        price = price.replace(",", "")
        return price


def uploadData(fileName, engine):
    """Upload data to databese
    If this is tripadvisor_outlet, applies additional transformations
    
    :param fileName: directory with file
    :return: None
    """
    file = openFile(fileName)
    normalizedData = pd.DataFrame(file)
    tableName = fileName.split(".")[0]
    
    if fileName == 'tripadvisor_outlet.json':
        normalizedData['price_range_from'] = (normalizedData['price_range']
                                              .apply(lambda x:
                                                     priceRange(x)))
    normalizedData.to_sql(tableName, con=engine, if_exists='append')
        

def executeQuery(query, engine):
    """Executes query and return results
    
    :param query: query as str ot tuple
    :return: result as str
    """
    returnList = []
    result = engine.execute(query)
    for row in result:
        returnList.append(str(row))
    return str(returnList)