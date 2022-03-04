from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Profile: 
    db = "golf_erd"
    def __init__( self , data ):
        self.id = data["id"]
        self.age = data["age"]
        self.headline = data["headline"]
        self.description = data["description"]
        self.handicap = data["handicap"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    # get all
    @classmethod
    def get_all (cls):
        query = "SELECT * FROM profiles JOIN users on profiles.user_id = users.id ;"
        results = connectToMySQL(cls.db).query_db(query)
        profiles = []
        for row in results:
            data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]

            }
            temp_profile = cls(row)
            temp_profile.user = user.User(data)
            profiles.append(temp_profile)
        return profiles

    # get one
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM profiles JOIN users on profiles.user_id = users.id WHERE profiles.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            temp_profile = cls(result[0])
            data = {
                "id" : result[0]["users.id"],
                "first_name" : result[0]["first_name"],
                "last_name" : result[0]["last_name"],
                "email" : result[0]["email"],
                "password" : result[0]["password"],
                "created_at" : result[0]["users.created_at"],
                "updated_at" : result[0]["users.updated_at"]

            }
            temp_profile.user = user.User(data)
            return temp_profile

    # save profile
    @classmethod
    def save(cls, data):

        query = "INSERT INTO profiles (age, headline, description, handicap, created_at, updated_at, user_id) "\
        "VALUES (%(age)s, %(headline)s, %(description)s, %(handicap)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # update profile
    @classmethod
    def update(cls, data):

        query = "UPDATE profiles SET age = %(age)s, headline = %(headline)s, description = %(description)s, "\
            "handicap = %(handicap)s, updated_at = NOW() WHERE id = %(id)s;"
        result =  connectToMySQL(cls.db).query_db(query, data)
        return result

    # validate profile
    @staticmethod
    def is_valid(profile):
        is_valid = True
        if profile["headline"] =='':
            is_valid = False
            flash("Headline is required.", "profile_error")        
        if len(profile["headline"]) < 10:
            is_valid = False
            flash("Headline should be at least 10 characters long.", "profile_error")        
        if profile["description"] =='':
            is_valid = False
            flash("Description is required.", "profile_error")  
        if len(profile["description"]) < 10:
            is_valid = False
            flash("Description should be at least 10 characters long.", "profile_error")          

        return is_valid



