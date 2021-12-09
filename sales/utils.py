from os import curdir
import uuid
from customers.models import Customer
from profiles.models import Profile

def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_customer_from_id(value):
    customer = Customer.objects.get(id=value)
    return customer

def get_salesman_from_id(value):
    profile = Profile.objects.get(id=value)
    return profile.user.username