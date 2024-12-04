class ShoppingCart: 
    def __init__(self):
        self.cart = [
            {"sr.no": 1, "Item": "Biscuits", "Quantity": 5, "Cost/Item":20.5},
            {"sr.no": 2, "Item": "Cereals", "Quantity": 10, "Cost/Item":90},
            {"sr.no": 3, "Item": "Chicken", "Quantity": 20, "Cost/Item":100},
        ]
        self.customerCart = []
        self.totalCost = 0 
        self.deliveryFee = 0
    def purchase(self):
        while True: 
            purchaseNumber = int(input("What do you wanna purchase: "))
            print(self.cart[0]["sr.no"])
            for i in self.cart:
                if i['sr.no'] == purchaseNumber: 
                    purchaseCount = int(input(f"How many {i['Item']} packages you wanna Purchase: "))
                    if purchaseCount <= 0:
                        print(f"Invalid")
                    if purchaseCount > i['Quantity']:
                        print(f"Available quantity of {i['Item']} is {i['Quantity']}")
                        purchaseCount = 0
                    else:
                        itemCost = purchaseCount*i["Cost/Item"]
                        cartDict = {"sr.no":i["sr.no"], "Item": i["Item"], "Qty":purchaseCount, "Total_cost":itemCost}
                        self.totalCost += itemCost
                        self.customerCart.append(cartDict)
                        i['Quantity'] -= purchaseCount
            continueShoping = input("Would you like to continue shoping Y/N : ")
            if continueShoping == "n".lower():
                if len(self.customerCart) == 0:
                    print("Your cart is empty!!")
                    break
                # customer details 
                self.cusDetails()
                # customer bill
                self.calBill()
                 #  calculate store
                self.calStore()
                break
    def calBill(self):
        print("-"*50 + "Bill" + "-"*50)
        print("S.no"+" "*4+"Item"+" "*4+"Qty"+" "*4+"TotalCost")
        for i in self.customerCart:
            print(str(i['sr.no'])+" "*4+i['Item']+" "*4+str(i['Qty'])+" "*4+str(i['Total_cost']))
            print("Total items cost: ", self.totalCost)
            print("Total Bill Amount: Total items cost + Delivery Charge is: ", self.totalCost + self.deliveryFee)
            print("Have a great day!!")
    
    def calStore(self):
        print("-"*50 + "Remaining Quantity in store" + "-"*50)
        print('sr.no'+" "*4+'Item'+" "*4+'Quantity'+" "*4+'Cost/Item')
        for i in self.cart:
            print(str(i['sr.no'])+" "*4+i['Item']+" "*4+str(i['Quantity'])+" "*4+str(i['Cost/Item']))
    
    def cusDetails(self):
        custName = input("Enter your name: ")
        custAddress = input("Enter your address: ")
        custDistance = int(input("Enter the distance from store 5/10/15/30:"))
        if custDistance < 15:
            self.deliveryFee = 50
            print("Delivery Charge: 50 Rs will be levied for distance less than 15km") 
        elif 15 <= custDistance < 30:
            self.deliveryFee = 100 
            print("Delivery Charge: 50 Rs will be levied for distance between 15 and 30km") 
        else:
            print("No delivery Available")
            


if __name__ == "__main__":
    Walmart = ShoppingCart()
    Walmart.purchase()



