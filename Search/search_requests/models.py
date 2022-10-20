import datetime

from mongoengine import Document, fields


class SearchRequest(Document):
    name = fields.StringField(max_length=50)
    address = fields.StringField(max_length=100)
    has_parking = fields.BooleanField()
    has_wifi = fields.BooleanField()
    has_washing_machine = fields.BooleanField()
    has_kitchen = fields.BooleanField()
    price_min = fields.DecimalField(min_value=0, max_value=1000, precision=2)
    price_max = fields.DecimalField(min_value=0, max_value=1000)
    beds_number = fields.IntField(min_value=0, max_value=10)
    owner = fields.IntField(min_value=0)
    city = fields.IntField(min_value=0)
    order = fields.StringField()
    booking_start_date = fields.DateTimeField()
    booking_end_date = fields.DateTimeField()

    created_at = fields.DateTimeField(default=datetime.datetime.now)
    user = fields.IntField(min_value=0)

    meta = {'collection': 'search_requests'}
