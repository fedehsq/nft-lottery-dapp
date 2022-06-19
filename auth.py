from flask import flash, redirect, url_for
from flask_login import UserMixin, LoginManager, current_user
from app import w3, owner
import enum
from functools import wraps

"""
Lightweight class for representing a user.
"""
class User(UserMixin):
    
    def __init__(self, address: str, is_admin: bool):
        self.id = address
        self.is_admin = is_admin
    
    def __repr__(self):
        return f"User({self.id}, {self.is_admin})"

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Only the owner can perform this operation")
            return redirect(url_for("home.index"))
        return f(*args, **kwargs)
    return decorated_function

def init_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = u"Please login to perform this operation."

    @login_manager.user_loader
    def load_user(user_id):
        """
        :param user_id: The address of the user to search for in w3 accounts
        :return: the user object
        """
        # Return a User object searching in w3 accounts by address
        accounts = w3.eth.accounts
        for account in accounts:
            if account == user_id:
                return User(account, True if account == owner.address else False)

    return login_manager
    