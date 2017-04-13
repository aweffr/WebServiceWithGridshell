import time
from flask import session


def mock_computing():
    if 't1' not in session:
        session['t1'] = time.clock()
    if time.clock() - session['t1'] < 5:
        session['compute_complete'] = False
    else:
        session['compute_complete'] = True