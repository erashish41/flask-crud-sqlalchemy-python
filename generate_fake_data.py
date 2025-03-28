from ctypes.wintypes import HWND
from faker import Faker
fake = Faker()

def get_faker_json_data(data):
    json_faker_data = []
    for x in range(data):
        json_faker_data.append(
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email" : fake.email(),
                "password": fake.password(),
                "phone_number": fake.phone_number()
            }
            
        )

    return json_faker_data


