import re, datetime
from flask import url_for
from app.models import IncidentReport, Location


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


def parse_to_db(db, filename):
    import csv, geocoder
    city_default = ', philadelphia, pennsylvania, usa'
    vehicle_id_index = 8
    license_plate_index = 9
    location_index = 4
    date_index = 0
    agency_index = 6
    picture_index = 13
    description_index = 11
    with open(filename, 'rb') as file:
        reader = csv.reader(file, delimiter=',')
        columns = reader.next()
        for row in reader:
            print row
            address_text = row[location_index]
            # TODO: error handling for geocoder
            coordinates = geocoder.arcgis(address_text + city_default).latlng
            loc = Location(
                latitude=coordinates[0],
                longitude=coordinates[1],
                original_user_text=address_text)
            db.session.add(loc)
            date_format = "%m/%d/%Y %H:%M"
            incident = IncidentReport(
                vehicle_id=row[vehicle_id_index],
                license_plate=row[license_plate_index],
                location=loc,
                date=datetime.datetime.strptime(row[date_index], date_format),
                # TODO: calculate duration interval from timestamps
                duration=0,
                picture_url=row[picture_index],
                description=row[description_index])
            db.session.add(incident)
        db.session.commit()
        return columns
