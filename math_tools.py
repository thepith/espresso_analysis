#!/usr/bin/env python3
"""Mathematical Tools"""


def is_int(value, **kwargs):
    """Checks if the value is (nearly) an integer number"""
    from math import isclose
    return isclose(value, round(value), **kwargs)
