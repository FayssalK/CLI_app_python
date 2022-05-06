# CLI application that increase LV1 CSRs efficiency by prompting instead of flowwing a script
# Customer types: Customer, New Customer, Existing Customer
#           - Attributes: First Name, Last Name, Call Reason
# Want to store our customer information to a file
# Upon restarting application, want to load customer data from file

# Importing customer module
import Parent_class_Customer as customer
import re
from pymongo import MongoClient
import logging

logging.basicConfig(filename='customer.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p::')

'''
DEBUG    - Detailed info, typically of interest only when diagnosing problems
INFO     - Confirmation that things are working as usual
WARNING  - An indication that something unexpected happened, or some problem may occur in the near future
ERROR    - Due to a serious problem, the application has not been able to perform some function
CRITICAL - A serious error indicating the program may be unable to continue
'''

# Used to create customer object from user-inputted values
def add_customer() -> customer.Customer:
    logging.debug("Entering add_customer")
    # Input verification
    while True:
        try:
            print("Is this a:")
            print("\t a) Other")
            print("\t c) New Customer")
            print("\t d) Existing Customer")
            typeCustomer = input(">>>")

            
            if not typeCustomer == 'c' and not typeCustomer == 'd' and not typeCustomer == 'a':
                raise ValueError('Invalid input for Customer Type')
            else:
                break
        except ValueError:
            print("Oh no! Please enter a valid type for this customer! ('a', 'c', 'd')")
            pass

    while True:
        try:
            print("\n\nEnter customer first name:")
            first_name = input(">>>")
            if not re.search(r"[,\.\\\*\-]", first_name) == None:
                raise ValueError
            else:
                break
        except ValueError:
            print("Customer first name cannot have special characters!")
            logging.info("ValueError caught: CSR entered special char in first name")


    while True:
        try:
            print("\n\nEnter customer last name:")
            last_name = input(">>>")
            if not re.search(r"[,\.\\\*\-]", last_name) == None:
                raise ValueError
            else:
                break
        except ValueError:
            print("Customer last name cannot have special characters!")
            logging.info("ValueError caught: CSR entered special char in last name")


    while True:
        try:
            print("\n\nEnter call reason:")
            call_reason = input(">>>")
            break
        except ValueError:
            print("Oh no! You must enter the reason for the call! Try again!")

    if typeCustomer == 'a':
        newCustomer = customer.Customer(first_name, last_name, call_reason)
    elif typeCustomer == 'c':
        newCustomer = customer.New_customer(first_name, last_name, call_reason)
    else:
        newCustomer = customer.Existing_customer(first_name, last_name, call_reason)
    
    return newCustomer


# Save customer list to saved_customers.txt
def save_customers(lst_Customers):
    logging.debug("Entering save_customers")
    f = open('saved_customers.txt', 'w')

    for customer in lst_Customers:
        f.write(customer.first_name + customer.last_name + ',' + str(customer.call_reason) + ',' +  customer.customer_type + "\n")

    f.close()

# Load customers from saved_customers.txt
def load_customers():
    logging.debug("Entering load_customers")
    f = open('saved_customers.txt', 'w+')
    lst_customers = []
    for line in f:
        if line == '':
            break

        customer_data = line.split(',')
        if customer_data[2].strip() == 'Generic':
            newCustomer = customer.Customer(customer_data[0], customer_data[1])
        elif customer_data[2].strip() == 'New Customer':
            newCustomer = customer.New_customer(customer_data[0], customer_data[1])
        else:
            newCustomer = customer.Existing_customer(customer_data[0], customer_data[1])
        
        lst_customers.append(newCustomer)
    f.close()
    return lst_customers

# Function to save a customer to collection in MongoDB
def save_to_db(cust, customerdb):
    logging.debug("Entering save_to_db")
    dict_Customer = {
        "first name" : cust.first_name,
        "last name" : cust.last_name,
        "customer type" : cust.type
    }

    customerdb.customers.insert_one(dict_Customer)
    logging.info("Successfully added an object to database")

#Main function
def main():
    check_conn = True
    try:
        client = MongoClient("127.0.0.1", 27017)

        customerdb = client.customer
    except BaseException:
        print("Sorry, could not connect!")
        check_conn = False

    print("Please enter Customer information promptly!")

    lst_Customer = load_customers()
    while True:
        try:
            print("Please select an option:")
            print("\ta) Enter Customer info")
            print("\ts) Save all calls to MongoDB (only run once!)")
            print("\tq) Quit")

            option = input(">>>")

            logging.debug("User inputted %s", option)

            if option == 'q':
                break

            elif option == 's' and check_conn:
                try:
                    for cust in lst_Customer:
                        save_to_db(cust, customerdb)
                except BaseException:
                    print("Sorry, could not make a good connection to db!")

            elif option == 's' and not check_conn:
                print("Sorry! Connection to db not established")

            elif option == 'a':
                lst_Customer.append(add_customer())

            else:
                raise ValueError('Invalid menu option')

        except ValueError as ve:
            print(ve)
            print("Invalid option! Please try again!")
    
    for customer in lst_Customer:
        print(customer, type(customer))
    
    save_customers(lst_Customer)


if __name__ == '__main__':
    main()


