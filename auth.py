from flask import flash, redirect, url_for
from flask_login import UserMixin, LoginManager, current_user
from app import w3, manager
import enum
from functools import wraps


class User(UserMixin):
    """
    Lightweight class for representing a user address.
    """    
    def __init__(self, address: str, is_manager: bool):
        self.id = address
        self.is_admin = is_manager
    
    def __repr__(self):
        return f"User({self.id}, {self.is_admin})"

def manager_required(f):
    """
    Decorator for views that require the user to be the manager of the contract.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Only the owner can perform this operation")
            return redirect(url_for("home.index"))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """
    Decorator for views that require the user to be a normal user.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash("Only normal users can can perform this operation")
            return redirect(url_for("home.index"))
        return f(*args, **kwargs)
    return decorated_function

def init_login_manager(app):
    """
    Initialize the login manager.
    """
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
                return User(account, True if account == manager.address else False)

    return login_manager
    