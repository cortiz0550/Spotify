from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import api_calls as api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artists_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.String(100))
    genres = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Artist {self.id}>'


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # I need to change this. I dont want to get a new access token everytime
        # I make a request. It should update every 55 minutes.
        access_token = api.authenticate()
        artist_id = request.form['artist_id']
        artist_info = api.get_artist(artist_id, access_token=access_token)
        artist_name = artist_info['name']
        # Artist Genre comes back as a list. We need to convert it.
        artist_genres = ', '.join(artist_info['genres'])

        new_artist = Artist(name=artist_name, genres=artist_genres)

        try:
            db.session.add(new_artist)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding the artist.'

    else:
        artists = Artist.query.order_by(Artist.date_added).all()
        return render_template('index.html', artists=artists)

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