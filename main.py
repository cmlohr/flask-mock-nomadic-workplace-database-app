from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXSECRET_KEYXXX'
Bootstrap(app)


class CafeForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    location = StringField("Location on Google Maps (URL)",
                           validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8:00AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 7:00PM", validators=[DataRequired()])
    amenities_rating = SelectField("Amenities Rating", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
                                   validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Rating", choices=["❌", "💡", "💡💡", "💡💡💡", "💡💡💡💡", "💡💡💡💡💡"],
                              validators=[DataRequired()])
    power_rating = SelectField("Power Rating", choices=["❌", "⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡⚡⚡⚡"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("locations.csv", mode="a") as csv_file:
            csv_file.write(f"\n{form.name.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.amenities_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('locations.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
