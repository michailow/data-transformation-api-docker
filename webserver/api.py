from flask import Flask
from sqlalchemy import create_engine
import pymysql
import helper


def createApp():
    app = Flask(__name__)
    credentials = helper.getCredentials()
    engine = create_engine(credentials)


    @app.route('/')
    def index():
        return "App started"


    @app.route("/getBrands/<string:brand>", methods=["GET"])
    def getBrands(brand):
        """GET outlets who sell certain brands

        :param brand: brand defined in the API call
        :return: query result OR error message
        """
        brand = "'%%" + brand + "%%'"
        getOutletsQuery = f"SELECT * FROM dashmote.ubereats_menu \
            WHERE brand LIKE {brand};"
        try:
            return helper.executeQuery(getOutletsQuery, engine)
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
            outletsQuery = f'SELECT DISTINCT id_outlet FROM dashmote.{source}'
            return helper.executeQuery(outletsQuery, engine)
        except Exception as e:
            return str(e)


    @app.route("/getMenuItems/<int:price>", methods=["GET"])
    def getMenuItems(price):
        """GET menu items above a certain price threshold
    
        :param: price threshold defined in the API call
        :return: query result OR error message
        """
        getMenuTripadvisorQuery = ("SELECT * "
                                   "FROM dashmote.tripadvisor_outlet "
                                   f"WHERE price_range_from > {price}")
    
        getMenuUberQuery = ("SELECT * "
                            "FROM dashmote.ubereats_menu "
                            f"WHERE price > {price}")
    
        try:
            menuTripadvisor = helper.executeQuery(getMenuTripadvisorQuery)
            menuUber = helper.executeQuery(getMenuUberQuery, engine)
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
            helper.uploadData(fileName, engine)
            successMessage = f'File {fileName} posted'
            return successMessage
        except Exception as e:
            return str(e)
        
        
    return app


def main():
    app = createApp()
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()