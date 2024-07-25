from models import User
from main import Session


with Session() as session:
    user_to_update = session.query(User).filter_by(username='john_doe').first()

    if user_to_update:
        user_to_update.email = 'new_email@example.com'
        session.commit()
        print('User email updated successfully.')
    else:
        print('User not found.')