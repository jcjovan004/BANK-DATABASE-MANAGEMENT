import mysql.connector
from abc import ABC, abstractmethod

# Abstract class representing a person (Abstraction)
class Person(ABC):
    def __init__(self, name, email):
        self._name = name  # Encapsulation: Protected variable
        self._email = email

    @abstractmethod
    def get_details(self):
        pass

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.__connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.__cursor = self.__connection.cursor()  # Encapsulation: Private variables
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
        
    def execute_query(self, query, data=None):
        try:
            if data:
                self.__cursor.execute(query, data)
            else:
                self.__cursor.execute(query)
            self.__connection.commit()
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        
    def fetch_all(self, query, data=None):
        try:
            if data:
                self.__cursor.execute(query, data)
            else:
                self.__cursor.execute(query)
            return self.__cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return []
    
    def close(self):
        self.__cursor.close()
        self.__connection.close()

# Inheriting from Person (Inheritance)
class Customer(Person):
    def __init__(self, customer_id, name, email):
        super().__init__(name, email)  # Call to parent class constructor
        self._customer_id = customer_id  # Private variable

    def get_details(self):
        return {"Customer ID": self._customer_id, "Name": self._name, "Email": self._email}  # Abstract method

class Account:
    def __init__(self, account_id, customer_id, balance):
        self._account_id = account_id  # Changed from private to protected
        self._customer_id = customer_id
        self._balance = float(balance)  # Ensure balance is a float

    def deposit(self, amount):
        self._balance += float(amount)
        query = "UPDATE accounts SET balance = %s WHERE account_id = %s"
        db.execute_query(query, (self._balance, self._account_id))

    def withdraw(self, amount):
        if float(amount) <= self._balance:
            self._balance -= float(amount)
            query = "UPDATE accounts SET balance = %s WHERE account_id = %s"
            db.execute_query(query, (self._balance, self._account_id))
        else:
            print("Insufficient funds.")
    
    def get_balance(self):
        return self._balance 

# Derived class for specialized types of accounts (Inheritance)
class SavingsAccount(Account):
    def __init__(self, account_id, customer_id, balance, interest_rate):
        super().__init__(account_id, customer_id, balance)
        self.__interest_rate = float(interest_rate)

    def apply_interest(self):
        self._balance += self._balance * self.__interest_rate
        query = "UPDATE accounts SET balance = %s WHERE account_id = %s"
        db.execute_query(query, (self._balance, self._account_id))  # Use protected _account_id

class Bank:
    def __init__(self, db):
        self.db = db

    def create_customer(self, name, email):
        query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
        self.db.execute_query(query, (name, email))
        customer_id = self.db._Database__cursor.lastrowid
        return Customer(customer_id, name, email)
    
    def create_account(self, customer_id, initial_balance):
        query = "INSERT INTO accounts (customer_id, balance) VALUES (%s, %s)"
        self.db.execute_query(query, (customer_id, float(initial_balance)))
        account_id = self.db._Database__cursor.lastrowid
        return Account(account_id, customer_id, float(initial_balance))

    def get_customer(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = %s"
        result = self.db.fetch_all(query, (customer_id,))
        if result:
            return Customer(result[0][0], result[0][1], result[0][2])
        return None

    def get_account(self, account_id):
        query = "SELECT * FROM accounts WHERE account_id = %s"
        result = self.db.fetch_all(query, (account_id,))
        if result:
            return Account(result[0][0], result[0][1], float(result[0][2]))  # Convert to float
        return None

    def transfer(self, from_account_id, to_account_id, amount):
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if from_account.get_balance() >= float(amount):
            from_account.withdraw(amount)
            to_account.deposit(amount)
            print(f"Transferred {amount} from account {from_account_id} to {to_account_id}")
        else:
            print("Insufficient balance for transfer.")
            
# Instantiate Database
db = Database(host='localhost', user='root', password='Jovan1234', database='bank_system')

# Instantiate Bank
bank = Bank(db)

# Example usage
def main():
    customer = bank.create_customer('John Doe', 'john.doe@example.com')
    
    account = bank.create_account(customer.get_details()['Customer ID'], 1000.00)
    
    account.deposit(500.00)
    
    account.withdraw(200.00)
    
    fetched_customer = bank.get_customer(customer.get_details()['Customer ID'])
    print(f"Customer: {fetched_customer._name}, Email: {fetched_customer._email}")

    # Example of a transfer between two accounts
    customer2 = bank.create_customer('Jane Doe', 'jane.doe@example.com')
    account2 = bank.create_account(customer2.get_details()['Customer ID'], 500.00)
    bank.transfer(account._account_id, account2._account_id, 300.00)

if __name__ == "__main__":
    main()
