from enum import Enum
from typing import Dict

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

class Operation(Enum):
    ADD = "add"
    REMOVE = "remove"

# TODO try to move enum classes inside the Order class
class Order:
    def __init__(self, order: OrderType, price: float, quantity: int, type: Operation = Operation.ADD):
        self.id = None
        self.order = order
        self.type = type
        self.price = price
        self.quantity = quantity

    def mark_removed(self):    
        self.type = Operation.REMOVE

    def unit_price(self):
        return self.price / self.quantity
    
    # TODO call order in order
    def is_better(self, other: Order):
        if self.type == OrderType.BUY:
            return self.unit_price() > other.unit_price()
        else:
            return self.unit_price() < other.unit_price()

    def __repr__(self):
        return f"Order({self.id}, {self.order.name}, {self.type.name}, Price: {self.price}, Quantity: {self.quantity})"


class Trade:
    # Track best orders
    best_buy: Order = None
    best_sell: Order = None
    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self.order_id_counter: int = 1
        self.buy_orders = []
        self.sell_orders = []

# TODO try to avoid sorting in add
    def add(self, order_type: OrderType, price: float, quantity: int):
        order = Order(order_type, price, quantity)
        order.id = self.order_id_counter
        self.order_id_counter += 1

        self.orders[order.id] = order

        if order_type == OrderType.BUY:
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda o: o.unit_price())
            best_buy = self.best_price_buy()
            print(f"\nAfter adding Buy Order ID {order.id}:")
            print("Best Buy Price Order:", best_buy)
        
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda o: -o.unit_price())
            best_sell = self.best_price_sell()
            print(f"\nAfter adding Sell Order ID {order.id}:")
            print("Best Sell Price Order:", best_sell)

    # TODO move sorting in remove
    def remove_order(self, order_id: int):
        if order_id in self.orders:
            self.orders[order_id].mark_removed()
            print(f"Order ID {order_id} marked as removed.")
        else:
            print(f"Order ID {order_id} does not exist.")
        self.clean_orders()

    def best_price_buy(self):
        if self.buy_orders:
            return self.buy_orders[0].unit_price(), self.buy_orders[0]
        return None

    def best_price_sell(self):
        if self.sell_orders:
            return self.sell_orders[0].unit_price(), self.sell_orders[0]
        return None

    def clean_orders(self):
        self.buy_orders = [order for order in self.buy_orders if order.type != Operation.REMOVE]
        self.sell_orders = [order for order in self.sell_orders if order.type != Operation.REMOVE]
    
    def __repr__(self):
        return f"Trade(Orders: {self.orders})"


def main():
    trade = Trade()
    trade.add(OrderType.BUY, 20.00, 100)
    trade.add(OrderType.SELL, 25.00, 200)
    trade.add(OrderType.BUY, 23.00, 50)
    trade.add(OrderType.BUY, 23.00, 700)
    trade.remove_order(3)
    trade.add(OrderType.SELL, 28.00, 100)

    while True:
        print("\nOptions:")
        print("1. Add Order")
        print("2. Remove Order")
        print("3. Show Orders")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            # Adding an order
            order_type_input = input("Enter Order Type (buy/sell): ").strip().lower()
            if order_type_input not in ["buy", "sell"]:
                print("Invalid Order Type. Please enter 'buy' or 'sell'.")
                continue
            
            try:
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))
            except ValueError:
                print("Invalid input for price or quantity. Please enter valid numbers.")
                continue

            order_type = OrderType.BUY if order_type_input == "buy" else OrderType.SELL
            trade.add(order_type, price, quantity)
        
        elif choice == "2":
            # Removing an order
            try:
                order_id = int(input("Enter Order ID to remove: "))
                trade.remove_order(order_id)
            except ValueError:
                print("Invalid input. Please enter a valid Order ID.")
        
        elif choice == "3":
            # Show all orders
            print("Current Orders:")
            for order_id, order in trade.orders.items():
                print(order)
        
        elif choice == "4":
            # Exit
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please select a valid number.")


if __name__ == "__main__":
    main()