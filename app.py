import statistics
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

import api_calls as api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artists_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(200))
    popularity = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Artist {self.id}>'
    

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.String(100), nullable=False)
    popularity = db.Column(db.Integer)
    played_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Song self.id>'


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # I need to change this. I dont want to get a new access token everytime
        # I make a request. It should update every 55 minutes.
        artist_id = request.form['artist_id']
        # duplicate = db.session.query(Artist.artist_id).filter(Artist.artist_id==artist_id).count() is not None
        
        # if duplicate:
        #     return redirect('/')

        access_token = api.authenticate()
        artist_info = api.get_artist(artist_id, access_token=access_token)
        artist_name = artist_info['name']
        # Artist Genre comes back as a list. We need to convert it.
        artist_genres = ', '.join(artist_info['genres'])
        artist_popularity = artist_info['popularity']

        new_artist = Artist(name=artist_name, genres=artist_genres, artist_id=artist_id, popularity=artist_popularity)

        try:
            db.session.add(new_artist)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding the artist.'

    else:
        artists = Artist.query.order_by(Artist.date_added).all()
        artists_avg_pop = Artist.query.with_entities(func.avg(Artist.popularity)).all()
        return render_template('index.html', artists=artists, avg_pop=artists_avg_pop)

@app.route('/delete/<int:id>')
def delete(id):
    artist_to_delete = Artist.query.get_or_404(id)

    try:
        db.session.delete(artist_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that artist.'

if __name__ == "__main__":
    app.run(debug=True)