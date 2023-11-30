"""
DAO (Data Access Object) file

Helper file containing functions for accessing data in our database
"""

from db import db, Organization


def get_org_by_email(email):
    """
    Returns a user object from the database given an email
    """
    return Organization.query.filter(Organization.login_email == email).first()


def get_org_by_session_token(session_token):
    """
    Returns a user object from the database given a session token
    """
    return Organization.query.filter(Organization.session_token == session_token).first()


def get_org_by_refresh_token(refresh_token):
    """
    Returns a user object from the database given an update token
    """
    return Organization.query.filter(Organization.refresh_token == refresh_token).first()


def verify_org_credentials(email, password):
    """
    Returns true if the credentials match, otherwise returns false
    """
    possible_org = get_org_by_email(email)
    if possible_org is None: 
        return False, None 
    
    return possible_org.verify_password(password), possible_org 


def create_org(name, email, password):
    """
    Creates a User object in the database

    Returns if creation was successful, and the User object
    """
    possible_org = get_org_by_email(email)
    if possible_org is not None: 
        return False, possible_org

    org = Organization(name=name, login_email=email, login_password=password)
    db.session.add(org)
    db.session.commit()
    return True, org


def renew_org_session(refresh_token):
    """
    Renews a user's session token
    
    Returns the User object
    """
    possible_org = get_org_by_refresh_token(refresh_token) 
    if possible_org is None: 
        raise Exception("invalid refresh token")
    possible_org.renew_session() 
    db.session.commit() 
    return possible_org
