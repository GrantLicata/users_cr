
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self ,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,created_at,updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users_schema').query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        print(query)
        return connectToMySQL('users_schema').query_db( query, data )

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db( query, data )

    @staticmethod
    def validate_user(data):
        is_valid = True # we assume this is true
        if len(data['first_name']) < 1:
            flash("First name is required.")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required.")
            is_valid = False
        if len(data['email']) < 1:
            flash("Email is required")
            is_valid = False
        elif len(data['email']) > 0: 
            flash("Invalid email address!")
            is_valid = False
        return is_valid