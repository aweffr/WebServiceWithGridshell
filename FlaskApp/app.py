# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, url_for, redirect, request, flash
from test_utils import mock_computing
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_script import Manager
from datetime import datetime
from InputToArray import input_to_array, parse_control_points, parse_end_points


class PointForm(FlaskForm):
    control_points = TextAreaField(
        u'初始控制点',
        validators=[DataRequired(), Length(min=2)]
    )
    end_points = StringField(
        u'首尾边界',
        validators=[DataRequired(), Length(min=2)]
    )
    submit = SubmitField(u'提交')


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = "good_good_study_day_day_up"
manager = Manager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    point_form = PointForm()
    if point_form.validate_on_submit():
        print request.form
        tmp1 = point_form.control_points.data
        tmp2 = point_form.end_points.data
        try:
            session['control_points'] = parse_control_points(tmp1)
            session['end_points'] = parse_end_points(tmp2)
            return redirect(url_for('index'))
        except Exception as e:
            flash("Wrong Data Format!")
            point_form.control_points.data = ''
            point_form.end_points.data = ''
    return render_template(
        'index.html', point_form=point_form,
        control_points=session.get('control_points'),
        end_points=session.get('end_points'),
        current_time=datetime.utcnow()
    )


@app.route('/confirm')
def confirm():
    url_result_png = url_for("static", filename="initial_plain.png")
    return render_template(
        'preview.html',
        inital_png_url=url_result_png,
        control_points=session.get('control_points'),
        end_points=session.get('end_points'),
        current_time=datetime.utcnow()
    )


@app.route('/result')
def result():
    mock_computing()
    if session['compute_complete']:
        url_result_png = url_for("static", filename="displacement.png")
        return render_template(
            "result.html",
            url_result_png=url_result_png
        )
    else:
        flash("Computing! Please wait.")
        return redirect(url_for('confirm'))


@app.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('index'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/computing_status')
def computing_status():
    if 'compute_complete' in session and session['compute_complete']:
        return 'True'
    else:
        return 'False'


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    import os

    os.chdir('..')
    manager.run()
