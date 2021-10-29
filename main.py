from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from functions import get_music, spotify, return_final_score, attributes

class GetMusic(FlaskForm):
    autocomplete = StringField('Search for Music', validators=[DataRequired()])
    autocompletemusic = StringField('Search for Music', validators=[DataRequired()])
    submit = SubmitField("Search")

# INITIATING
app = Flask(__name__)
# app.config['SECRET_KEY'] = Key
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = GetMusic()
    return render_template("index.html", form=form)


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    if request.method == "GET":
        search = request.args.get('q')
        tracks = spotify.search_music(search)
        results = [tracks[track]['track'] for track in tracks]
        id = [tracks[track]['id'] for track in tracks]
        return jsonify(matching_results=results)

@app.route('/results', methods=['GET', 'POST'])
def results():
    form = GetMusic()
    try:
        music1 = get_music(form.autocomplete.data)
        music2 = get_music(form.autocompletemusic.data)
        final = int(return_final_score(music1, music2)[0])
        attributes_score = return_final_score(music1, music2)[1]
    except:
        flash("There was a problem with your music. May you try another one?")
        form = GetMusic()
        return render_template('index.html', form=form)
    else:
        return render_template("comparison.html", music1=music1, music2=music2, final=final, attributes=attributes, attributes_score=attributes_score)

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)