# Parent class
class Customer:
    isAlive = True
    customer_type = 'Generic'

    # Cunstructor/initializer of object
    def __init__(self, first_name, last_name, call_reason):
        self.first_name = first_name
        self.last_name = last_name
        self.call_reason = call_reason
        self.type = 'Generic'

    def buy(self):
        print('*purchase*')
        return "*purchase*"

    def subscribe(self):
        print(self.first_name, self.last_name, " has joined.")
        return self.first_name + self.last_name + " has joined."

    def cancel(self):
        print(self.first_name, self.last_name, " has canceled the subscription.")
        return self.first_name + self.last_name + " has canceled the subscription."

    def __str__(self):
        return self.first_name + self.last_name + ": " + str(self.call_reason)

    def death(self):
        print(self.first_name, self.last_name, "has died.")
        self.isAlive = False
        
# Child class of Customer
class New_customer(Customer):
    customer_type = 'New Customer'
    def buy(self):
        print("*purchase*")
        return("*purchase*")

    def subscribe(self):
        print(self.first_name, self.last_name, " has subscribed!")
        return self.first_name + self.last_name + " has subscribed!"
# Child class of Customer
class Existing_customer(Customer):
    customer_type = 'Existing Customer'
    def buy(self):
        print("*purchase*")
        return("*purchase*")

    def cancel(self):
        print(self.first_name, self.last_name, "has cancelled!")
        return self.first_name + self.last_name + " has cancelled!"

    


# Initializing instances of Customer/New/Existing

def main():
    a1 = Customer("Brenda", "Davis", "buying a product")
    c1 = New_customer("Solomon", "Grandi", "buying a subscription")
    d1 = Existing_customer("Nicole", "Baskerville", "cancelling a subscription")

    lst_customers = [a1, c1, d1]

    for obj in lst_customers:
        print(obj)
        obj.buy()
        obj.subscribe()
        obj.cancel()

if __name__ == '__main__':
    main()

