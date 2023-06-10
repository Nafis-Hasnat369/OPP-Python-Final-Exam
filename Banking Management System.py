class Bank:
    def __init__(self, name) -> None:
        self.name = name
        self.__all_accounts = []
        self.loan_status = True
        self.bank_balance = 0

    def create_bank_account(self, name, email, password):
        account = Bank_account(name, email, password)
        account.role = 'Customer'
        self.__all_accounts.append(account)
        return account

    def create_admin_account(self, name, email, password):
        account = Bank_account(name, email, password)
        account.role = 'ADMIN'
        self.__all_accounts.append(account)
        return account

    def total_balance_of_bank(self, user):
        if user.role == 'ADMIN':
            total_balance = 0
            for account in self.__all_accounts:
                total_balance += account.my_balance
            print(f'Total balance of The {self.name} ${total_balance}\n')
        else:
            print(f'UNAUTHORIZED ACCESS/ACCESS DENIED!!!\n')

    def total_loan(self, user):
        if user.role == 'ADMIN':
            total_loan = 0
            for account in self.__all_accounts:
                total_loan += account.my_loan
            print(f'Total loan given by the Bank ${total_loan}\n')
        else:
            print(f'UNAUTHORIZED ACCESS/ACCESS DENIED!!!\n')

    def active_loan(self, user):
        if user.role == 'ADMIN':
            if self.loan_status == True:
                self.loan_status = False
            else:
                self.loan_status = True
        else:
            print(f'UNAUTHORIZED ACCESS/ACCESS DENIED!!!\n')

    def get_loan_status(self):
        return self.loan_status

    def set_bank_balance(self, amount):
        self.bank_balance += amount

    # def __repr__(self) -> str:
    #     # print(len(self.__all_accounts))
    #     print(self.loan_status)
    #     return ''


class Bank_account:
    def __init__(self, name, email, password) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.my_balance = 0
        self.transactions = []
        self.my_loan = 0

    def deposit(self, amount):
        self.my_balance += amount
        self.transactions.append(f'Deposited amount: ${amount}')
        world_bank.set_bank_balance(amount)
        print(
            f'{self.name} deposited ${amount} successfully! New Balance: ${self.my_balance}\n')

    def withdraw(self, amount):
        if self.my_balance >= amount:
            self.my_balance -= amount
            world_bank.set_bank_balance(-amount)
            self.transactions.append(f'Withdrawal amount: ${amount}')
            print(
                f'{self.name} withdrawal ${amount} successfully! New Balance: ${self.my_balance}\n')
        else:
            print('Insufficient balance!\n')

    def available_balance(self):
        print(f'Available Balance: ${self.my_balance}\n')

    def transfer_money(self, receiver_account, amount):
        if self.my_balance >= amount and self.email != receiver_account.email:
            self.my_balance -= amount
            receiver_account.my_balance += amount
            self.transactions.append(
                f"Sent: ${amount} to {receiver_account.name}")
            receiver_account.transactions.append(
                f"Received: ${amount} from {self.name}")
            print(
                f'${amount} has been sent successfully! from {self.name} to {receiver_account.name}\n')
        elif self.email == receiver_account.email:
            print(f'Transaction failed!!! you can\'t send money to you\'re own account\n')
        else:
            print('Transaction failed due to insufficient balance!\n')

    def print_transaction_history(self):
        print(f'-------Transaction History of {self.name}-------\n')
        for transaction in self.transactions:
            print(transaction)
        print('\n-------------End------------\n')

    def take_loan(self, amount):
        if self.my_loan > 0 and world_bank.bank_balance > self.my_balance * 2:
            print(
                f'Sorry, you can\'t take loan twice, your previous loan amount is ${self.my_loan}\n')
        elif world_bank.get_loan_status() == True and world_bank.bank_balance > self.my_balance * 2:
            if amount <= self.my_balance * 2:
                self.my_loan = amount
                self.transactions.append(f"Given loan: ${self.my_loan}")
                print(
                    f'Congratulation you have successfully got loan of ${self.my_loan}\n')
            else:
                print(
                    f'Sorry, you can\'t take loan more than twice the amount of your balance\n')
        else:
            print(f'THE BANK IS BANKRUPT\n sorry, you can\'t take any loan now!\n')


world_bank = Bank('World Bank')

# Create user account
user1 = world_bank.create_bank_account('User1', 'user1@gmail.com', '#user1')
user2 = world_bank.create_bank_account('User2', 'user2@gmail.com', '#user2')

print("---------Deposits---------\n")
# deposit
user1.deposit(2000)
user1.deposit(5000)
user2.deposit(9000)

print("---------Withdraw---------\n")
# withdraw
user1.withdraw(500)
user2.withdraw(1000)

print("---------Balance Check---------\n")
# balance check
user1.available_balance()
user2.available_balance()

print("---------Money Transfer---------\n")
# transfers
user1.transfer_money(user1, 500)
user1.transfer_money(user2, 500)
user1.transfer_money(user2, 10000)
user2.transfer_money(user1, 5000)

# transaction history
user1.print_transaction_history()
# user2.print_transaction_history()

print("---------Loans---------\n")
# loan
user1.take_loan(6000)
user2.take_loan(10000)


# create admin account
admin = world_bank.create_admin_account('Admin', 'admin@gmail.com', '#admin')
# admin.deposit(10000)

print("---------Total Balance---------\n")
# available balance in the bank
world_bank.total_balance_of_bank(admin)

print("---------Total Loan---------\n")
# total loan given by the bank
world_bank.total_loan(admin)

# disable loan
print("-------Disabled loan---------\n")
world_bank.active_loan(admin)
user2.take_loan(2000)

# enable loan
print("-------After Active Loan---------\n")
world_bank.active_loan(admin)
user2.take_loan(2000)

# print(world_bank.bank_balance)
