from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user


class Round:
    db = "golf_erd"

    def __init__(self, data):
        self.id = data["id"]
        self.course_name = data["course_name"]
        self.tee_time = data["tee_time"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # get all
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM rounds JOIN users on rounds.user_id = users.id ;"
        results = connectToMySQL(cls.db).query_db(query)
        rounds = []
        for row in results:
            data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]

            }
            temp_round = cls(row)
            temp_round.user = user.User(data)
            rounds.append(temp_round)
        return rounds

    # get one
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM rounds JOIN users on rounds.user_id = users.id WHERE rounds.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            temp_round = cls(result[0])
            data = {
                "id": result[0]["users.id"],
                "first_name": result[0]["first_name"],
                "last_name": result[0]["last_name"],
                "email": result[0]["email"],
                "password": result[0]["password"],
                "created_at": result[0]["users.created_at"],
                "updated_at": result[0]["users.updated_at"]

            }
            temp_round.user = user.User(data)
            return temp_round

    # save round
    @classmethod
    def save(cls, data):

        query = "INSERT INTO rounds (course_name, tee_time, description, created_at, updated_at, user_id) "\
            "VALUES (%(course_name)s, %(tee_time)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # update round
    @classmethod
    def update(cls, data):

        query = "UPDATE rounds SET course_name = %(course_name)s, tee_time = %(tee_time)s, description = %(description)s, "\
            "updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # delete round
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM rounds WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # validate round
    @staticmethod
    def is_valid(round):
        is_valid = True
        if round["course_name"] == '':
            is_valid = False
            flash("Course name is required.", "round_error")
        if len(round["course_name"]) < 5:
            is_valid = False
            flash("Course name should be at least 5 characters long.", "round_error")
        if round["tee_time"] == '':
            is_valid = False
            flash("Must select a date and time.", "round_error")
        if round["description"] == '':
            is_valid = False
            flash("Description about round is required.", "profile_error")
        if len(round["description"]) < 10:
            is_valid = False
            flash("Description should be at least 10 characters long.", "round_error")

        return is_valid
