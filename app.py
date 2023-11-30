from db import db
from flask import Flask, request
import json

from db import User, Organization, Busy_Time, Free_Time, Tag, Location, Org_Request, Chat_Request, User_Org, Position

import users_dao
import orgs_dao
import datetime

app = Flask(__name__)
db_filename = "lattelink.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

# ----------------------------------------------------------------------------
@app.route("/")
def base():
    return success_response("this is the base route")

# ------------------  User Login Authentication Routes -----------------------
def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, failure_response("Missing Authentication header", 400)

    # Bearer <Token>
    bearer_token = auth_header.replace("Bearer", "").strip()
    if not bearer_token:
        return False, failure_response("Invalid Authorization header", 400)
    return True, bearer_token

@app.route("/register/user/", methods=["POST"])
def register_user_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("login_email")
    password = body.get("login_password")

    if None in (name, email, password):
        return failure_response("Invalid body", 400)
    
    created, user = users_dao.create_user(name, email, password)
    if not created:
        return failure_response("User already exists", 400)
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token
    }, 201)
    
@app.route("/login/user/", methods=["POST"])
def user_login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    email = body.get("login_email")
    password = body.get("login_password")
    
    if None in (email, password):
        return failure_response("Invalid body", 400)
    
    success, user = users_dao.verify_user_credentials(email, password)
    if not success:
        return failure_response("Invalid credentials", 400)
    user.renew_session()
    db.session.commit()
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token
    }, 200)

@app.route("/logout/user/", methods=["POST"])
def user_logout():
    """
    Endpoint for logging out a user
    """    
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    user.session_expiration = datetime.datetime.now()
    db.session.commit()
    return success_response("You have successfully logged out", 200)
    
@app.route("/session/user/", methods=["POST"])
def refresh_user_session():
    """
    Endpoint for updating a user's session
    """
    success, response = extract_token(request)
    if not success:
        return response
    refresh_token = response
    try:
        user = users_dao.renew_user_session(refresh_token)
    except:
        return failure_response("Invalid refresh token", 400)
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "refresh_token": user.refresh_token
    }, 200)

# -----------------  Organization Login Authentication Routes ------------------

@app.route("/register/org/", methods=["POST"])
def register_org_account():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("login_email")
    password = body.get("login_password")

    if None in (name, email, password):
        return failure_response("Invalid body", 400)
    
    created, org = orgs_dao.create_org(name, email, password)
    if not created:
        return failure_response("User already exists", 400)
    
    return success_response({
        "session_token": org.session_token,
        "session_expiration": str(org.session_expiration),
        "refresh_token": org.refresh_token
    }, 201)
    
@app.route("/login/org/", methods=["POST"])
def org_login():
    """
    Endpoint for logging in a user
    """
    body = json.loads(request.data)
    email = body.get("login_email")
    password = body.get("login_password")
    
    if None in (email, password):
        return failure_response("Invalid body", 400)
    
    success, org = orgs_dao.verify_org_credentials(email, password)
    if not success:
        return failure_response("Invalid credentials", 400)
    org.renew_session()
    db.session.commit()
    return success_response({
        "session_token": org.session_token,
        "session_expiration": str(org.session_expiration),
        "refresh_token": org.refresh_token
    }, 201)

@app.route("/logout/org/", methods=["POST"])
def org_logout():
    """
    Endpoint for logging out a user
    """    
    success, response = extract_token(request)
    if not success:
        return response
    session_token = response
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    org.session_expiration = datetime.datetime.now()
    db.session.commit()
    return success_response("You have successfully logged out", 200)
    
@app.route("/session/org/", methods=["POST"])
def refresh_org_session():
    """
    Endpoint for updating a user's session
    """
    success, response = extract_token(request)
    if not success:
        return response
    refresh_token = response
    try:
        org = orgs_dao.renew_org_session(refresh_token)
    except:
        return failure_response("Invalid refresh token", 400)
    
    return success_response({
        "session_token": org.session_token,
        "session_expiration": str(org.session_expiration),
        "refresh_token": org.refresh_token
    }, 200)


# -------------------------------- User Routes --------------------------------

# Route : Get all users
@app.route("/api/users/", methods = ["GET"])
def get_all_users():
    users = [user.simple_serialize() for user in User.query.all()]
    return success_response({"users": users})

# Route : Get specific user
@app.route("/api/users/<int:user_id>/", methods = ["GET"])
def get_specific_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 404)
    return success_response(user.safe_serialize())

# Route : Delete a user
@app.route("/api/users/<int:user_id>/", methods = ["DELETE"])
def delete_user(user_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.safe_serialize())

# Route : Update a current user (can't change login email, login password, or name)
@app.route("/api/users/<int:user_id>/", methods=["PUT"])
def update_user(user_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id=user_id).first()
    
    body = json.loads(request.data)
    year = body.get("year")
    major = body.get("major")
    pfp = body.get("pfp")
    bio = body.get("bio")
    banner = body.get("banner")
    instagram = body.get("instagram")
    linkedin = body.get("linkedin")
    email = body.get("email")
    status = body.get("status")
    
    if year is not None:
        user.year = year
    if major is not None:
        user.major = major
    if pfp is not None:
        user.user_pfp = pfp
    if bio is not None:
        user.user_bio = bio
    if banner is not None:
        user.banner = banner
    if instagram is not None:
        user.instagram = instagram
    if linkedin is not None:
        user.linkedin = linkedin
    if email is not None:
        user.public_email = email
    if status is not None:
        user.status = status
        # Removes all the free times from user if they are not open to interview others
        if not status:
            user.free_times.clear()

    db.session.commit()
        
    return success_response(user.safe_serialize())

# -------------------------------- Organization Routes --------------------------------

# Create new organization 
@app.route("/api/orgs/", methods = ["POST"])
def create_organization():
    body = json.loads(request.data)
    if body.get("name") is None:
        return failure_response("One or more fields not supplied", 400)
    new_org = Organization(name = body.get("name"), org_pfp = body.get("pfp"), org_banner = body.get("banner"), org_bio = body.get("bio"))
    db.session.add(new_org)
    db.session.commit()
    return success_response(new_org.serialize(), 201)

# Route : Get all organizations
@app.route("/api/orgs/", methods = ["GET"])
def get_all_orgs():
    orgs = [org.simple_serialize() for org in Organization.query.all()]
    return success_response({"organizations": orgs})

# Route : get organization by ID
@app.route("/api/org/<int:org_id>/", methods = ["GET"])
def get_org_by_id(org_id):
    org = Organization.query.filter_by(id = org_id).first()
    return success_response(org.serialize(), 200)

# Route : Update org profile 
@app.route("/api/orgs/<int:org_id>/", methods = ["PUT"])
def update_org(org_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400)

    body = json.loads(request.data)
    org = Organization.query.filter_by(id=org_id).first()

    name = body.get("name")
    pfp = body.get("pfp")
    banner = body.get("banner")
    bio = body.get("bio")

    org.name = name 
    org.org_pfp = pfp
    org.org_banner = banner
    org.org_bio = bio 
    db.session.commit()
    
    return success_response(org.serialize(), 200)

# Route : Delete org profile 
@app.route("/api/orgs/<int:org_id>/", methods = ["DELETE"])
def delete_org(org_id):
    # Authentication 
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400)
    
    org = Organization.query.filter_by(id=org_id).first()
    if org is None:
        return failure_response("Organization not found")
    db.session.delete(org)
    db.session.commit()
    return success_response(org.simple_serialize())

# -------------------------------- Location Routes --------------------------------

# Route : Add preferred location to user
@app.route("/api/location/<int:user_id>/", methods = ["POST"])
def add_loc_to_user(user_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    location_text = body.get("location")
    if location_text is None:
        return failure_response("One or more fields not supplied", 400)
    
    current_user = User.query.filter_by(id = user_id).first()
    if current_user is None:
        return failure_response("User not found", 404)
    
    current_location = Location.query.filter_by(location = location_text).first()

    if current_location in current_user.location_prefs:
        return failure_response("Location already exists in organization", 400)
    
    if current_location is None: 
        new_location = Location(location = location_text)    
        db.session.add(new_location)
        current_user.location_prefs.append(new_location)
    else: 
        if current_location not in current_user.location_prefs:
            current_user.location_prefs.append(current_location)
    
    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_user.simple_serialize())
    dictionary.update({"location prefs": [t.simple_serialize() for t in Location.query.filter(Location.user_id.contains(current_user))]})
    
    return success_response(dictionary)

#Route : Delete location from user 
@app.route("/api/locations/<int:l_id>/user/<int:u_id>/", methods = ["DELETE"])
def delete_loc_from_user(l_id, u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id = u_id).first()
    location = Location.query.filter_by(id=l_id).first()

    if user is None or location is None: 
        return failure_response("user not found", 404)
    
    try:
        user.location_prefs.remove(location)

    except ValueError as e:
        return failure_response("Location does not exist in user", 404)

    db.session.commit()

    return success_response(location.simple_serialize(), 200)

# -------------------------------- Tag Routes --------------------------------

# Route : Get all tags
@app.route("/api/tags/", methods = ["GET"])
def get_all_tags():
    tags = [tag.simple_serialize() for tag in Tag.query.all()]
    return success_response({"tags": tags})

# Route : Get specific tag
@app.route("/api/tags/<int:tag_id>/", methods = ["GET"])
def get_specific_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        return failure_response("Tag not found", 404)
    return success_response(tag.serialize())

# Route : Get all tags from a specific id
@app.route("/api/tags/<int:new_id>/tags/", methods = ["GET"])
def get_tags_by_user(new_id):
    body = json.loads(request.data)
    type = body.get("type")
    if type == "user":
        user = User.query.filter_by(id=new_id).first()
        if user is None:
            return failure_response("User not found", 404)
        dictionary = {"tags": []}
        for tag in user.tags:
            dictionary["tags"].append(tag.simple_serialize())
    elif type == "organization":
        org = Organization.query.filter_by(id = new_id).first()
        if org is None:
            return failure_response("Organization not found", 404)
        dictionary = {"tags": []}
        for tag in org.tags:
            dictionary["tags"].append(tag.simple_serialize())
    else:
        return failure_response("input not spelled correctly", 400)
    return success_response(dictionary,200)

#Route : Add tag to user 
@app.route("/api/tags/user/<int:u_id>/", methods = ["POST"])
def add_tag_to_user(u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    tag_text = body.get("text")
    if tag_text is None:
        return failure_response("One or more fields not supplied", 400)
    
    current_user = User.query.filter_by(id = u_id).first()
    if current_user is None:
        return failure_response("User not found", 404)

    current_tag = Tag.query.filter_by(text = tag_text).first()
    
    if current_tag in current_user.tags:
        return failure_response("Tag already exists in user", 400)
    
    if current_tag is None: 
        new_tag = Tag(text = tag_text)    
        db.session.add(new_tag)
        current_user.tags.append(new_tag)
    else: 
        if current_tag not in current_user.tags:
            current_user.tags.append(current_tag)
    
    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_user.simple_serialize())
    dictionary.update({"tags": [t.simple_serialize() for t in Tag.query.filter(Tag.user_id.contains(current_user))]})
    
    return success_response(dictionary)

#Route : Delete tag from user 
@app.route("/api/tags/<int:t_id>/user/<int:u_id>/", methods = ["DELETE"])
def delete_tag_from_user(t_id, u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id = u_id).first()
    tag = Tag.query.filter_by(id=t_id).first()
    if user is None or tag is None: 
        return failure_response("user not found", 404)
    
    try:
        user.tags.remove(tag)

    except ValueError as e:
        return failure_response("Tag does not exist in user", 404)

    db.session.commit()

    return success_response(tag.simple_serialize(), 200)

# Route : add tag to organization 
@app.route("/api/tags/org/<int:o_id>/", methods = ["POST"])
def add_tag_to_org(o_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    tag_text = body.get("text")
    if tag_text is None:
        return failure_response("One or more fields not supplied", 400)
    
    current_org = Organization.query.filter_by(id = o_id).first()
    if current_org is None:
        return failure_response("Organization not found", 404)
    
    current_tag = Tag.query.filter_by(text = tag_text).first()
    
    if current_tag in current_org.tags:
        return failure_response("Tag already exists in organization", 400)
    
    if current_tag is None: 
        new_tag = Tag(text = tag_text)    
        db.session.add(new_tag)
        current_org.tags.append(new_tag)
    else: 
        if current_tag not in current_org.tags:
            current_org.tags.append(current_tag)
    
    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_org.simple_serialize())
    dictionary.update({"tags": [t.simple_serialize() for t in Tag.query.filter(Tag.org_id.contains(current_org))]})
    
    return success_response(dictionary)

#Route : Delete tag from org 
@app.route("/api/tags/<int:t_id>/org/<int:o_id>/", methods = ["DELETE"])
def delete_tag_from_org(t_id, o_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    org = Organization.query.filter_by(id = o_id).first()
    tag = Tag.query.filter_by(id=t_id).first()
    
    if org is None or tag is None: 
        return failure_response("organization not found", 404)
    
    try:
        org.tags.remove(tag)
    except ValueError as e:
        return failure_response("Tag does not exist in organization", 404)

    db.session.commit()

    return success_response(tag.simple_serialize(), 200)

# -------------------------------- Time Routes --------------------------------

#Route : Add a free time to user
@app.route("/api/ft/<int:u_id>/", methods = ["POST"])
def add_ft_to_user(u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    new_month = body.get("month")
    new_day = body.get("day")
    new_year = body.get("year")
    new_weekday = body.get("weekday")
    start_t = body.get("start time")
    
    if None in (new_day, start_t, new_month, new_year, new_weekday):
        return failure_response("One or more fields not supplied", 400)
    
    current_user = User.query.filter_by(id = u_id).first()
    if current_user is None:
        return failure_response("User not found", 404)
    
    if current_user.status == False:
        return failure_response("User is not open to coffee chatting", 400)
    
    new_time = Busy_Time.query.filter_by(month = new_month, day = new_day, year = new_year, weekday = new_weekday, start_time = start_t).first()
    
    if new_time in current_user.busy_times:
        return failure_response("user busy at this time, cannot add free time", 400)
    
    current_free_time = Free_Time.query.filter_by(month = new_month, day = new_day, year = new_year, weekday = new_weekday, start_time = start_t).first()

    if current_free_time is None: 
        new_free_time = Free_Time(month = new_month, day = new_day, year = new_year, weekday = new_weekday, start_time = start_t)    
        db.session.add(new_free_time)
        current_user.free_times.append(new_free_time)
    else: 
        if current_free_time not in current_user.free_times:
            current_user.free_times.append(current_free_time)
        else: 
            return failure_response("Free time already exists in user", 400)

    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_user.simple_serialize())
    dictionary.update({"free times": [bt.simple_serialize() for bt in Free_Time.query.filter(Free_Time.user_id.contains(current_user))]})
    
    return success_response(dictionary)

# Route : Remove a free time from user
@app.route("/api/ft/<int:ft_id>/user/<int:u_id>/", methods = ["DELETE"])
def remove_ft_from_user(u_id, ft_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id = u_id).first()
    ft = Free_Time.query.filter_by(id=ft_id).first()
    
    if user is None or ft is None: 
        return failure_response("user or free time not found", 404)
    
    try:
        user.free_times.remove(ft)
        db.session.commit()
    except ValueError as e:
        return failure_response("Time does not exist in user", 404)

    return success_response(ft.simple_serialize(), 200)

# Route : Add a busy time to user
@app.route("/api/bt/<int:u_id>/", methods = ["POST"])
def add_bt_to_user(u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    new_month = body.get("month")
    new_day = body.get("day")
    new_year = body.get("year")
    new_weekday = body.get("weekday")
    start_t = body.get("start time")
    
    if None in (new_day, start_t, new_month, new_year, new_weekday):
        return failure_response("One or more fields not supplied", 400)
    
    current_user = User.query.filter_by(id = u_id).first()
    if current_user is None:
        return failure_response("User not found", 404)
    
    current_busy_time = Busy_Time.query.filter_by(month = new_month, day = new_day, year = new_year, weekday = new_weekday, start_time = start_t).first()

    if current_busy_time is None: 
        new_busy_time = Busy_Time(month = new_month, day = new_day, year = new_year, weekday = new_weekday, start_time = start_t)    
        db.session.add(new_busy_time)
        current_user.busy_times.append(new_busy_time)
    else: 
        if current_busy_time not in current_user.busy_times:
            current_user.busy_times.append(current_busy_time)
        else: 
            return failure_response("Busy time already exists in user", 400)

    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_user.simple_serialize())
    dictionary.update({"busy times": [bt.simple_serialize() for bt in Busy_Time.query.filter(Busy_Time.user_id.contains(current_user))]})
    
    return success_response(dictionary)

# Route : Remove a busy time from user 
@app.route("/api/bt/<int:bt_id>/user/<int:u_id>/", methods = ["DELETE"])
def remove_bt_from_user(u_id, bt_id): 
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    user = User.query.filter_by(id = u_id).first()
    bt = Busy_Time.query.filter_by(id=bt_id).first()
    
    if user is None or bt is None: 
        return failure_response("user not found", 404)
    
    try:
        user.busy_times.remove(bt)
    except ValueError as e:
        return failure_response("Time does not exist in user", 404)

    db.session.commit()

    return success_response(bt.simple_serialize(), 200)

# -------------------------------- Coffee Chat Request Routes --------------------------------

# Route : Get Coffee Chat Requests from a specific user
@app.route("/api/cr/<int:user_id>/", methods = ["GET"])
def get_user_cr(user_id):
    body = json.loads(request.data)
    status = body.get("status")
    dictionary = {}
    dictionary.update(User.query.filter_by(id = user_id).first().simple_serialize())
    if status == "received":
        dictionary.update({"received chat requests": [cr.serialize() for cr in Chat_Request.query.filter_by(receiver_id = user_id)]})
        return success_response(dictionary)
    elif status == "sent":
        dictionary.update({"sent chat requests": [cr.serialize() for cr in Chat_Request.query.filter_by(sender_id = user_id)]})
        return success_response(dictionary)
    
# Route : Get all confirmed coffee chats from user
@app.route("/api/c_cr/<int:user_id>/", methods = ["GET"])
def get_user_conf_cr(user_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    dictionary = {}
    dictionary.update(User.query.filter_by(id = user_id).first().simple_serialize())
    dictionary.update({"confirmed chat requests": [cr.serialize() for cr in Chat_Request.query.filter_by(sender_id = user_id, accepted = True)]})
    dictionary["confirmed chat requests"].append([cr.serialize() for cr in Chat_Request.query.filter_by(receiver_id = user_id, accepted = True)])
    return success_response(dictionary, 200)

#Route : create new coffee chat request from user 
@app.route("/api/cr/<int:u_id>/", methods = ["POST"])
def create_new_chat_request(u_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data) 
    r_id = body.get("receiver id")
    s_time = body.get("start time")
    new_month = body.get("month")
    new_day = body.get("day")
    new_weekday = body.get("weekday")
    new_year = body.get("year") 
    new_message = body.get("message")
    new_location = body.get("location")
    
    if None in (r_id, s_time, new_day, new_month, new_year, new_weekday, new_message, new_location):
        return failure_response("One or more fields not supplied", 400)
    
    if r_id == u_id:
        return failure_response("Cannot request coffee chat with self", 400)
    
    current_user = User.query.filter_by(id = u_id).first()
    receiver_user = User.query.filter_by(id = r_id).first()

    if current_user is None:
        return failure_response("User not found", 404)
    if receiver_user is None:
        return failure_response("User not found", 404)
    
    if receiver_user.status == False: 
        return failure_response("User is not open to coffee chatting", 400)
    
    request_time = Busy_Time.query.filter_by(weekday = new_weekday, month = new_month, day = new_day, year = new_year, start_time = s_time).first()
    
    if request_time is None: 
        request_time = Busy_Time(start_time = s_time, month = new_month, day = new_day, year = new_year, weekday = new_weekday)
        db.session.add(request_time)
        db.session.commit()

    if current_user.status: 
        if request_time in current_user.free_times or request_time in current_user.busy_times:
            return failure_response("Time conflict, coffee chat cannot be requested (true)", 400)
        else: 
            current_user.busy_times.append(request_time)
            new_cr = Chat_Request(location = new_location, month = new_month, day = new_day, year = new_year, weekday = new_weekday, 
                              start_time = s_time, message = new_message, sender_id = u_id, receiver_id = r_id)
            current_user.chat_requests_sent.append(new_cr)
            receiver_user.chat_requests_received.append(new_cr)
            db.session.commit()
    else: 
        if request_time in current_user.busy_times:
            return failure_response("Request already made at this time or time conflict.", 400)
        else: 
            current_user.busy_times.append(request_time)
            new_cr = Chat_Request(location = new_location, month = new_month, day = new_day, year = new_year, weekday = new_weekday, 
                              start_time = s_time, message = new_message, sender_id = u_id, receiver_id = r_id)
            current_user.chat_requests_sent.append(new_cr)
            receiver_user.chat_requests_received.append(new_cr)
            db.session.commit()
    
    dictionary = {}
    dictionary.update(current_user.simple_serialize())
    dictionary.update({"coffee chat requests": [cr.serialize() for cr in Chat_Request.query.filter_by(sender = current_user)]})
    
    return success_response(dictionary) 
    
# Route : Accept or deny coffee chat requests 
@app.route("/api/cr/<int:cr_id>/user/<int:user_id>/", methods = ["POST"])
def accept_chat_request(cr_id, user_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    accepted_response = body.get("accepted")
    cc_req = Chat_Request.query.filter_by(id = cr_id).first()
    if User.query.get(user_id) is None:
        return failure_response("User does not exist", 404)
    if cc_req is None:
        return failure_response("Coffee Chat Request does not exist", 404)
    if cc_req.receiver_id != user_id:
        return failure_response("User is not the receiver of this coffee chat request", 400)
    
    receiver = User.query.filter_by(id = user_id).first()
    sender = User.query.filter_by(id = cc_req.sender_id).first()

    # Creates a new Busy Time if doesnt exist, otherwise queries the busy time object
    if Busy_Time.query.filter_by(month = cc_req.month, day = cc_req.day, year = cc_req.year, 
                                         weekday = cc_req.weekday, start_time = cc_req.start_time).first() is None:
        new_bt = Busy_Time(month = cc_req.month, day = cc_req.day, year = cc_req.year, 
                                   weekday = cc_req.weekday, start_time = cc_req.start_time)    
        db.session.add(new_bt)
    else:
        new_bt = Busy_Time.query.filter_by(month = cc_req.month, day = cc_req.day, year = cc_req.year, 
                                           weekday = cc_req.weekday, start_time = cc_req.start_time).first()   
            
    new_ft = Free_Time.query.filter_by(month = cc_req.month, day = cc_req.day, year = cc_req.year, 
                                               weekday = cc_req.weekday, start_time = cc_req.start_time).first()  
    if cc_req.accepted is None:
        if accepted_response:
            # Checks if the both users have the free time object and dont have the busy time object
            if new_ft in receiver.free_times and new_bt not in receiver.busy_times:                    
                receiver.busy_times.append(new_bt)
                receiver.free_times.remove(new_ft)
                cc_req.accepted = True
            else:
                return failure_response("Sender or receiver already busy", 400)
        elif not accepted_response:
            sender.busy_times.remove(new_bt)
            cc_req.accepted = False
            db.session.delete(cc_req)
    else:
        return failure_response("Request already satisfied", 400)
    
    db.session.commit()
    return success_response(cc_req.serialize(), 201)

# Route : Delete coffee chat request
@app.route("/api/cr/<int:cr_id>/", methods = ["DELETE"])
def delete_chat_request(cr_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    chat_req = Chat_Request.query.filter_by(id = cr_id).first()
    if chat_req is None:
        return failure_response("Coffee Chat Request not found", 404)
    if chat_req.accepted is not None: 
        return failure_response("Request cannot be deleted after its been accepted or denied", 400)
    db.session.delete(chat_req)
    db.session.commit()
    return success_response(chat_req.serialize(), 200)

# -------------------------------- Organization Request Routes --------------------------------

# Route : Get all incoming requests to join organization from users
@app.route("/api/or/<int:org_id>/", methods = ["GET"])
def get_org_or(org_id):
    return success_response({"received organization requests": [org.serialize() for org in Org_Request.query.filter_by(org_id = org_id)]})

# Route : Add a org request to user
@app.route("/api/or/<int:sender_id>/", methods = ["POST"])
def add_og_to_user(sender_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    rec_id = body.get("organization id")
    new_position = body.get("position")
    if None in (rec_id, new_position):
        return failure_response("One or more fields not supplied", 400)
    
    current_org = Organization.query.filter_by(id = rec_id).first()
    if current_org is None:
        return failure_response("Organization not found", 404)
    
    new_or = Org_Request(user_id = sender_id, org_id = rec_id, position = new_position)        

    db.session.add(new_or)
    db.session.commit()
    
    dictionary = {}
    dictionary.update(current_org.simple_serialize())
    dictionary.update({"organization requests": [org.serialize() for org in Org_Request.query.filter_by(user_id = sender_id)]})
        
    return success_response(dictionary)

# Route : Delete an org request
@app.route("/api/or/<int:og_id>/", methods = ["DELETE"])
def delete_og(og_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    org_req = Org_Request.query.filter_by(id = og_id).first()
    if org_req is None:
        return failure_response("Organization Request not found", 404)
    db.session.delete(org_req)
    db.session.commit()
    return success_response(org_req.serialize(), 200)

# Route : Accept or deny user request to join organization 
@app.route("/api/or/requests/<int:req_id>/", methods = ["POST"])
def accept_org_request(req_id):
    # Authentication
    success, response = extract_token(request)
    if not success: 
        return response
    session_token = response 
    org = orgs_dao.get_org_by_session_token(session_token)
    if not org or not org.verify_session_token(session_token): 
        return failure_response("Invalid session token", 400) 
    
    body = json.loads(request.data)
    accepted_response = body.get("accepted")
    org_req = Org_Request.query.filter_by(id = req_id).first()
    if org_req is None:
        return failure_response("Organization Request not found", 404)
                                
    user_id = org_req.user_id
    org_id = org_req.org_id
    current_user = User.query.filter_by(id = user_id).first()
    org = Organization.query.filter_by(id = org_id).first()
    new_position = Position(position = org_req.position)

    if accepted_response is None or current_user is None or org is None: 
        return failure_response("Request not found", 404)
        
    if accepted_response: 
        org_req.accepted = True
        association = User_Org(user = current_user, organization = org, position = new_position)
        db.session.delete(org_req)
        db.session.add(association)      
        db.session.commit()
    elif not accepted_response: 
        org_req.accepted = False
        db.session.commit()
    else:
        return failure_response("Org Request already satisfied", 400)
        
    return success_response(org_req.serialize())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)