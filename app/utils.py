import re
import requests

from flask import url_for, flash, current_app
from datetime import timedelta
from pytimeparse.timeparse import timeparse


def register_template_utils(app):
    """Register Jinja 2 helpers (called from __init__.py)."""

    @app.template_test()
    def equalto(value, other):
        return value == other

    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)

    app.add_template_global(index_for_role)


def index_for_role(role):
    return url_for(role.index)


def parse_phone_number(phone_number):
    """Make phone number conform to E.164 (https://en.wikipedia.org/wiki/E.164)
    """
    stripped = re.sub(r'\D', '', phone_number)
    if len(stripped) == 10:
        stripped = '1' + stripped
    stripped = '+' + stripped
    return stripped


def minutes_to_timedelta(minutes):
    """Use when creating new report."""
    return timedelta(minutes=minutes)


def parse_timedelta(duration):
    """Parse string into timedelta object"""
    seconds = timeparse(duration)
    return timedelta(seconds=seconds)


def flash_errors(form):
    """Show a list of all errors in form after trying to submit."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error: %s - %s" % (
                getattr(form, field).label.text, error),
                'form-error')


def strip_non_alphanumeric_chars(input_string):
    """Strip all non-alphanumeric characters from the input."""
    stripped = re.sub('[\W_]+', '', input_string)
    return stripped


# Viewport-biased geocoding using Google API
# Returns a tuple of (latitude, longitude), (None, None) if geocoding fails
def geocode(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'bounds': current_app.config['VIEWPORT']}
    r = requests.get(url, params=payload)
    if r.json()['status'] is 'ZERO_RESULTS' or len(r.json()['results']) is 0:
        return None, None
    else:
        coords = r.json()['results'][0]['geometry']['location']
        return coords['lat'], coords['lng']
