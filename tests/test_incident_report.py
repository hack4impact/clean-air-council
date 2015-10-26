import unittest
import datetime
from app import create_app, db
from app.models import IncidentReport, Location, Agency


class IncidentReportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_location_no_incident(self):
        loc = Location(
            latitude='39.951039',
            longitude='-75.197428',
            original_user_text='3700 Spruce St.'
        )
        self.assertTrue(loc.latitude == '39.951039')
        self.assertTrue(loc.longitude == '-75.197428')
        self.assertTrue(loc.original_user_text == '3700 Spruce St.')
        self.assertTrue(loc.incident_report is None)

    def test_location_has_incident(self):
        incident_report_1 = IncidentReport()
        incident_report_2 = IncidentReport()
        loc = Location(
            latitude='39.951039',
            longitude='-75.197428',
            original_user_text='3700 Spruce St.',
            incident_report=incident_report_1
        )
        self.assertEqual(loc.incident_report, incident_report_1)
        loc.incident_report = incident_report_2
        self.assertEqual(loc.incident_report, incident_report_2)

    def test_incident_report_no_location_no_agency(self):
        now = datetime.datetime.now()
        incident = IncidentReport(
            vehicle_id='123456',
            license_plate='ABC123',
            date=now,
            duration=datetime.timedelta(minutes=5),
            picture_url='http://google.com',
            description='Truck idling on the road!'
        )
        self.assertEqual(incident.vehicle_id, '123456')
        self.assertEqual(incident.license_plate, 'ABC123')
        self.assertEqual(incident.date, now)
        self.assertEqual(incident.duration, datetime.timedelta(minutes=5))
        self.assertEqual(incident.picture_url, 'http://google.com')
        self.assertEqual(incident.description, 'Truck idling on the road!')

    def test_incident_report_with_location_no_agency(self):
        loc1 = Location(
            latitude='-75.197428',
            longitude='39.951039',
            original_user_text='3700 Spruce St.'
        )
        loc2 = Location(
            latitude='',
            longitude='-75.197428',
            original_user_text='3800 Spruce St.'
        )
        incident = IncidentReport(
            vehicle_id='123456',
            license_plate='ABC123',
            date=datetime.datetime.now(),
            duration=datetime.timedelta(minutes=5),
            picture_url='http://google.com',
            description='Truck idling on the road!',
            location=loc1
        )
        self.assertEqual(incident.location, loc1)
        incident.location = loc2
        self.assertEqual(incident.location, loc2)

    def test_incident_report_with_agency_no_location(self):
        agency1 = Agency(name='SEPTA')
        agency2 = Agency(name='PECO')

        incident = IncidentReport(
            vehicle_id='123456',
            license_plate='ABC123',
            date=datetime.datetime.now(),
            duration=datetime.timedelta(minutes=5),
            picture_url='http://google.com',
            description='Truck idling on the road!',
            agency=agency1
        )
        self.assertEqual(incident.agency, agency1)
        incident.agency = agency2
        self.assertEqual(incident.agency, agency2)