from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import round
from flask_app.models import profile
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
# model the class after the users table from our database
class User:
    db = "golf_erd"
    def __init__( self , data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # save user
    @classmethod
    def save(cls, data):
        hash = bcrypt.generate_password_hash(data["password"])
        user = {
            "first_name": data ["first_name"],
            "last_name": data ["last_name"],
            "email": data ["email"],
            "password": hash
        }

        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) "\
        "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL(cls.db).query_db(query, user)
        return result

    # get one email
    @classmethod
    def get_by_email (cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    # get one id
    @classmethod
    def get_by_id (cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    # validate login
    @classmethod
    def validate_login(cls, data):
        # If user exists in database
        user_in_db = User.get_by_email(data)

        # If user not in database
        if not user_in_db: 
            flash ("Invalid email/password", "invalid_email")
            return False
        
        # Password's don't match
        if not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash ("Invalid email/password", "invalid_email")
            return False
        
        return True

    # Validate user information

    @staticmethod
    def is_valid(user):
        is_valid = True
        if len(user['first_name']) < 2 :
            is_valid = False
            flash("First name must be at least 2 characters.", "login_error")
        if len(user['last_name']) < 2 :
            is_valid = False
            flash("Last name must be at least 2 characters.", "login_error")
        
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('golf_erd').query_db(query, user)
        if len(results) >= 1:
            flash ("Email already taken.", "login_error")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", "login_error")
            is_valid = False

        if len(user['password']) < 8 :
            is_valid = False
            flash("Password must be at least 8 characters.", "login_error")
        if user['password'] !=  user['confirm'] :
            is_valid = False
            flash("Passwords do not match", "login_error")

        return is_valid

    # delete account
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # query to get plans for user
    @classmethod
    def get_plans_for_user (cls, data):
        query = "SELECT * FROM users LEFT JOIN rounds on users.id = rounds.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls ( results[0])
        
        user.rounds = []
        if results[0]["rounds.id"]:
            for row_from_db in results:
                round_data = {
                    "id" : row_from_db["rounds.id"],
                    "course_name" : row_from_db["course_name"],
                    "tee_time" : row_from_db["tee_time"],
                    "description" : row_from_db["description"],
                    "created_at" : row_from_db["rounds.created_at"],
                    "updated_at" : row_from_db["rounds.updated_at"]
                }

                user.rounds.append( round.Round ( round_data) )
        return user

    # query to get profiles for user
    @classmethod
    def get_profile_for_user (cls, data):
        query = "SELECT * FROM users LEFT JOIN rounds on users.id = rounds.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls ( results[0])
        
        user.profile = []
        if results[0]["profiles.id"]:
            for row_from_db in results:
                profile_data = {
                    "id" : row_from_db["profiles.id"],
                    "age" : row_from_db["course_name"],
                    "headline" : row_from_db["tee_time"],
                    "description" : row_from_db["description"],
                    "handicap" : row_from_db["handicap"],
                    "created_at" : row_from_db["profiles.created_at"],
                    "updated_at" : row_from_db["profiles.updated_at"]
                }

                user.profile.append( profile.Profile ( profile_data) )
        return user