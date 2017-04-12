# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_script import Manager
from datetime import datetime
from InputToArray import input_to_array
from Utils import *
from FirstStep import *


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
    control_points = None
    end_points = None
    if point_form.validate_on_submit():
        tmp1 = point_form.control_points.data
        tmp2 = point_form.end_points.data
        control_points = input_to_array(tmp1)
        end_points = input_to_array(tmp2)
        if not control_points or not end_points:
            point_form.control_points.data = ''
            point_form.end_points.data = ''
        else:
            init_plain(
                end_points[0], end_points[1], 1.0,
                "init_plain.dat", 'mdbFile', 'odbJob', point_list=control_points[:],
                abaqus_file_save_path='./AbaqusFiles'
            )
    return render_template(
        'index.html', point_form=point_form,
        control_points=control_points,
        end_points=end_points,
        current_time=datetime.utcnow()
    )


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1> 404 Error </h1>"


if __name__ == '__main__':
    import os
    os.chdir('..')
    manager.run()
