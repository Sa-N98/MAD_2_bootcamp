from flask import Flask, request, render_template as rt , redirect , url_for
from model import * 
import os
from api import *
from celery_worker import make_celery
from celery.result import AsyncResult
from celery.schedules import crontab

from flask_security import Security, SQLAlchemyUserDatastore, login_required, login_user, logout_user
from flask_security.utils import hash_password, verify_password
from flask_jwt_extended import JWTManager, create_access_token


from Email import send_email


from flask_restful import Api


current_dir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ os.path.join(current_dir,"mad-1.sqlite3")
app.config['SECRET_KEY'] = 'superseccret'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['JWT_SECRET_KEY'] = 'AKASMNGAKWGK.MWELVNQEWBHJQWVNJKQW'
app.config.update(
    CELERY_BROKER_URL = 'redis://localhost:6379',
    result_backend = 'redis://localhost:6379'
)


db.init_app(app)
jwt= JWTManager(app)
app.app_context().push()

celery = make_celery(app)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

api = Api(app)
api.add_resource(search, '/api/search/<tags>/<search_query>')

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user_data = User.query.filter(User.email == email).first()
        print(user_data.username, user_data.email, user_data.password)
        print()
        if user_data:
            if verify_password(password , user_data.password):
                login_user(user_data)
                token = create_access_token(identity=user_data.email)
                user_data.API_token = token
                db.session.commit()
                
                if user_data.user_type == 'consumers':
                    return redirect(url_for('user_dashbord'))

                if user_data.user_type == 'artist':
                    print('hit')
                    return redirect(url_for('artist_dashbord'))
            return rt('home.html', massage= "Wrong email or password")
    return rt('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':

        if request.form['type'] == 'artist':
            if not User.query.filter(User.email == request.form['email']).all():
                # newUser = users(username = request.form['username'], email = request.form['email'] , password = request.form['password'], user_type = request.form['type']) 
                # db.session.add(newUser)
                # db.session.commit()

                user_datastore.create_user(
                                            username = request.form['username'], 
                                            email = request.form['email'] , 
                                            password = hash_password(request.form['password']),
                                            user_type = request.form['type']
                )
                
                db.session.commit()        


        if request.form['type'] == 'consumers':
            if not User.query.filter(User.email == request.form['email']).all():
                user_datastore.create_user(
                                            username = request.form['username'], 
                                            email = request.form['email'] , 
                                            password = hash_password(request.form['password']),
                                            user_type = request.form['type']
                )
                
                db.session.commit()      
            
    return rt('signup.html')


@app.route('/user_dashbord', methods=['GET'])
@login_required
def user_dashbord():
    return rt('userDashbord.html')


@app.route('/search_query', methods=['GET', 'POST'])
def search_query():
    if request.method == 'POST':
        search_tag = request.form['search_tag']
        query = request.form['search_query']
        if search_tag == 'Song':
            data = songs.query.filter(songs.name.like('%'+query+'%')).all()
            return rt('results.html', search_data = data)
        elif search_tag == 'Artist':
            data = songs.query.filter(songs.artist.like('%'+query+'%')).all()
            return rt('results.html', search_data = data)
        elif search_tag == 'Album':
            data = songs.query.filter(songs.album.like('%'+query+'%')).all()
            return rt('results.html', search_data = data)
    return 'search'





@app.route('/artist_dashbord', methods=['GET'])
@login_required
def artist_dashbord():
    return rt("artistDashbort.html")




import time 
from datetime import timedelta

@celery.task
def daily_remiender():
    lis_usr = User.query.filter(User.user_type == 'consumers').all()
    for usr in lis_usr:
        massage = rt('email.html', user_name= usr.username)
        send_email(to_address=usr.email, subject= "Website remiender", message=massage)


celery.conf.beat_schedule = {

'app_daily_remiender': {
    'task': 'main.daily_remiender',
    'schedule': timedelta(seconds= 30)
}
                            
                            }










@app.route('/test', methods=['GET', 'POST'])
def test():
    test = User.query.filter(User.id == 1).first()
    for i in test.myPlaylist:
        print(i.playlistName)

        for j in i.songList:
            print(j)
            song=songs.query.filter(songs.id == j).first()
            print(song.name)
    return "hit"

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')


