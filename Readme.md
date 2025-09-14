# 🏦 Python Console-Based Banking System

A **console-based Banking System** built in **Python** with file handling, secure login, and transaction management.  
This project is part of **Project-Rollout B3M1** and demonstrates persistent storage, modular programming, and error handling.

---

## ✨ Features

### 🔹 Core Functionalities
- 📂 **File Handling**
  - `accounts.txt` → Stores account details *(Account Number, Name, Password, Balance)*
  - `transactions.txt` → Stores transaction history *(Account Number, Transaction Type, Amount, Date)*
  - Automatic file initialization with headers
- 🏠 **Main Menu**
  - Create Account
  - Login
  - Exit
- 👤 **Account Creation**
  - Unique 6-digit account number generation
  - Name, password, initial deposit input
  - Initial transaction logged automatically
- 🔑 **Login System**
  - Account number + password verification
  - Account lock after 3 failed attempts
- 💼 **Account Menu**
  - Check Balance
  - Deposit Money
  - Withdraw Money
  - Mini Statement
  - Change Password ✅
  - Fund Transfer ✅
  - Logout

### 🔹 Error Handling
- Invalid login credentials
- Insufficient balance checks
- Invalid deposits/withdrawals
- Account lockout after 3 failed attempts
- Input validation with helpful error messages

### 🔹 Extra Features
- 🔐 **Change Password** with old password verification
- 💸 **Fund Transfer** between accounts
- 🔒 **Account Lockout** for security
- 🎨 **Pretty Console UI** with emojis and clear menus

---

## 🛠️ Tech Stack

- **Language**: Python 3
- **File Handling**: CSV (via `csv` module)
- **Storage**: `accounts.txt`, `transactions.txt`
- **Modules Used**: `csv`, `datetime`, `os`, `random`

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/banking-system.git
   cd banking-system


## 📸 Demo (Console Flow)

![Demo 1](https://github.com/VTCodeCraft/Python-Console-Based-Banking-System/blob/main/Screenshot%202025-09-14%20135246.png?raw=true)

![Demo 2](https://github.com/VTCodeCraft/Python-Console-Based-Banking-System/blob/main/Screenshot%202025-09-14%20135257.png?raw=true)

![Demo 3](https://github.com/VTCodeCraft/Python-Console-Based-Banking-System/blob/main/Screenshot%202025-09-14%20135326.png?raw=true)
