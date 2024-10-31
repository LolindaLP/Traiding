from typing import Dict

class Order:
    from enum import Enum

    class OrderType(Enum):
        BUY = "buy"
        SELL = "sell"

    class Operation(Enum):
        ADD = "add"
        REMOVE = "remove"

    def __init__(self, order: 'Order.OrderType', 
                 price: float, quantity: int, type: 'Order.Operation' = Operation.ADD):
        self.id = None
        self.order = order
        self.type = type
        self.price = price
        self.quantity = quantity

    def mark_removed(self):    
        self.type = Order.Operation.REMOVE

    def unit_price(self):
        return round(self.price / self.quantity, 3)
    
    def is_better(self, other):
        
        if self.type == Order.OrderType.BUY:
            return self.unit_price() > other.unit_price()
        else:
            return self.unit_price() < other.unit_price()

    def __repr__(self):
        return f"Order({self.id}, {self.order.name}, {self.type.name}, Price: {self.price}, Quantity: {self.quantity})"


class Trade:
    def __init__(self):
        self.best_buy: 'Order' = None
        self.best_sell: 'Order' = None
        self.orders: Dict[int, Order] = {}
        self.order_id_counter: int = 1
        self.buy_orders = []
        self.sell_orders = []

    def add(self, order_type: Order.OrderType, price: float, quantity: int):
        order = Order(order_type, price, quantity)
        order.id = self.order_id_counter
        self.order_id_counter += 1
        self.orders[order.id] = order

        if order_type == Order.OrderType.BUY:
            for i in range(len(self.buy_orders)):
                if self.buy_orders[i].is_better(order):
                    self.buy_orders.insert(i, order)
                    break
            else:
                self.buy_orders.append(order)
            self.best_buy = self.buy_orders[-1]
            print(f"\nAfter adding Buy Order ID {order.id}:")
            print("Best Buy Price Order:", self.best_buy, "Price:", self.best_buy.unit_price())
        else:
            for i in range(len(self.sell_orders)):
                if self.sell_orders[i].is_better(order):
                    self.sell_orders.insert(i, order)
                    break
            else:
                self.sell_orders.append(order)
            self.best_sell = self.sell_orders[0]
            print(f"\nAfter adding Sell Order ID {order.id}:")
            print("Best Sell Price Order:", self.best_sell, "Price:", self.best_sell.unit_price())

    def remove_order(self, order_id: int):
        if order_id in self.orders:
            self.orders[order_id].mark_removed()
            print(f"Order ID {order_id} marked as removed.")
        else:
            print(f"Order ID {order_id} does not exist.")

    def __repr__(self):
        return f"Trade(Orders: {self.orders})"


def main():
    trade = Trade()
    trade.add(Order.OrderType.BUY, 20.00, 100)
    trade.add(Order.OrderType.SELL, 25.00, 200)
    trade.add(Order.OrderType.BUY, 23.00, 50)
    trade.add(Order.OrderType.BUY, 23.00, 700)
    trade.remove_order(3)
    trade.add(Order.OrderType.SELL, 28.00, 100)

    while True:
        print("\nOptions:")
        print("1. Add Order")
        print("2. Remove Order")
        print("3. Show Orders")
        print("4. Exit")

        choice = input("Select an option: ")

        match choice:
            case "1":
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

                order_type = Order.OrderType.BUY if order_type_input == "buy" else Order.OrderType.SELL
                trade.add(order_type, price, quantity)

            case "2":
                # Removing an order
                try:
                    order_id = int(input("Enter Order ID to remove: "))
                    trade.remove_order(order_id)
                except ValueError:
                    print("Invalid input. Please enter a valid Order ID.")

            case "3":
                # Show all orders
                print("Current Orders:")
                for order_id, order in trade.orders.items():
                    print(order)

            case "4":
                # Exit
                print("Exiting the program.")
                return  # Use return to exit from main

            case _:
                print("Invalid option. Please select a valid number.")


if __name__ == "__main__":
    main()