from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' # Can be whatever for us, for now; this is what 'seeds' the CSRF protection
app.debug=True

API_KEY = 'f37d2a49b946d808bffe304d318c2ab'

class = weatherForm(FlaskForm):
    zip_code = IntegerField("Enter a US zipcode", validators=[Required()])
    submit = SubmitField("Submit")

    def validate_zipcode(self, field):
        if len(str(field.data)) != 5:
            raise ValidationError('Please enter a 5 digit zipcode')

@app.route('/zipcode', methods=["GET","POST"])
def zip_form():
    form = weatherForm()
    if form.validate_on_submit():
        zipcode = str(form.zipcode.data)
        params = {}
        params['zip'] = zipcode + ",us"
        params['appid'] = 'f37d2a49b946d808bffe304d318c2ab'
        baseurl = 'http://api.openweathermap.org/data/2.5/weather?'
        resp = requests.get(baseurl, params=params)
        resp_dict = json.loads(resp.text)
        print(resp_dict)

        description = resp_dict['weather'][0]['description']
        city = resp_dict['name']
        temperature_kelvin = resp_dict['main']['temp']

        return render_template('results.html', city=city, description=description, temperature=temperature_kelvin)
    flash(form.errors)
    return render_template('weather_form.html'), form = form

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)