from models import User
from main import Session


with Session() as session:
    user_to_delete = session.query(User).filter_by(username='john_doe').first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"User '{user_to_delete.username}' deleted successfully.")
    else:
        print('User not found.')
