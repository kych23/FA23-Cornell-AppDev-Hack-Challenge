import datetime
import hashlib
import os
import bcrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Association Tables 
free_user_table = db.Table("free_user", db.Model.metadata,
            db.Column("free_times_id", db.Integer, db.ForeignKey("freetimes.id")),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id")))

busy_user_table = db.Table("busy_user", db.Model.metadata,
            db.Column("busy_times_id", db.Integer, db.ForeignKey("busytimes.id")),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id")))

user_tag_table = db.Table("user_tag", db.Model.metadata,
            db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id")))

org_tag_table = db.Table("org_tag", db.Model.metadata,
            db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
            db.Column("org_id", db.Integer, db.ForeignKey("organizations.id")))

user_location_table = db.Table("user_location", db.Model.metadata,
            db.Column("location_id", db.Integer, db.ForeignKey("locations.id")),
            db.Column("user_id", db.Integer, db.ForeignKey("users.id")))

#User Database 
class User(db.Model):
    """
    User Class
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Authentication
    login_email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)
    
    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String, nullable=False, unique=True)
    
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String, nullable=False)
    user_pfp = db.Column(db.String, nullable=False)
    user_bio = db.Column(db.String, nullable=False)
    user_banner = db.Column(db.String, nullable=False)
    instagram = db.Column(db.String, nullable=False)
    linkedin = db.Column(db.String, nullable=False)
    public_email = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    
    user_organizations = db.relationship("User_Org", back_populates="user")
    location_prefs = db.relationship("Location", secondary = user_location_table, back_populates = "user_id")
    free_times = db.relationship("Free_Time", secondary = free_user_table, back_populates = "user_id")
    busy_times = db.relationship("Busy_Time", secondary = busy_user_table, back_populates = "user_id")
    tags = db.relationship("Tag", secondary = user_tag_table, back_populates = "user_id")
    chat_requests_sent = db.relationship("Chat_Request", back_populates="sender", foreign_keys="[Chat_Request.sender_id]")
    chat_requests_received = db.relationship("Chat_Request", back_populates="receiver", foreign_keys="[Chat_Request.receiver_id]")
    org_requests = db.relationship("Org_Request", cascade="delete")
    
    def __init__(self, **kwargs):
        """
        Initializes a User Object
        """
        self.login_email = kwargs.get("login_email", "")
        self.password_digest = bcrypt.hashpw(kwargs.get("login_password").encode("utf8"), bcrypt.gensalt(rounds=13))
        
        self.name = kwargs.get("name", "")
        self.year = kwargs.get("year", 0)
        self.major = kwargs.get("major", "")
        self.user_pfp = kwargs.get("pfp", "")
        self.user_banner = kwargs.get("banner", "")
        self.user_bio = kwargs.get("bio", "")
        self.instagram = kwargs.get("instagram", "")
        self.linkedin = kwargs.get("linkedin", "")
        self.public_email = kwargs.get("public email", "")
        self.status = kwargs.get("status", False)
        
        self.renew_session()
        
    # Authentication Methods
    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=7)
        self.refresh_token = self._urlsafe_base_64()
    
    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, refresh_token):
        """
        Verifies the update token of a user
        """
        return refresh_token == self.refresh_token
    
    # Return methods
    def safe_serialize(self):
        """
        Returns a User Object without login credentials
        """
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "major": self.major,
            "pfp": self.user_pfp,
            "banner": self.user_banner,
            "bio": self.user_bio,
            "instagram": self.instagram,
            "linkedin": self.linkedin,
            "public email": self.public_email,
            "status": self.status,
            "organizations": [a.serialize() for a in self.user_organizations],
            "tags": [tag.simple_serialize() for tag in self.tags],
            "busy times": [bt.simple_serialize() for bt in self.busy_times],
            "free times": [ft.simple_serialize() for ft in self.free_times],
            "preferred locations": [l.simple_serialize() for l in self.location_prefs],
            "org requests": [orgr.serialize() for orgr in self.org_requests],
            "chat requests sent": [crs.serialize() for crs in self.chat_requests_sent],
            "chat requests received": [crr.serialize() for crr in self.chat_requests_received]
        }
    
    def simple_serialize(self):
        """
        Returns a User object with only its name and pfp
        """
        return {
            "id": self.id,
            "name": self.name,
            "pfp": self.user_pfp
        }
    
# Organizations Database
class Organization(db.Model):
    
    """
    Organization Class
    """
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)

    # Authentication
    login_email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)
    
    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String, nullable=False, unique=True)
    
    org_pfp = db.Column(db.String)
    org_banner = db.Column(db.String)
    org_bio = db.Column(db.String) 
    
    user_organizations = db.relationship("User_Org", back_populates="organization")
    org_requests = db.relationship("Org_Request", cascade="delete")
    tags = db.relationship("Tag", secondary = org_tag_table, back_populates = "org_id")
    
    def __init__(self, **kwargs):
        """
        Initializes a Organization Object
        """
        self.login_email = kwargs.get("login_email", "")
        self.password_digest = bcrypt.hashpw(kwargs.get("login_password").encode("utf8"), bcrypt.gensalt(rounds=13))
        
        self.name = kwargs.get("name", "")
        self.org_pfp = kwargs.get("pfp", "")
        self.org_bio = kwargs.get("bio", "")
        self.org_banner = kwargs.get("banner", "")
        
        self.renew_session()
    
    # Authentication Methods
    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=7)
        self.refresh_token = self._urlsafe_base_64()
    
    def verify_password(self, password):
        """
        Verifies the password of a org
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a org
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, refresh_token):
        """
        Verifies the update token of a user
        """
        return refresh_token == self.refresh_token
    
    # Return Methods
    def serialize(self):
        """
        Returns organization
        """
        return {
            "id": self.id,
            "name": self.name,
            "pfp": self.org_pfp,
            "banner": self.org_banner,
            "bio": self.org_bio,
            "users": [user.serialize() for user in self.user_organizations],
            "tags": [tag.simple_serialize() for tag in self.tags],
            "org requests": [orgr.serialize() for orgr in self.org_requests]
        }
        
    def simple_serialize(self):
        """
        Returns organization without the users and tags
        """
        return {
            "id": self.id,
            "name": self.name,
            "org pfp": self.org_pfp,
        }
    
# User Org Database (Association)
class User_Org(db.Model):
    __tablename__ = 'user_organization'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    position = db.Column(db.Integer, nullable = False)

    user = db.relationship("User", back_populates="user_organizations")
    organization = db.relationship("Organization", back_populates="user_organizations")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "organization_id": self.organization_id,
            "position": self.position
        }

# Free Times Database
class Free_Time(db.Model):
    """ 
    Free Time Class
    """
    __tablename__ = "freetimes"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    start_time = db.Column(db.Integer, nullable = False)
    month = db.Column(db.Integer, nullable = False)
    day = db.Column(db.Integer, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    weekday = db.Column(db.Integer, nullable = False)
    
    user_id = db.relationship("User", secondary = free_user_table, back_populates = "free_times")
    
    def __init__(self, **kwargs):
        """
        Initializes a Free_Time Object
        """
        self.day = kwargs.get("day", -1)
        self.month = kwargs.get("month", -1)
        self.year = kwargs.get("year", -1)
        self.weekday = kwargs.get("weekday", -1)
        self.start_time = kwargs.get("start_time", 0)
        
    def serialize(self):
        """
        Returns the free times and all the users with that time
        """
        return {
            "id": self.id,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "weekday": self.weekday,
            "start time": self.start_time,
            "users": [user.simple_serialize() for user in self.user_id]
        }
        
    def simple_serialize(self):
        """
        Returns the free times without the users
        """
        return {
            "id": self.id,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "weekday": self.weekday,
            "start time": self.start_time
        }

# Busy Times Database
class Busy_Time(db.Model):
    """ 
    Busy Time Class
    """
    __tablename__ = "busytimes"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    start_time = db.Column(db.Integer, nullable = False)
    month = db.Column(db.Integer, nullable = False)
    day = db.Column(db.Integer, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    weekday = db.Column(db.Integer, nullable = False)
        
    user_id = db.relationship("User", secondary = busy_user_table, back_populates = "busy_times")
    
    def __init__(self, **kwargs):
        """
        Initializes a Busy_Time Object
        """
        self.day = kwargs.get("day", -1)
        self.month = kwargs.get("month", -1)
        self.year = kwargs.get("year", -1)
        self.weekday = kwargs.get("weekday", -1)
        self.start_time = kwargs.get("start_time", 0)

    def delete_row(self, bt_id, u_id):
        row = db.session.query(busy_user_table).filter_by(user_id=u_id, free_times_id=bt_id).one()
        db.session.delete(row)


    def serialize(self):
        """
        Returns the busy times and all the users with that time
        """
        return {
            "id": self.id,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "weekday": self.weekday,
            "start time": self.start_time,
            "users": [user.simple_serialize() for user in self.user_id]
        }
        
    def simple_serialize(self):
        """
        Returns the busy times without the users
        """
        return {
            "id": self.id,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "weekday": self.weekday,
            "start time": self.start_time,
        }
    
# Tags Database
class Tag(db.Model):
    """ 
    Tag Class
    """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    text = db.Column(db.String, nullable = False)
    
    user_id = db.relationship("User", secondary = user_tag_table, back_populates = "tags")
    org_id = db.relationship("Organization", secondary = org_tag_table, back_populates = "tags")
    
    def __init__(self, **kwargs):
        """
        Initializes a Tag Object
        """
        self.text = kwargs.get("text", "")
        
    def serialize(self):
        """
        Returns tag
        """
        return {
            "id": self.id,
            "text": self.text,
            # 'users' is a list of names
            "users": [user.simple_serialize() for user in self.user_id],
            # 'organizations' is a list of the org title
            "organizations": [org.simple_serialize() for org in self.org_id]
        }
        
    def simple_serialize(self):       
        """
        Returns organization without the users and tags
        """
        return {
            "id": self.id,
            "text": self.text
        }
    
# Locations Databse
class Location(db.Model):
    """
    Location Class
    """
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    location = db.Column(db.String, nullable = False)
    
    user_id = db.relationship("User", secondary = user_location_table, back_populates = "location_prefs")
    def __init__(self, **kwargs):
        """
        Initializes a Location Object
        """
        self.location = kwargs.get("location", "")
        
    def serialize(self):
        """
        Return a Location object
        """
        return {
            "id": self.id,
            "location": self.location,
            "users": [user.simple_serialize() for user in self.user_id],
        }
        
    def simple_serialize(self):
        """
        Return a location object without users
        """
        return {
            "id": self.id,
            "location": self.location
        }
    
# Organization Request Database   
class Org_Request(db.Model):
    """
    Organization Request Class
    """
    __tablename__ = "org_requests"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    accepted = db.Column(db.Boolean) 
    position = db.Column(db.String, nullable = False)   
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    org_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable = False)
    
    def __init__(self, **kwargs):
        """
        Initializes an Org_Request Object
        """
        self.accepted = kwargs.get("accepted", None)
        self.position = kwargs.get("position", "")
        self.user_id = kwargs.get("user_id", 0)
        self.org_id = kwargs.get("org_id")
        
    def serialize(self):
        """
        Return an organization request object
        """
        return {
            "id": self.id,
            "position": self.position,
            "accepted": self.accepted,
            "user id": self.user_id,
            "organization id": self.org_id
        }

# Coffee Chat Request Database
class Chat_Request(db.Model):
    """
    Coffee Chat Request Class
    """
    __tablename__ = "chat_requests"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    start_time = db.Column(db.Integer, nullable = False)
    month = db.Column(db.Integer, nullable = False)
    day = db.Column(db.Integer, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    weekday = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String, nullable = False)
    message = db.Column(db.String, nullable = False)
    
    accepted = db.Column(db.Boolean)
    
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="chat_requests_sent")
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="chat_requests_received")

    def __init__(self, **kwargs):        

        """
        Initializes a Chat Request Object
        """
        self.start_time = kwargs.get("start_time", 0)
        self.day = kwargs.get("day", -1)
        self.month = kwargs.get("month", -1)
        self.year = kwargs.get("year", -1)
        self.weekday = kwargs.get("weekday", -1)
        self.location = kwargs.get("location", "")
        self.message = kwargs.get("message", "")
        self.sender_id = kwargs.get("sender id", "")
        self.receiver_id = kwargs.get("receiver id", "")
        self.accepted = None
        
    def serialize(self):
        """
        Return a chat request object
        """
        return {
            "id": self.id,
            "start time": self.start_time,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "weekday": self.weekday,
            "location": self.location,
            "message": self.message,
            "accepted": self.accepted,
            "sender": self.sender_id, 
            "receiver": self.receiver_id
        }           








