from models import User
from main import Session


with Session() as session:
    new_user = User(
        username='john_doe',
        email='john.doe@example.com'
    )

    session.add(new_user)
    session.commit()