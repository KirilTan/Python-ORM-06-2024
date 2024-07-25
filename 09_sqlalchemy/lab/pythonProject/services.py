from main import Session
from models import User, Order

with Session() as session:
    session.add_all(
        (
            Order(user_id=7), Order(user_id=9)
        )
    )
    session.commit()
