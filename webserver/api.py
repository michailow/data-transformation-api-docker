from flask import Flask
import json
import pandas as pd
from sqlalchemy import create_engine
import pymysql


engine = create_engine(
      "mysql+pymysql://de:root@localhost/main")


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


def uploadData(fileName):
    
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
        

def collectOutlets(source):
    
    """Query data to get all unique outlets
    
    :param source: table form with we want get list
    :return: unique outlets
    """
    
    if source  == "tripadvisor_user":
        return "Outlets not presented in this table"
    else:
        outletsQuery = f'SELECT DISTINCT id_outlet FROM main.{source}'
    returnList = []
    resultBrand = engine.execute(outletsQuery)
    for row in resultBrand:
        returnList.append(str(row))
    return str(returnList)
    

app = Flask(__name__)


@app.route('/')
def index():
    return "App started"


@app.route("/getBrands/<string:brand>", methods=["GET"])
def getBrands(brand):
    
    """GET outlets who sell certain brands
    
    :param brand: brand defined in the API call
    :return: query result OR error message
    """
    
    brand = "'" + brand + "'"
    getOutletsQuery = f"SELECT * FROM main.ubereats_menu \
        WHERE brand = {brand};"
    
    try:
        returnList = []
        resultBrand = engine.execute(getOutletsQuery)
        for row in resultBrand:
            returnList.append(str(row))
        return str(returnList)
    except Exception as e:
        return str(e)
    

@app.route("/getOutlets/<string:source>", methods=["GET"])
def getOutlets(source):
    
    """GET a list of outlets that have a presence in one specific source
    
    :param: source defined in the API call
    :return: query result OR error message
    """
    
    try:
        return collectOutlets(source)
    except Exception as e:
        return str(e)


@app.route("/getMenuItems/<int:price>", methods=["GET"])
def getMenuItems(price):
    
    """GET menu items above a certain price threshold
    
    :param: price threshold defined in the API call
    :return: query result OR error message
    """
    
    getMenuTripadvisorQuery = ("SELECT * "
    "FROM main.tripadvisor_outlet "
    f"WHERE price_range_from > {price}")
    
    getMenuUberQuery = ("SELECT * "
    "FROM main.ubereats_menu "
    f"WHERE price > {price}")
    
    try:
        returnList = []
        resultTripadvisor = engine.execute(getMenuTripadvisorQuery)
        for row in resultTripadvisor:
            returnList.append(str(row))
            
        resultTripadvisor = engine.execute(getMenuUberQuery)
        for row in resultTripadvisor:
            returnList.append(str(row))
        
        return(str(returnList))
    except Exception as e:
        return str(e)


@app.route("/postOutlet/<string:fileName>", methods=["POST"])
def postOutlet(fileName):
    
    """POST a new outlet
    
    :param: filename with outlet data
    :return success message or error message
    """
    
    try:
        uploadData(fileName)
        successMessage = f'File {fileName} posted'
        return successMessage
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)