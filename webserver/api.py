from flask import Flask
import json
import pandas as pd
from sqlalchemy import create_engine
import pymysql


engine = create_engine(
      "mysql+pymysql://de:root@localhost/devDB")


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
        

def executeQuery(query):
    """Executes query and return results
    
    :param query: query as str ot tuple
    :return: result as str
    """
    returnList = []
    result = engine.execute(query)
    for row in result:
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
    getOutletsQuery = f"SELECT * FROM devDB.ubereats_menu \
        WHERE brand = {brand};"
    try:
        return executeQuery(getOutletsQuery)
    except Exception as e:
        return str(e)
    

@app.route("/getOutlets/<string:source>", methods=["GET"])
def getOutlets(source):
    """GET a list of outlets that have a presence in one specific source
    
    :param: source defined in the API call
    :return: query result OR error message
    """
    if source == "tripadvisor_user":
        return "Outlets not presented in this table"
    try:
        outletsQuery = f'SELECT DISTINCT id_outlet FROM devDB.{source}'
        return executeQuery(outletsQuery)
    except Exception as e:
        return str(e)


@app.route("/getMenuItems/<int:price>", methods=["GET"])
def getMenuItems(price):
    """GET menu items above a certain price threshold
    
    :param: price threshold defined in the API call
    :return: query result OR error message
    """
    getMenuTripadvisorQuery = ("SELECT * "
    "FROM devDB.tripadvisor_outlet "
    f"WHERE price_range_from > {price}")
    
    getMenuUberQuery = ("SELECT * "
    "FROM devDB.ubereats_menu "
    f"WHERE price > {price}")
    
    try:
        menuTripadvisor = executeQuery(getMenuTripadvisorQuery)
        menuUber = executeQuery(getMenuUberQuery)
        return(menuTripadvisor + menuUber)
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