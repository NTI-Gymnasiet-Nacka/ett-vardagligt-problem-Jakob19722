import sys
import pickle #used to store data
from datetime import date
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QInputDialog, QListWidget, QListWidgetItem, QLineEdit, QDialog, QDialogButtonBox, QFormLayout, QCalendarWidget

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Login") #window title

        self.username = QLineEdit(self) #where the name is typed
        self.password = QLineEdit(self) #where password is typed
        self.password.setEchoMode(QLineEdit.Password) #changes the password text to asterikses so it cannot be seen.

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self) #creates  a dialog box)
        self.buttons.accepted.connect(self.accept) #what to do if accept
        self.buttons.rejected.connect(self.reject) #what to do if cancel

        layout = QFormLayout(self) #creates new area for buttons
        layout.addRow("Username", self.username) #username text
        layout.addRow("Password", self.password) #password text
        layout.addWidget(self.buttons) #ok and cancel buttons 


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super(RegisterDialog, self).__init__(parent)
        self.setWindowTitle("Register") #window title

        self.username = QLineEdit(self) #where name is typed
        self.password = QLineEdit(self) #where password is typed
        self.password.setEchoMode(QLineEdit.Password) #makes password more secure with asteriks

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self) #creates the buttons
        self.buttons.accepted.connect(self.accept) #what to do if accept
        self.buttons.rejected.connect(self.reject) #what to do if cancel

        layout = QFormLayout(self) #manages widgets and labels
        layout.addRow("Username", self.username) #username text
        layout.addRow("Password", self.password) #password text
        layout.addWidget(self.buttons) #ok and cancel buttons


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super(CalendarDialog, self).__init__(parent)
        self.setWindowTitle("Calendar") # window title

        self.calendar = QCalendarWidget(self) #created the calender widget
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self) #creates the buttons
        self.buttons.accepted.connect(self.accept) # do this if ok
        self.buttons.rejected.connect(self.reject) # do this if cnacel

        layout = QVBoxLayout(self) #manages the layout
        layout.addWidget(self.calendar) #add calender to the layout
        layout.addWidget(self.buttons) #add button to the layout


class BudgetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Planner") #window title
        self.credentials = {} #how much money
        self.expenses = {} #how many expenses
        self.budget = 0 #begin with 0 money
        self.initUI() 
        self.load_state()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel('Please login or register') #crate label
        self.login_button = QPushButton('Login') #login button
        self.register_button = QPushButton('Register') #register button
        self.set_budget_button = QPushButton('Set Budget') #budget button
        self.add_expense_button = QPushButton('Add Expense') #expenses button
        self.view_day_button = QPushButton('View Expenses for Day') #view expenses for a day button
        self.view_calendar_button = QPushButton('View Calendar') #calender button
        self.expense_list = QListWidget() #provides a list

        self.login_button.clicked.connect(self.login) #if login is clicked call the login method
        self.register_button.clicked.connect(self.register) #if reg button is clicked call the reg method
        self.set_budget_button.clicked.connect(self.set_budget) # if budget button is clicked call the budget method
        self.add_expense_button.clicked.connect(self.add_expense) # if the expense button is clicked call the expense method
        self.view_day_button.clicked.connect(self.view_day) #if view the day button is clicked call its method
        self.view_calendar_button.clicked.connect(self.view_calendar) # if the calender button is called call its method
        
        #adding widgets/buttons to the layout

        self.layout.addWidget(self.label) 
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.set_budget_button)
        self.layout.addWidget(self.add_expense_button)
        self.layout.addWidget(self.view_day_button)
        self.layout.addWidget(self.view_calendar_button)
        self.layout.addWidget(self.expense_list)

        self.setLayout(self.layout)

        self.is_logged_in = False # sets so that the user is not logged in 
        self.add_expense_button.setEnabled(False) #disable the expense button
        self.view_day_button.setEnabled(False) #disable to view day button
        self.view_calendar_button.setEnabled(False) #disable to view calender button
        self.expense_list.setEnabled(False) #disables expense list

        self.setStyleSheet( #styles
            """
            QPushButton {
                background-color: #4CAF50;
                font-size: 15px;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:disabled {
                background-color: #A9A9A9;
            }
            QLabel {
                font-size: 20px;
            }
            QListWidget {
                font-size: 15px;
            }
            """
        )

    def login(self):
        login_dialog = LoginDialog(self) #creates a diaglog box
        if login_dialog.exec_() == QDialog.Accepted:
            username = login_dialog.username.text() #saves the username
            password = login_dialog.password.text() #saves the password
            if self.credentials.get(username) == password: #if the username and the password match the saved ones logg in = true
                self.is_logged_in = True
                self.label.setText('Welcome, ' + username) #welcoming the user upon loging in
                self.login_button.setEnabled(False)
                self.register_button.setEnabled(False)
                self.set_budget_button.setEnabled(True) #budget button is not acessable
            else:
                self.label.setText('Invalid login. Please try again.') #user will try again if failed credentials
    #this is the same as before
    def register(self):
        register_dialog = RegisterDialog(self) 
        if register_dialog.exec_() == QDialog.Accepted:
            username = register_dialog.username.text()
            password = register_dialog.password.text()
            if username not in self.credentials:
                self.credentials[username] = password
                self.label.setText('Registration successful. Please login.')
            else:
                self.label.setText('Username already exists. Please try again.')

    def set_budget(self):
        budget, ok = QInputDialog.getDouble(self, 'Budget Input', 'Enter your budget:') #creates a dialog where user can enter their budget
        if ok:
            self.budget = float(budget) #makes it a float number
            self.label.setText('Budget: $' + str(self.budget)) #makes it so the text can show the inputed budget
            self.set_budget_button.setEnabled(False) #disable the budget button
            self.add_expense_button.setEnabled(True) #enable add expense button
            self.view_day_button.setEnabled(True) # enable view day button
            self.view_calendar_button.setEnabled(True) #enable view calender button
            self.expense_list.setEnabled(True) # enable expense list button

    def add_expense(self):
        if self.is_logged_in: #if logges in create the calender dialog
            calendar_dialog = CalendarDialog(self)
            if calendar_dialog.exec_() == QDialog.Accepted:  #if user  picked a date and clicks ok continue
                selected_date = calendar_dialog.calendar.selectedDate() 
                day = selected_date.day()
                month = selected_date.month()
                expense, ok = QInputDialog.getDouble(self, 'Expense Input', 'Enter your expense:')
                if ok: #if ok this happens:
                    if month not in self.expenses: #if expens not exist for this month then create an entry
                        self.expenses[month] = {}
                    if day not in self.expenses[month]: #if expens not exist yet for this day create an entry
                        self.expenses[month][day] = []
                    self.expenses[month][day].append(expense) #takes the cost of that day on that month
                    self.budget -= expense #new budget is old - spent
                    self.label.setText('Budget: $' + str(self.budget)) #changing the text to the new budget
                    self.expense_list.addItem(QListWidgetItem('Expense for day ' + str(day) + ', month ' + str(month) + ': $' + str(expense))) #adds to the list what happened

    def view_day(self):
        day, ok = QInputDialog.getInt(self, 'Day Input', 'Enter day of month to view expenses for:', min=1, max=31) #makes the user have to input a day inbetween 1-31
        if ok:
            month, ok = QInputDialog.getInt(self, 'Month Input', 'Enter month to view expenses for:', min=1, max=12) #same but for month
            if ok:
                expenses = self.expenses.get(month, {}).get(day, []) #view the expenses of a certain day of a certain month
                expenses_str = "\n".join(["$"+str(e) for e in expenses])  #creating a text string for  each expense in the list
                if expenses_str: #if there is any expenses
                    self.expense_list.clear() #clear the list
                    #ads the expenses to the gui list
                    self.expense_list.addItem(QListWidgetItem('Expenses for day ' + str(day) + ', month ' + str(month) + ':')) 
                    self.expense_list.addItem(QListWidgetItem(expenses_str))
                else:
                    #if no expenses clear expenses and write that there are not any
                    self.expense_list.clear()
                    self.expense_list.addItem(QListWidgetItem('No expenses for day ' + str(day) + ', month ' + str(month)))


         #this is like before but visually and it only shows expenses, you can NOT add it.   
    def view_calendar(self):
        if self.is_logged_in:
            calendar_dialog = CalendarDialog(self) 
            if calendar_dialog.exec_() == QDialog.Accepted:
                selected_date = calendar_dialog.calendar.selectedDate()
                day = selected_date.day()
                month = selected_date.month()
                expenses = self.expenses.get(month, {}).get(day, [])
                expenses_str = "\n".join(["$"+str(e) for e in expenses])
                if expenses_str:
                    self.expense_list.clear()
                    self.expense_list.addItem(QListWidgetItem('Expenses for day ' + str(day) + ', month ' + str(month) + ':'))
                    self.expense_list.addItem(QListWidgetItem(expenses_str))
                else:
                    self.expense_list.clear()
                    self.expense_list.addItem(QListWidgetItem('No expenses for day ' + str(day) + ', month ' + str(month)))

    def save_state(self): #saves data
        with open('budget_app_data.pickle', 'wb') as f: #opens a file to store data
            pickle.dump((self.credentials, self.expenses, self.budget), f) #dumps the credentials, expenses and budget into that file.


    #restores the saved data and if there is no data to begin with it passes, does nothing.
    def load_state(self):
        try:
            with open('budget_app_data.pickle', 'rb') as f:
                self.credentials, self.expenses, self.budget = pickle.load(f)
        except FileNotFoundError:
            pass

    def closeEvent(self, event):
        self.save_state() #saves the data to the ifle
        event.accept() #allows the window to close
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    budget_app = BudgetApp()
    budget_app.show()
    sys.exit(app.exec_())
