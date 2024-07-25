from main import Session
from models import User


with Session() as session:
    # Create new users
    user1 = User(
        username='john_doe',
        email='john.doe@example.com'
    )

    user2 = User(
        username='sarah_smith',
        email='sarah.smith@gmail.com'
    )

    user3 = User(
        username='mike_jones',
        email='mike.jones@company.com'
    )

    user4 = User(
        username='emma_wilson',
        email='emma.wilson@domain.net'
    )

    user5 = User(
        username='david_brown',
        email='david.brown@email.org'
    )

    # Add users using add_all() method
    session.add_all([user1, user2, user3, user4, user5])

    # Commit changes
    session.commit()

    # Retrieve all users using all() method
    all_users = session.query(User).all()

    for user in all_users:
        print(f'User: {user.username}, Email: {user.email}')
