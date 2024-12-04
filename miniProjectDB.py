import mysql.connector


class ShoppingCart:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="root",  
            database="ShoppingCartDB"
        )
        self.cursor = self.connection.cursor()
        self.totalCost = 0
        self.deliveryFee = 0

    def purchase(self):
        while True:
            try:
                purchaseNumber = int(input("What do you wanna purchase: "))
                self.cursor.execute("SELECT * FROM Products WHERE sr_no = %s", (purchaseNumber,))
                product = self.cursor.fetchone()

                if not product:
                    print("Invalid")
                    continue

                purchaseCount = int(input(f"How many {product[1]} packages do you want to purchase? "))

                if purchaseCount <= 0:
                    print("Invalid")
                elif purchaseCount > product[2]:
                    print(f"Available quantity of {product[1]} is {product[2]}.")
                else:
                    itemCost = purchaseCount * product[3]
                    self.totalCost += itemCost

                    self.cursor.execute("""
                        INSERT INTO CustomerCart (item_id, item_name, qty, total_cost)
                        VALUES (%s, %s, %s, %s)
                    """, (product[0], product[1], purchaseCount, itemCost))
                    self.connection.commit()

                    self.cursor.execute("""
                        UPDATE Products SET quantity = quantity - %s WHERE sr_no = %s
                    """, (purchaseCount, product[0]))
                    self.connection.commit()

            except ValueError:
                print("Invalid input. Please enter valid numbers.")
                continue

            continueShopping = input("Would you like to continue shopping (Y/N)? ").strip().lower()
            if continueShopping == "n":
                self.cusDetails()
                self.calBill()
                self.calStore()
                break

    def calBill(self):
        print("\n" + "-" * 50 + " Bill " + "-" * 50)
        print("S.no | Item      | Qty  | Total Cost")
        self.cursor.execute("SELECT * FROM CustomerCart")
        items = self.cursor.fetchall()
        for item in items:
            print(f"{item[0]}    | {item[2]} | {item[3]}   | {item[4]}")
        print(f"Total items cost: {self.totalCost} Rs")
        print(f"Delivery Fee: {self.deliveryFee} Rs")
        print(f"Total Bill Amount: {self.totalCost + self.deliveryFee} Rs")
        print("-" * 100)

    def calStore(self):
        print("\n" + "-" * 50 + " Remaining Quantity in Store " + "-" * 50)
        print("S.no | Item      | Quantity | Cost/Item")
        self.cursor.execute("SELECT * FROM Products")
        products = self.cursor.fetchall()
        for product in products:
            print(f"{product[0]}    | {product[1]} | {product[2]}       | {product[3]}")

    def cusDetails(self):
        name = input("Enter your name: ")
        address = input("Enter your address: ")
        try:
            distance = int(input("Enter the distance from the store (e.g., 5/10/15/30): "))
            if distance < 15:
                self.deliveryFee = 50
                print("Delivery Fee: 50 Rs for distance less than 15 km.")
            elif 15 <= distance < 30:
                self.deliveryFee = 100
                print("Delivery Fee: 100 Rs for distance between 15 and 30 km.")
            else:
                print("No delivery available for distances above 30 km.")
                self.deliveryFee = 0
                return
            self.cursor.execute("""
                INSERT INTO CustomerDetails (name, address, distance, delivery_fee)
                VALUES (%s, %s, %s, %s)
            """, (name, address, distance, self.deliveryFee))
            self.connection.commit()

        except ValueError:
            print("Invalid distance. Please enter a number.")


if __name__ == "__main__":
    Walmart = ShoppingCart()
    Walmart.purchase()
