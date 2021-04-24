from flask_restful import Api, Resource, reqparse
import mysql.connector
import os


class ProfileApiHandler(Resource):

    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Login Api Handler"
        }

    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str)

        args = parser.parse_args()
        print(args)
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

        request_userID = args['userID']
        # ret_status, ret_msg = ReturnData(request_email, request_password)
        # # currently just returning the req straight

        ret_status = "Failure"
        ret_msg = ""
        user_info = []

        # connect to mysql database
        host = os.environ.get('MYSQL_HOST')
        database = os.environ.get('MYSQL_DATABASE')
        password = os.environ.get('MYSQL_PASSWORD')
        user = os.environ.get('MYSQL_USER')

        cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)

        # check database
        cursor = cnx.cursor()
        sql_query = "SELECT *FROM UserProfile WHERE UserID ='%s'" % request_userID

        cursor.execute(sql_query)
        query_results = cursor.fetchall()

        if len(query_results) == 0:
            ret_msg = "No user with userID: " + request_userID + " has been found"
        else:
            ret_status = "Success"
            ret_msg = "Log in successfully"
            for row in query_results:
                user_id = row[0]
                email = row[1]
                name = row[2]
                pic_url = row[4]
                location = row[5]
                restaurant_list_id = row[6]
                print(row)

        # find restaurants' ids with userID
        restaurant_sql_query = "SELECT *FROM UserRestaurantList WHERE UserID ='%s'" % request_userID
        cursor.execute(restaurant_sql_query)
        restaurant_query_results = cursor.fetchall()
        restaurant_ids = []
        if len(restaurant_query_results) == 0:
            ret_msg = "No restaurant under userID: " + request_userID + " has been found"
        else:
            ret_status = "Success"
            ret_msg = "Log in successfully"
            for row in query_results:
                restaurant_ids.append(row[1])
                print(row)

        # find detailed info about restaurants with restaurants' ids
        restaurants = []
        for restaurant_id in restaurant_ids:
            restaurant_info_sql_query = "SELECT *FROM Restaurant WHERE RestaurantID ='%s'" % restaurant_id
            cursor.execute(restaurant_info_sql_query)
            restaurant_info_query_result = cursor.fetchall()[0]
            restaurants.append(restaurant_info_query_result)

        final_ret = {"status": ret_status, "message": ret_msg, "restaurants": restaurants, "name": name, "email": email,
                     "pic_url": pic_url, "location": location}

        return final_ret