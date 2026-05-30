# Budget Tracker

A comprehensive Python-based personal finance management application that helps you track income and expenses, manage spending categories, and visualize financial data through interactive charts.

## Description

Budget Tracker is a desktop application designed to simplify personal finance management. It provides an intuitive graphical user interface built with tkinter and customtkinter, allowing users to:

- **Track Transactions**: Log all income and expense transactions with detailed information
- **Manage Categories**: Organize transactions by customizable spending and income categories
- **Visualize Data**: Generate interactive bar charts to analyze income and expense patterns
- **Secure Accounts**: User authentication system with password management
- **Real-time Notifications**: Receive instant alerts on financial activities
- **Analyze Trends**: Review transaction history with filtering and analysis tools

The application stores all data securely in a local SQLite database, ensuring your financial information remains private and accessible only to you.

## Features

### Core Features
- **User Authentication**: Secure login and registration system with password hashing
- **Transaction Management**: 
  - Add, edit, and delete income and expense transactions
  - Track transaction date, category, amount, title, and description
  - View transaction history with automatic refresh
- **Category Management**:
  - Manage income categories separately from expense categories
  - Create custom categories for better organization
  - Edit and delete categories as needed
- **Financial Dashboard**:
  - View balance overview at a glance
  - Display total income and total expenses
  - Quick access to recent transactions
- **Data Visualization**:
  - Interactive bar charts for income by category
  - Interactive bar charts for expenses by category
  - Real-time chart generation with matplotlib integration
- **Notifications**: Receive notifications for new transactions and financial updates
- **Settings**: Customize application preferences and user profile management
- **Password Management**: Change account password securely

### Technical Features
- Clean, modern UI with customizable theme
- Responsive interface with scrollable transaction lists
- Auto-refresh functionality for real-time updates
- Secure database with abstracted interface layer
- Modular architecture for easy maintenance and extension

## Technologies Used

- **Python 3.x** - Core programming language
- **Tkinter** - Standard Python GUI library
- **CustomTkinter** - Modern themed tkinter widgets for enhanced UI
- **SQLite3** - Lightweight database for data persistence
- **Matplotlib** - Data visualization and chart generation
- **Pandas** - Data analysis and manipulation
- **Pillow (PIL)** - Image processing and asset handling

## Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your system
- pip (Python package installer)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kyleeeee0/Budget-Tracker.git
   cd Budget-Tracker
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Dependencies**
   ```bash
   pip install customtkinter matplotlib pandas pillow
   ```

5. **Run the Application**
   ```bash
   python Main.py
   ```

The application window will open, displaying the login/registration interface.

## Usage

### Getting Started

1. **Create an Account**
   - Launch the application
   - Click on "Sign In" to create a new account
   - Enter your desired username and password
   - Confirm your registration

2. **Log In**
   - Enter your username and password
   - Click "Log In" to access your dashboard

### Main Dashboard

Once logged in, you'll see the home dashboard with:
- **Navigation Sidebar** (Left): Quick access to different features
  - Home
  - Analysis
  - Transactions
  - Categories
- **Welcome Section** (Top): Personalized greeting and time-based message
- **Transaction Panel** (Right): Recent transactions with edit options
- **Analysis Panel** (Left): Quick financial overview

### Adding a Transaction

1. Click the **Transactions** button in the sidebar
2. Click **Add Income** or **Add Expense** button
3. Fill in the transaction details:
   - Select the date
   - Choose a category
   - Enter the amount
   - Add a title and description
4. Click **Save** to record the transaction

### Viewing Analysis

1. Click the **Analysis** button in the sidebar
2. Choose between:
   - **Income Analysis** - View income sources by category
   - **Expense Analysis** - View expenses by category
3. Charts automatically display totals for each category

### Managing Categories

1. Click the **Categories** button in the sidebar
2. View existing categories
3. Create, edit, or delete categories as needed
4. Organize your transactions with custom categories

### Settings

1. Click the **Settings** icon (gear icon) in the top-right corner
2. Available options:
   - Change password
   - Update profile information
   - Customize application preferences

### Notifications

1. Click the **Notification** icon (bell icon) in the top-right corner
2. View recent transaction alerts and system notifications
3. Stay updated on your financial activities

## Project Structure

```
Budget-Tracker/
├── Main.py                      # Application entry point
├── Controller.py                # Business logic controller
├── Database.py                  # Database interface and operations
├── Log_In.py                    # Login form UI
├── Sign_In.py                   # Registration form UI
├── Transaction.py               # Transaction management tab
├── transaction_entry.py         # Transaction entry form
├── Categories.py                # Category management tab
├── Category_Entry.py            # Category entry form
├── Category_Income.py           # Income category handler
├── Category_Expense.py          # Expense category handler
├── Analysis.py                  # Analysis tab and base tab class
├── Analysis_Income_Charts.py    # Income chart generation
├── Analysis_Expense_Charts.py   # Expense chart generation
├── Notification.py              # Notification system
├── Settings.py                  # Application settings
├── Change_Password.py           # Password change interface
├── assets/                      # UI images and graphics
│   ├── assets_home/
│   ├── assets_transaction/
│   ├── assets_user_authentication/
│   └── assets_analysis/
├── tests/                       # Unit and integration tests
└── README.md                    # Project documentation
```

## Database Schema

The application uses SQLite3 with the following main tables:

- **users** - User account information (username, hashed password)
- **transactions** - Income and expense records
- **categories** - User-defined transaction categories
- **notifications** - User activity notifications

## Features in Detail

### Secure Authentication
- Password hashing for secure storage
- Account recovery options
- Session management

### Transaction Tracking
- Timestamp for all transactions
- Flexible categorization
- Detailed descriptions
- Edit and delete capabilities

### Financial Analysis
- Category-based expense breakdown
- Income source analysis
- Visual trend representation
- Historical data tracking

## License & Contact

**License**: [Add your license here - e.g., MIT License, GPL-3.0, etc.]

**Author**: Kyle Luis Marcial

**Repository**: [https://github.com/Kyleeeee0/Budget-Tracker](https://github.com/Kyleeeee0/Budget-Tracker)

**Contact**: [Add your contact information here - e.g., email, LinkedIn, etc.]

## Future Enhancements

- Export reports to PDF/CSV format
- Budget goal setting and tracking
- Recurring transaction automation
- Data backup and restore functionality
- Mobile app companion
- Multi-user support with shared budgets

## Troubleshooting

### Application Won't Start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that no other instance is running

### Database Errors
- Ensure write permissions in the application directory
- Delete the existing database file to reinitialize (WARNING: This will erase all data)

### UI Display Issues
- Update CustomTkinter: `pip install --upgrade customtkinter`
- Ensure your system meets display scaling requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request with improvements, bug fixes, or new features.

---

**Happy Budget Tracking! 💰**
