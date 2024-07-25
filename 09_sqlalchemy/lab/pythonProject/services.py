from main import Session
from models import User, Order

with Session() as session:
    orders = session.query(Order).order_by(Order.user_id.desc()).all()

    if not orders:
        print("No orders found.")
    else:
        for i, order in enumerate(orders):
            user = order.user
            print(
                f'Order number {order.id}\n'
                f'Is completed: {order.is_completed}\n'
                f'Username: {user.username}'
            )
            if i < len(orders) - 1:
                print()