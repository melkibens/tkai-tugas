from django.http import JsonResponse
import psycopg2, hashlib, binascii, os
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def follow_person(request):
    if request.method == "POST":
        usernameX = request.POST["usernameX"]
        usernameY = request.POST["usernameY"]
        insert_to_db_following_or_follower(usernameX, usernameY)
        return JsonResponse({"message":"success"})
    return JsonResponse({"message":"invalid method"})

@csrf_exempt
def unfollow_person(request):
    if request.method == "POST":
        usernameX = request.POST["usernameX"]
        usernameY = request.POST["usernameY"]
        delete_to_db_following_or_follower(usernameX, usernameY)
        return JsonResponse({"message":"success"})
    return JsonResponse({"message":"invalid method"})

@csrf_exempt
def list_follower(request):
    response = {"data":[]}
    if request.method == "POST":
        username = request.POST["username"]
        follower = find_db_follower(username)
        if follower is not None:
            for person in follower:
                response["data"].append({"username":person,"isfollow":is_follow_person(username,person[0])})
    return JsonResponse(response)

@csrf_exempt
def list_following(request):
    response = {"data":[]}
    if request.method == "POST":
        username = request.POST["username"]
        following = find_db_following(username)
        if following is not None:
            for person in following:
                response["data"].append({"username":person})
    return JsonResponse(response)

@csrf_exempt
def is_follow_person_API(request):
    if request.method == "POST":
        usernameX = request.POST['usernameX']
        usernameY = request.POST['usernameY']
        if (is_follow_person(usernameX, usernameY)):
            return JsonResponse({"isfollow":True})
        return JsonResponse({"isfollow":False})
    return JsonResponse({"message":"invalid"})

        
def is_follow_person(usernameX,usernameY):
    query = "SELECT * FROM public.follow WHERE usernameX = '{}' and usernameY = '{}'".format(usernameX, usernameY)
    result = connect_db(query)
    if (result):
        return True
    return False

def find_db_follower(username):
    query = "SELECT usernameX FROM public.follow WHERE usernameY = '{}'".format(username)
    result = connect_db(query)
    return result

def find_db_following(username):
    query = "SELECT usernameY FROM public.follow WHERE usernameX = '{}'".format(username)
    result = connect_db(query)
    return result

def delete_to_db_following_or_follower(usernameX, usernameY):
    try:
        query = '''DELETE FROM public."follow" WHERE usernameX = '{}' and usernameY = '{}'
                    RETURNING usernameX,usernameY'''.format(usernameX,usernameY)
        connect_db(query)
        return True, "Success"
        
    except:
        return False, "Error"    

def insert_to_db_following_or_follower(usernameX, usernameY):
    try:
        query = '''INSERT INTO public."follow"(usernameX,usernameY) VALUES('{}','{}') 
                    RETURNING usernameX,usernameY'''.format(usernameX,usernameY)
        connect_db(query)
        return True, "Success"
        
    except:
        return False, "Error"

def connect_db(query):
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "bernadius",
                                    host = "localhost",
                                    port = "5432",
                                    database = "tkai_tugas")

        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        connection.commit()
        return record 

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return None

    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")