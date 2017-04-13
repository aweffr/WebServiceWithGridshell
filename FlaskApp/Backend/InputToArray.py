# -*- coding:utf-8 -*-
from flask import session


def input_to_array(s):
    out = []
    try:
        points = s.split()
        for p in points:
            tmp = p.strip().strip("()").split(",")
            out.append(map(float, tmp))
        return out
    except Exception as e:
        print e


def parse_control_points(s):
    out = []
    try:
        points = s.split()
        for p in points:
            tmp = p.strip().strip("()").split(",")
            if len(tmp) != 2:
                raise Exception
            else:
                out.append(map(float, tmp))
    except Exception as e:
        print e
        raise Exception
    return out


def parse_end_points(s):
    s = s.strip().strip("()").split(",")
    if len(s) != 2:
        raise Exception
    return map(float, s)
