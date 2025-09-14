import csv
import os
from datetime import datetime
import random

class BankingSystem:
    def __init__(self):
        self.accounts_file = "accounts.txt"
        self.transactions_file = "transactions.txt"
        self.current_account = None
        self.failed_attempts = {}  # Track failed login attempts
        
        # Initialize files with headers if they don't exist
        self.initialize_files()
    
    def initialize_files(self):
        """Create files with headers if they don't exist"""
        # Initialize accounts.txt
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account Number', 'Name', 'Password', 'Balance'])
        
        # Initialize transactions.txt
        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account Number', 'Transaction Type', 'Amount', 'Date'])
    
    def generate_account_number(self):
        """Generate a unique 6-digit account number"""
        while True:
            account_num = str(random.randint(100000, 999999))
            if not self.account_exists(account_num):
                return account_num
    
    def account_exists(self, account_number):
        """Check if account number already exists"""
        try:
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Account Number'] == account_number:
                        return True
        except FileNotFoundError:
            pass
        return False
    
    def create_account(self):
        """Create a new bank account"""
        print("\n" + "="*50)
        print("CREATE NEW ACCOUNT")
        print("="*50)
        
        try:
            name = input("Enter your full name: ").strip()
            if not name:
                print("❌ Name cannot be empty!")
                return
            
            while True:
                try:
                    initial_deposit = float(input("Enter initial deposit amount: ₹"))
                    if initial_deposit < 0:
                        print("❌ Initial deposit cannot be negative!")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a valid amount!")
            
            password = input("Create a password: ").strip()
            if not password:
                print("❌ Password cannot be empty!")
                return
            
            # Generate unique account number
            account_number = self.generate_account_number()
            
            # Save account to file
            with open(self.accounts_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([account_number, name, password, initial_deposit])
            
            # Log initial deposit transaction
            self.log_transaction(account_number, "Initial Deposit", initial_deposit)
            
            print(f"\n✅ Account created successfully!")
            print(f"📋 Account Number: {account_number}")
            print(f"👤 Account Holder: {name}")
            print(f"💰 Initial Balance: ₹{initial_deposit:.2f}")
            print(f"🔐 Please remember your account number and password for login.")
            
        except Exception as e:
            print(f"❌ Error creating account: {str(e)}")
    
    def login(self):
        """Login to existing account"""
        print("\n" + "="*50)
        print("ACCOUNT LOGIN")
        print("="*50)
        
        try:
            account_number = input("Enter account number: ").strip()
            password = input("Enter password: ").strip()
            
            # Check for account lock
            if account_number in self.failed_attempts and self.failed_attempts[account_number] >= 3:
                print("❌ Account is locked due to multiple failed login attempts!")
                print("Please contact customer service to unlock your account.")
                return
            
            # Verify credentials
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Account Number'] == account_number and row['Password'] == password:
                        self.current_account = {
                            'account_number': account_number,
                            'name': row['Name'],
                            'balance': float(row['Balance'])
                        }
                        # Reset failed attempts on successful login
                        if account_number in self.failed_attempts:
                            del self.failed_attempts[account_number]
                        print(f"\n✅ Welcome back, {row['Name']}!")
                        self.account_menu()
                        return
            
            # Failed login
            if account_number not in self.failed_attempts:
                self.failed_attempts[account_number] = 0
            self.failed_attempts[account_number] += 1
            
            remaining_attempts = 3 - self.failed_attempts[account_number]
            if remaining_attempts > 0:
                print(f"❌ Invalid credentials! {remaining_attempts} attempts remaining.")
            else:
                print("❌ Account locked due to multiple failed attempts!")
                
        except FileNotFoundError:
            print("❌ No accounts found. Please create an account first.")
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
    
    def account_menu(self):
        """Display account menu and handle user choices"""
        while True:
            print("\n" + "="*50)
            print("ACCOUNT MENU")
            print("="*50)
            print(f"👤 Account Holder: {self.current_account['name']}")
            print(f"📋 Account Number: {self.current_account['account_number']}")
            print(f"💰 Current Balance: ₹{self.current_account['balance']:.2f}")
            print("\n1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Mini Statement")
            print("5. Change Password")
            print("6. Fund Transfer")
            print("7. Logout")
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.mini_statement()
            elif choice == '5':
                self.change_password()
            elif choice == '6':
                self.fund_transfer()
            elif choice == '7':
                print("👋 Logging out... Goodbye!")
                self.current_account = None
                break
            else:
                print("❌ Invalid choice! Please select 1-7.")
    
    def check_balance(self):
        """Display current account balance"""
        print(f"\n💰 Current Balance: ₹{self.current_account['balance']:.2f}")
    
    def deposit(self):
        """Deposit money into account"""
        print("\n" + "="*30)
        print("DEPOSIT MONEY")
        print("="*30)
        
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            if amount <= 0:
                print("❌ Deposit amount must be positive!")
                return
            
            # Update balance
            self.current_account['balance'] += amount
            
            # Update accounts file
            self.update_account_balance()
            
            # Log transaction
            self.log_transaction(self.current_account['account_number'], "Deposit", amount)
            
            print(f"✅ ₹{amount:.2f} deposited successfully!")
            print(f"💰 New Balance: ₹{self.current_account['balance']:.2f}")
            
        except ValueError:
            print("❌ Please enter a valid amount!")
        except Exception as e:
            print(f"❌ Deposit error: {str(e)}")
    
    def withdraw(self):
        """Withdraw money from account"""
        print("\n" + "="*30)
        print("WITHDRAW MONEY")
        print("="*30)
        
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            if amount <= 0:
                print("❌ Withdrawal amount must be positive!")
                return
            
            if amount > self.current_account['balance']:
                print("❌ Insufficient balance!")
                print(f"💰 Available Balance: ₹{self.current_account['balance']:.2f}")
                return
            
            # Update balance
            self.current_account['balance'] -= amount
            
            # Update accounts file
            self.update_account_balance()
            
            # Log transaction
            self.log_transaction(self.current_account['account_number'], "Withdrawal", amount)
            
            print(f"✅ ₹{amount:.2f} withdrawn successfully!")
            print(f"💰 New Balance: ₹{self.current_account['balance']:.2f}")
            
        except ValueError:
            print("❌ Please enter a valid amount!")
        except Exception as e:
            print(f"❌ Withdrawal error: {str(e)}")
    
    def mini_statement(self):
        """Display recent transactions"""
        print("\n" + "="*50)
        print("MINI STATEMENT")
        print("="*50)
        print(f"Account: {self.current_account['account_number']}")
        print(f"Account Holder: {self.current_account['name']}")
        print(f"Current Balance: ₹{self.current_account['balance']:.2f}")
        print("\nRecent Transactions:")
        print("-" * 50)
        
        try:
            transactions = []
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Account Number'] == self.current_account['account_number']:
                        transactions.append(row)
            
            # Show last 10 transactions
            recent_transactions = transactions[-10:] if len(transactions) > 10 else transactions
            
            if not recent_transactions:
                print("No transactions found.")
            else:
                for transaction in recent_transactions:
                    print(f"{transaction['Date']} | {transaction['Transaction Type']} | ₹{float(transaction['Amount']):.2f}")
            
        except FileNotFoundError:
            print("No transaction history found.")
        except Exception as e:
            print(f"❌ Error retrieving statement: {str(e)}")
    
    def change_password(self):
        """Change account password"""
        print("\n" + "="*30)
        print("CHANGE PASSWORD")
        print("="*30)
        
        try:
            current_password = input("Enter current password: ").strip()
            
            # Verify current password
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                accounts = list(reader)
            
            account_found = False
            for account in accounts:
                if (account['Account Number'] == self.current_account['account_number'] and 
                    account['Password'] == current_password):
                    account_found = True
                    break
            
            if not account_found:
                print("❌ Current password is incorrect!")
                return
            
            new_password = input("Enter new password: ").strip()
            if not new_password:
                print("❌ Password cannot be empty!")
                return
            
            confirm_password = input("Confirm new password: ").strip()
            if new_password != confirm_password:
                print("❌ Passwords do not match!")
                return
            
            # Update password in accounts file
            for account in accounts:
                if account['Account Number'] == self.current_account['account_number']:
                    account['Password'] = new_password
                    break
            
            with open(self.accounts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account Number', 'Name', 'Password', 'Balance'])
                for account in accounts:
                    writer.writerow([account['Account Number'], account['Name'], 
                                   account['Password'], account['Balance']])
            
            print("✅ Password changed successfully!")
            
        except Exception as e:
            print(f"❌ Error changing password: {str(e)}")
    
    def fund_transfer(self):
        """Transfer money to another account"""
        print("\n" + "="*30)
        print("FUND TRANSFER")
        print("="*30)
        
        try:
            recipient_account = input("Enter recipient account number: ").strip()
            
            if recipient_account == self.current_account['account_number']:
                print("❌ Cannot transfer to your own account!")
                return
            
            # Check if recipient account exists
            recipient_found = False
            recipient_name = ""
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Account Number'] == recipient_account:
                        recipient_found = True
                        recipient_name = row['Name']
                        break
            
            if not recipient_found:
                print("❌ Recipient account not found!")
                return
            
            amount = float(input(f"Enter amount to transfer to {recipient_name}: ₹"))
            if amount <= 0:
                print("❌ Transfer amount must be positive!")
                return
            
            if amount > self.current_account['balance']:
                print("❌ Insufficient balance!")
                print(f"💰 Available Balance: ₹{self.current_account['balance']:.2f}")
                return
            
            # Update sender's balance
            self.current_account['balance'] -= amount
            self.update_account_balance()
            self.log_transaction(self.current_account['account_number'], f"Transfer to {recipient_account}", amount)
            
            # Update recipient's balance
            self.update_recipient_balance(recipient_account, amount)
            self.log_transaction(recipient_account, f"Transfer from {self.current_account['account_number']}", amount)
            
            print(f"✅ ₹{amount:.2f} transferred successfully to {recipient_name}!")
            print(f"💰 Your new balance: ₹{self.current_account['balance']:.2f}")
            
        except ValueError:
            print("❌ Please enter a valid amount!")
        except Exception as e:
            print(f"❌ Transfer error: {str(e)}")
    
    def update_account_balance(self):
        """Update account balance in accounts file"""
        try:
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                accounts = list(reader)
            
            for account in accounts:
                if account['Account Number'] == self.current_account['account_number']:
                    account['Balance'] = str(self.current_account['balance'])
                    break
            
            with open(self.accounts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account Number', 'Name', 'Password', 'Balance'])
                for account in accounts:
                    writer.writerow([account['Account Number'], account['Name'], 
                                   account['Password'], account['Balance']])
        except Exception as e:
            print(f"❌ Error updating balance: {str(e)}")
    
    def update_recipient_balance(self, recipient_account, amount):
        """Update recipient's balance after transfer"""
        try:
            with open(self.accounts_file, 'r') as file:
                reader = csv.DictReader(file)
                accounts = list(reader)
            
            for account in accounts:
                if account['Account Number'] == recipient_account:
                    account['Balance'] = str(float(account['Balance']) + amount)
                    break
            
            with open(self.accounts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Account Number', 'Name', 'Password', 'Balance'])
                for account in accounts:
                    writer.writerow([account['Account Number'], account['Name'], 
                                   account['Password'], account['Balance']])
        except Exception as e:
            print(f"❌ Error updating recipient balance: {str(e)}")
    
    def log_transaction(self, account_number, transaction_type, amount):
        """Log transaction to transactions file"""
        try:
            with open(self.transactions_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([account_number, transaction_type, amount, datetime.now().strftime("%Y-%m-%d")])
        except Exception as e:
            print(f"❌ Error logging transaction: {str(e)}")
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n" + "="*60)
            print("🏦 WELCOME TO THE BANKING SYSTEM 🏦")
            print("="*60)
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            print("="*60)
            
            choice = input("Select an option (1-3): ").strip()
            
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("👋 Thank you for using our Banking System. Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-3.")

def main():
    """Main function to run the banking system"""
    banking_system = BankingSystem()
    banking_system.main_menu()

if __name__ == "__main__":
    main()
