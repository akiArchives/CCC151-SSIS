import sys
import pandas as pd
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QDialog, QFormLayout, QMessageBox, QComboBox, QTabWidget
)
from csv_handler import ensure_csv_files_exist, read_csv
from student_handler import add_student, delete_student, update_student, list_students
from program_handler import add_program, delete_program, update_program, list_programs
from college_handler import add_college, delete_college, update_college, list_colleges


class AddEditStudentDialog(QDialog):
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student" if not student_data else "Edit Student")
        self.student_data = student_data

        layout = QFormLayout(self)

        self.id_number = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.year_level = QComboBox()
        self.year_level.addItems(["1", "2", "3", "4"])  # Only valid year levels
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        self.program_code = QComboBox()  # Change to QComboBox
        self.program_code.setEditable(True)  # Allow typing and searching

        # Populate Program Code dropdown with valid codes from Program.csv
        try:
            programs = list_programs()
            self.program_code.addItems(programs['Code'].tolist())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load programs: {e}")

        layout.addRow("ID Number (YYYY-NNNN):", self.id_number)
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Year Level:", self.year_level)
        layout.addRow("Gender:", self.gender)
        layout.addRow("Program Code (e.g., BSCS, BSIT):", self.program_code)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_student)
        layout.addRow(self.save_button)

        if student_data:
            self.id_number.setText(student_data['ID Number'])
            self.first_name.setText(student_data['First Name'])
            self.last_name.setText(student_data['Last Name'])
            self.year_level.setCurrentText(student_data['Year Level'])
            self.gender.setCurrentText(student_data['Gender'])
            self.program_code.setCurrentText(student_data['Program Code'])

    def save_student(self):
        try:
            # Get input values
            id_number = self.id_number.text().strip()
            first_name = self.first_name.text().strip()
            last_name = self.last_name.text().strip()
            year_level = self.year_level.currentText()
            gender = self.gender.currentText()
            program_code = self.program_code.currentText().strip()  # Get the current text from the combo box

            # Validate ID Number format (YYYY-NNNN)
            if not re.match(r"^\d{4}-\d{4}$", id_number):
                QMessageBox.warning(self, "Invalid ID Number", "ID Number must be in the format YYYY-NNNN.")
                return

            # Validate Program Code format (uppercase, lowercase, and '-')
            if not re.match(r"^[A-Za-z\-]{2,10}$", program_code):
                QMessageBox.warning(self, "Invalid Program Code", "Program Code must be 2-10 characters long and can include uppercase, lowercase letters, and '-' (e.g., BSCS, bs-it).")
                return

            # Validate Year Level (must be 1, 2, 3, or 4)
            if year_level not in ["1", "2", "3", "4"]:
                QMessageBox.warning(self, "Invalid Year Level", "Year Level must be 1, 2, 3, or 4.")
                return

            # Validate empty fields
            if not all([id_number, first_name, last_name, program_code]):
                QMessageBox.warning(self, "Empty Fields", "All fields are required.")
                return

            # Foreign Key Validation: Check if Program Code exists in Program.csv
            programs = list_programs()
            if program_code not in programs['Code'].values:
                QMessageBox.warning(self, "Invalid Program Code", f"Program Code '{program_code}' does not exist in the Programs table.")
                return

            # Prepare student data
            student_data = {
                'ID Number': id_number,
                'First Name': first_name,
                'Last Name': last_name,
                'Year Level': year_level,
                'Gender': gender,
                'Program Code': program_code
            }

            # Add or update student
            if self.student_data:
                update_student(self.student_data['ID Number'], student_data)
            else:
                # Check if ID Number already exists
                students = list_students()
                if id_number in students['ID Number'].values:
                    QMessageBox.warning(self, "Duplicate ID", "A student with this ID Number already exists.")
                    return
                add_student(student_data)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class AddEditProgramDialog(QDialog):
    def __init__(self, parent=None, program_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Program" if not program_data else "Edit Program")
        self.program_data = program_data

        layout = QFormLayout(self)

        self.code = QLineEdit()
        self.name = QLineEdit()
        self.college = QComboBox()  # Change to QComboBox for better user experience

        # Populate College Code dropdown with valid codes
        valid_college_codes = ["CCS", "COE", "CASS", "CED", "CSM", "CEBA"]
        self.college.addItems(valid_college_codes)

        layout.addRow("Code (e.g., BSCS, BSIT):", self.code)
        layout.addRow("Name:", self.name)
        layout.addRow("College:", self.college)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_program)
        layout.addRow(self.save_button)

        if program_data:
            self.code.setText(program_data['Code'])
            self.name.setText(program_data['Name'])
            self.college.setCurrentText(program_data['College'])

    def save_program(self):
        try:
            # Get input values
            code = self.code.text().strip()
            name = self.name.text().strip()
            college = self.college.currentText().strip()

            # Validate Program Code format (uppercase, lowercase, and '-')
            if not re.match(r"^[A-Za-z\-]{2,10}$", code):
                QMessageBox.warning(self, "Invalid Program Code", "Program Code must be 2-10 characters long and can include uppercase, lowercase letters, and '-' (e.g., BSCS, bs-it).")
                return

            # Validate empty fields
            if not all([code, name, college]):
                QMessageBox.warning(self, "Empty Fields", "All fields are required.")
                return

            # Foreign Key Validation: Check if College Code exists in College.csv
            colleges = list_colleges()
            if college not in colleges['Code'].values:
                QMessageBox.warning(self, "Invalid College Code", f"College Code '{college}' does not exist in the Colleges table.")
                return

            # Prepare program data
            program_data = {
                'Code': code,
                'Name': name,
                'College': college
            }

            # Add or update program
            if self.program_data:
                update_program(self.program_data['Code'], program_data)
            else:
                # Check if Code already exists
                programs = list_programs()
                if code in programs['Code'].values:
                    QMessageBox.warning(self, "Duplicate Code", "A program with this Code already exists.")
                    return
                add_program(program_data)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class AddEditCollegeDialog(QDialog):
    def __init__(self, parent=None, college_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add College" if not college_data else "Edit College")
        self.college_data = college_data

        layout = QFormLayout(self)

        self.code = QLineEdit()
        self.name = QLineEdit()

        layout.addRow("Code (e.g., CCS, COE, CASS, CED, CSM, CEBA):", self.code)
        layout.addRow("Name:", self.name)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_college)
        layout.addRow(self.save_button)

        if college_data:
            self.code.setText(college_data['Code'])
            self.name.setText(college_data['Name'])

    def save_college(self):
        try:
            # Get input values
            code = self.code.text().strip()
            name = self.name.text().strip()

            # Validate College Code format (e.g., CCS, COE, CASS, CED, CSM, CEBA)
            valid_college_codes = ["CCS", "COE", "CASS", "CED", "CSM", "CEBA"]
            if code not in valid_college_codes:
                QMessageBox.warning(self, "Invalid College Code", f"College Code must be one of: {', '.join(valid_college_codes)}.")
                return

            # Validate empty fields
            if not all([code, name]):
                QMessageBox.warning(self, "Empty Fields", "All fields are required.")
                return

            # Prepare college data
            college_data = {
                'Code': code,
                'Name': name
            }

            # Add or update college
            if self.college_data:
                update_college(self.college_data['Code'], college_data)
            else:
                # Check if Code already exists
                colleges = list_colleges()
                if code in colleges['Code'].values:
                    QMessageBox.warning(self, "Duplicate Code", "A college with this Code already exists.")
                    return
                add_college(college_data)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


class StudentInformationSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setGeometry(100, 100, 800, 600)
        try:
            ensure_csv_files_exist()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize CSV files: {e}")
            sys.exit(1)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Create tabs
        self.tabs = QTabWidget()
        self.student_tab = QWidget()
        self.program_tab = QWidget()
        self.college_tab = QWidget()

        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.program_tab, "Programs")
        self.tabs.addTab(self.college_tab, "Colleges")

        self.layout.addWidget(self.tabs)

        # Initialize tabs
        self.init_student_tab()
        self.init_program_tab()
        self.init_college_tab()

    def init_student_tab(self):
        layout = QVBoxLayout(self.student_tab)

        # Search bar
        self.student_search_bar = QLineEdit()
        self.student_search_bar.setPlaceholderText("Search by ID, Name, or Program Code")
        self.student_search_bar.textChanged.connect(self.filter_student_table)
        layout.addWidget(self.student_search_bar)

        # Table to display students
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'])
        self.student_table.setSortingEnabled(True)  # Enable sorting
        self.student_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        layout.addWidget(self.student_table)

        # Buttons for CRUD operations
        self.student_button_layout = QHBoxLayout()
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.edit_student_button = QPushButton("Edit Student")
        self.edit_student_button.clicked.connect(self.open_edit_student_dialog)
        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student)
        self.refresh_student_button = QPushButton("Refresh List")
        self.refresh_student_button.clicked.connect(self.refresh_student_table)

        self.student_button_layout.addWidget(self.add_student_button)
        self.student_button_layout.addWidget(self.edit_student_button)
        self.student_button_layout.addWidget(self.delete_student_button)
        self.student_button_layout.addWidget(self.refresh_student_button)
        layout.addLayout(self.student_button_layout)

        self.refresh_student_table()

    def init_program_tab(self):
        layout = QVBoxLayout(self.program_tab)

        # Search bar
        self.program_search_bar = QLineEdit()
        self.program_search_bar.setPlaceholderText("Search by Code or Name")
        self.program_search_bar.textChanged.connect(self.filter_program_table)
        layout.addWidget(self.program_search_bar)

        # Table to display programs
        self.program_table = QTableWidget()
        self.program_table.setColumnCount(3)
        self.program_table.setHorizontalHeaderLabels(['Code', 'Name', 'College'])
        self.program_table.setSortingEnabled(True)  # Enable sorting
        self.program_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        layout.addWidget(self.program_table)

        # Buttons for CRUD operations
        self.program_button_layout = QHBoxLayout()
        self.add_program_button = QPushButton("Add Program")
        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.edit_program_button = QPushButton("Edit Program")
        self.edit_program_button.clicked.connect(self.open_edit_program_dialog)
        self.delete_program_button = QPushButton("Delete Program")
        self.delete_program_button.clicked.connect(self.delete_program)
        self.refresh_program_button = QPushButton("Refresh List")
        self.refresh_program_button.clicked.connect(self.refresh_program_table)

        self.program_button_layout.addWidget(self.add_program_button)
        self.program_button_layout.addWidget(self.edit_program_button)
        self.program_button_layout.addWidget(self.delete_program_button)
        self.program_button_layout.addWidget(self.refresh_program_button)
        layout.addLayout(self.program_button_layout)

        self.refresh_program_table()

    def init_college_tab(self):
        layout = QVBoxLayout(self.college_tab)

        # Search bar
        self.college_search_bar = QLineEdit()
        self.college_search_bar.setPlaceholderText("Search by Code or Name")
        self.college_search_bar.textChanged.connect(self.filter_college_table)
        layout.addWidget(self.college_search_bar)

        # Table to display colleges
        self.college_table = QTableWidget()
        self.college_table.setColumnCount(2)
        self.college_table.setHorizontalHeaderLabels(['Code', 'Name'])
        self.college_table.setSortingEnabled(True)  # Enable sorting
        self.college_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        layout.addWidget(self.college_table)

        # Buttons for CRUD operations
        self.college_button_layout = QHBoxLayout()
        self.add_college_button = QPushButton("Add College")
        self.add_college_button.clicked.connect(self.open_add_college_dialog)
        self.edit_college_button = QPushButton("Edit College")
        self.edit_college_button.clicked.connect(self.open_edit_college_dialog)
        self.delete_college_button = QPushButton("Delete College")
        self.delete_college_button.clicked.connect(self.delete_college)
        self.refresh_college_button = QPushButton("Refresh List")
        self.refresh_college_button.clicked.connect(self.refresh_college_table)

        self.college_button_layout.addWidget(self.add_college_button)
        self.college_button_layout.addWidget(self.edit_college_button)
        self.college_button_layout.addWidget(self.delete_college_button)
        self.college_button_layout.addWidget(self.refresh_college_button)
        layout.addLayout(self.college_button_layout)

        self.refresh_college_table()

    def refresh_student_table(self):
        try:
            self.student_table.setRowCount(0)
            students = list_students()
            for _, row in students.iterrows():
                row_position = self.student_table.rowCount()
                self.student_table.insertRow(row_position)
                for col_index, value in enumerate(row):
                    self.student_table.setItem(row_position, col_index, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh student table: {e}")

    def refresh_program_table(self):
        try:
            self.program_table.setRowCount(0)
            programs = list_programs()
            for _, row in programs.iterrows():
                row_position = self.program_table.rowCount()
                self.program_table.insertRow(row_position)
                for col_index, value in enumerate(row):
                    self.program_table.setItem(row_position, col_index, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh program table: {e}")

    def refresh_college_table(self):
        try:
            self.college_table.setRowCount(0)
            colleges = list_colleges()
            for _, row in colleges.iterrows():
                row_position = self.college_table.rowCount()
                self.college_table.insertRow(row_position)
                for col_index, value in enumerate(row):
                    self.college_table.setItem(row_position, col_index, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh college table: {e}")

    def filter_student_table(self):
        search_text = self.student_search_bar.text().lower()
        for row in range(self.student_table.rowCount()):
            match = False
            for col in range(self.student_table.columnCount()):
                item = self.student_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.student_table.setRowHidden(row, not match)
            
    def open_add_student_dialog(self):
        dialog = AddEditStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_student_table()             
            
    def open_edit_student_dialog(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            try:
                student_data = {
                    'ID Number': self.student_table.item(selected_row, 0).text(),
                    'First Name': self.student_table.item(selected_row, 1).text(),
                    'Last Name': self.student_table.item(selected_row, 2).text(),
                    'Year Level': self.student_table.item(selected_row, 3).text(),
                    'Gender': self.student_table.item(selected_row, 4).text(),
                    'Program Code': self.student_table.item(selected_row, 5).text()
                }
                dialog = AddEditStudentDialog(self, student_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_student_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit student: {e}")

    def delete_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            try:
                student_id = self.student_table.item(selected_row, 0).text()
                delete_student(student_id)
                self.refresh_student_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete student: {e}")
        
    def filter_program_table(self):
            search_text = self.program_search_bar.text().lower()
            for row in range(self.program_table.rowCount()):
                match = False
                for col in range(self.program_table.columnCount()):
                    item = self.program_table.item(row, col)
                    if item and search_text in item.text().lower():
                        match = True
                        break
                self.program_table.setRowHidden(row, not match) 
            
    def open_add_program_dialog(self):
        dialog = AddEditProgramDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_program_table()     
            
    def open_edit_program_dialog(self):
        selected_row = self.program_table.currentRow()
        if selected_row >= 0:
            try:
                program_data = {
                    'Code': self.program_table.item(selected_row, 0).text(),
                    'Name': self.program_table.item(selected_row, 1).text(),
                    'College': self.program_table.item(selected_row, 2).text()
                }
                dialog = AddEditProgramDialog(self, program_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_program_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit program: {e}")        
                
    def delete_program(self):
        selected_row = self.program_table.currentRow()
        if selected_row >= 0:
            try:
                program_code = self.program_table.item(selected_row, 0).text()
                delete_program(program_code)
                self.refresh_program_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete program: {e}") 
                            
    def filter_college_table(self):
        search_text = self.college_search_bar.text().lower()
        for row in range(self.college_table.rowCount()):
            match = False
            for col in range(self.college_table.columnCount()):
                item = self.college_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.college_table.setRowHidden(row, not match)             
                
    def open_add_college_dialog(self):
        dialog = AddEditCollegeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_college_table()             
                
    def open_edit_college_dialog(self):
        selected_row = self.college_table.currentRow()
        if selected_row >= 0:
            try:
                college_data = {
                    'Code': self.college_table.item(selected_row, 0).text(),
                    'Name': self.college_table.item(selected_row, 1).text()
                }
                dialog = AddEditCollegeDialog(self, college_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_college_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit college: {e}")             
                
    def delete_college(self):
        selected_row = self.college_table.currentRow()
        if selected_row >= 0:
            try:
                college_code = self.college_table.item(selected_row, 0).text()
                delete_college(college_code)
                self.refresh_college_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete college: {e}")             


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentInformationSystem()
    window.show()
    sys.exit(app.exec())