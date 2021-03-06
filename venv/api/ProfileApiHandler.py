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
                print(row)
                user_info = {
                    "user_id": user_id,
                    "email": email,
                    "name": name,
                    "pic_url": pic_url,
                    "location": location
                }

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
            print(restaurant_query_results)
            for row in restaurant_query_results:
                restaurant_ids.append(row[2])

        print(restaurant_ids)
        # find detailed info about restaurants with restaurants' ids
        restaurants = []
        for restaurant_id in restaurant_ids:
            restaurant_info_sql_query = "SELECT *FROM Restaurant WHERE RestaurantID ='%s'" % restaurant_id
            cursor.execute(restaurant_info_sql_query)
            restaurant_info_query_result = cursor.fetchall()[0]
            # restaurants.append(restaurant_info_query_result)
            restaurant_dict = {
                "r_id": restaurant_info_query_result[0],
                "r_name": restaurant_info_query_result[1],
                "r_longitude": restaurant_info_query_result[2],
                "r_latitude": restaurant_info_query_result[3],
                "r_rating": restaurant_info_query_result[4],
                "r_pic_url": restaurant_info_query_result[5],
                "r_address": restaurant_info_query_result[6]
            }
            restaurants.append(restaurant_dict)
        print(restaurants)

        # find followers' ids with userID
        follower_sql_query = "SELECT *FROM Followers WHERE UserID ='%s'" % request_userID
        cursor.execute(follower_sql_query)
        follower_query_results = cursor.fetchall()
        follower_ids = []
        if len(follower_query_results) == 0:
            ret_msg = "No follower under userID: " + request_userID + " has been found"
        else:
            ret_status = "Success"
            ret_msg = "Log in successfully"
            print(follower_query_results)
            for row in follower_query_results:
                follower_ids.append(row[2])
        print(follower_ids)

        # find detailed info about followers with followers' ids
        followers = []
        for follower_id in follower_ids:
            follower_info_sql_query = "SELECT *FROM UserProfile WHERE UserID ='%s'" % follower_id
            cursor.execute(follower_info_sql_query)
            follower_info_sql_query_result = cursor.fetchall()[0]
            follower_dict = {
                "follower_id": follower_info_sql_query_result[0],
                "follower_email": follower_info_sql_query_result[1],
                "follower_name": follower_info_sql_query_result[2],
                "follower_pic_url": follower_info_sql_query_result[4],
                "follower_location": follower_info_sql_query_result[5],
            }
            followers.append(follower_dict)
        print(followers)

        final_ret = {"status": ret_status, "message": ret_msg, "restaurants": restaurants, "user_info": user_info,
                     "location": location, "followers": followers}

        return final_ret
