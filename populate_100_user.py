from generate_fake_data import get_faker_json_data
from models import User, db


# def create_data():
fake_data = get_faker_json_data(100)

for fake_obj in fake_data:
    user = User(
            name=fake_obj["first_name"], 
            email=fake_obj["email"], 
            password=fake_obj["password"], 
            mobile_number=fake_obj["phone_number"]
        )
    db.session.add(user)

db.session.commit()

print('>>>>>> data seeded >>>>>>>>>>>>>>>')