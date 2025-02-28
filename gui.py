import sys
import pandas as pd
import re
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QDialog, QFormLayout, QMessageBox, QComboBox, QTabWidget, QHeaderView
)

from csv_handler import ensure_csv_files_exist, read_csv
from student_handler import *
from program_handler import *
from college_handler import *



class AddEditStudentDialog(QDialog):
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student" if not student_data else "Edit Student")
        self.setWindowIcon(QIcon("icons/studentWindowIcon.png"))
        self.student_data = student_data
 
        self.setFixedSize(300, 240)

        layout = QFormLayout(self)

        self.id_number = QLineEdit()
        self.id_number.setObjectName("idNumber")

        self.first_name = QLineEdit()
        self.first_name.setObjectName("firstName")

        self.last_name = QLineEdit()
        self.last_name.setObjectName("lastName")

        self.year_level = QComboBox()
        self.year_level.setObjectName("yearLevel")
        self.year_level.addItems(["1", "2", "3", "4"])  # Only valid year levels

        self.gender = QComboBox()
        self.gender.setObjectName("gender")
        self.gender.addItems(["Male", "Female", "Other"])

        self.program_code = QComboBox()  # Change to QComboBox
        self.program_code.setObjectName("programCode")
        self.program_code.setEditable(True)  # Allow typing and searching

        # Populate Program Code dropdown with valid codes from Program.csv
        try:
            programs = list_programs()
            self.program_code.addItems(programs['Code'].tolist())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load programs: {e}")

        layout.addRow("ID Number:", self.id_number)
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Year Level:", self.year_level)
        layout.addRow("Gender:", self.gender)
        layout.addRow("Program Code:", self.program_code)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        self.save_button.setObjectName("saveButton")
        self.save_button.setMinimumHeight(33)
        self.save_button.clicked.connect(self.save_student)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add a spacer item to push the button to the right
        button_layout.addWidget(self.save_button)
        layout.addRow(button_layout)

        if student_data:
            self.id_number.setText(student_data['ID Number'])
            self.first_name.setText(student_data['First Name'])
            self.last_name.setText(student_data['Last Name'])
            self.year_level.setCurrentText(student_data['Year Level'])
            self.gender.setCurrentText(student_data['Gender'])
            self.program_code.setCurrentText(student_data['Program Code'])
    
        else:
            self.id_number.setPlaceholderText("YYYY-NNNN")
            self.first_name.setPlaceholderText("John")
            self.last_name.setPlaceholderText("Doe")
            self.program_code.setPlaceholderText("BSCS")

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
            if not re.match(r"^[A-Za-z\- ]{2,10}$", program_code):
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
                save_confirmation = QMessageBox.question(
                    self, "Edit Student", "Are you sure you want to edit the selected student?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if save_confirmation == QMessageBox.StandardButton.Yes:
                    # Check for duplicate ID if the ID number was changed
                    if id_number != self.student_data['ID Number']:
                        students = list_students()
                        if id_number in students['ID Number'].values:
                            QMessageBox.warning(self, "Duplicate ID", "A student with this ID Number already exists.")
                            return
                    update_student(self.student_data['ID Number'], student_data)
            else:
                save_confirmation = QMessageBox.question(
                    self, "Add Student", "Are you sure you want to add this student?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if save_confirmation == QMessageBox.StandardButton.Yes:
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
        self.setWindowIcon(QIcon("icons/programWindowIcon.png"))
        self.program_data = program_data
 
        self.setFixedSize(550, 140)

        layout = QFormLayout(self)

        self.code = QLineEdit()
        self.code.setObjectName("programCodeLine")

        self.name = QLineEdit()
        self.name.setObjectName("programNameLine")

        self.college = QComboBox()
        self.college.setObjectName("collegeCodeCombo")
        self.college.setFixedWidth(75)

        # Populate College dropdown with valid codes from College.csv
        try:
            colleges = list_colleges()
            self.college.addItems(colleges['Code'].tolist())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load colleges: {e}")

        layout.addRow("Program code:", self.code)
        layout.addRow("Name:", self.name)
        layout.addRow("College:", self.college)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        self.save_button.setObjectName("saveButton")
        self.save_button.setMinimumHeight(33)
        self.save_button.clicked.connect(self.save_program)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add a spacer item to push the button to the right
        button_layout.addWidget(self.save_button)
        layout.addRow(button_layout)

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
            if not re.match(r"^[A-Za-z\- ]{2,10}$", code):
                QMessageBox.warning(self, "Invalid Program Code", "Program Code must be 2-10 characters long and can include uppercase, lowercase letters, and '-' (e.g., BSCS).")
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
            
            # Check if Program Code and Name already exists
            programs = list_programs()
            if code in programs['Code'].values and (not self.program_data or self.program_data['Code'] != code):
                QMessageBox.warning(self, "Duplicate Code", f"A program with the Code '{code}' already exists.")
                return
            if name in programs['Name'].values and (not self.program_data or self.program_data['Name'] != name):
                QMessageBox.warning(self, "Duplicate Name", f"A program with the Name '{name}' already exists.")
                return

            # Prepare program data
            program_data = {
                'Code': code,
                'Name': name,
                'College': college
            }

            # Add or update program
            if self.program_data:
                save_confirmation = QMessageBox.question(
                    self, "Edit Program", "Are you sure you want to edit the selected program?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if save_confirmation == QMessageBox.StandardButton.Yes:
                    old_code = self.program_data['Code']
                    update_program(old_code, program_data)
                    if old_code != code:
                        update_student_program_code(old_code, code)
                    
            else:
                save_confirmation = QMessageBox.question(
                    self, "Add Program", "Are you sure you want to add this program?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if save_confirmation == QMessageBox.StandardButton.Yes:
                    # Check if Code already exists
                    programs = list_programs()
                    if code in programs['Code'].values:
                        QMessageBox.warning(self, "Duplicate Code", "A program with this Code already exists.")
                        return
                    if name in programs['Name'].values:
                        QMessageBox.warning(self, "Duplicate Name", "A program with this Name already exists.")
                        return
                    add_program(program_data)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class AddEditCollegeDialog(QDialog):
    def __init__(self, parent=None, college_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add College" if not college_data else "Edit College")
        self.setWindowIcon(QIcon("icons/collegeWindowIcon.png"))
        self.college_data = college_data

        layout = QFormLayout(self)

        self.setFixedSize(350,110)

        self.code = QLineEdit()
        self.code.setObjectName("collegeCodeLine")

        self.name = QLineEdit()
        self.name.setObjectName("collegeNameLine")

        layout.addRow("Code:", self.code)
        layout.addRow("Name:", self.name)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        self.save_button.setObjectName("saveButton")
        self.save_button.setMinimumHeight(33)
        self.save_button.clicked.connect(self.save_college)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add a spacer item to push the button to the right
        button_layout.addWidget(self.save_button)
        layout.addRow(button_layout)

        if college_data:
            self.code.setText(college_data['Code'])
            self.name.setText(college_data['Name'])

        def convert_to_uppercase(self):
            self.code.setText(self.code.text().upper())

    def save_college(self):
        try:
            # Get input values
            code = self.code.text().strip()
            name = self.name.text().strip()

            # Validate College Code format (all letters, no numbers)
            if not re.match(r"^[A-Za-z]+$", code):
                QMessageBox.warning(self, "Invalid College Code", "College Code must consist of all letters and no numbers.")
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
                old_code = self.college_data['Code']
                if old_code != code:
                    # Check if new Code already exists
                    colleges = list_colleges()
                    if code in colleges['Code'].values:
                        QMessageBox.warning(self, "Duplicate Code", "A college with this Code already exists.")
                        return
                    update_college(old_code, college_data)
                    update_program_college_code(old_code, code)
                else:
                    update_college(old_code, college_data)

            else:
                # Check if Code already exists
                colleges = list_colleges()
                if code in colleges['Code'].values:
                    QMessageBox.warning(self, "Duplicate Code", "A college with this Code already exists.")
                    return
                if name in colleges['Name'].values:
                    QMessageBox.warning(self, "Duplicate Name", "A college with this Name already exists.")
                    return
                add_college(college_data)



            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


class StudentInformationSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Information System")
        self.setWindowIcon(QIcon("icons/windowIcon.png"))
        self.setGeometry(100, 100, 900, 600)

        # Initialize CSV files
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

        # Add shortcut for unselecting rows
        self.add_shortcuts()

    def add_shortcuts(self):
        self.escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.escape_shortcut.activated.connect(self.unselect_all_rows)

    def unselect_all_rows(self):
        self.student_table.clearSelection()
        self.program_table.clearSelection()
        self.college_table.clearSelection()

    def init_student_tab(self):
        layout = QVBoxLayout(self.student_tab)

        # Search bar and Clear Search button
        search_layout = QHBoxLayout()
        self.student_search_bar = QLineEdit()
        self.student_search_bar.setObjectName("studentSearchBar")
        self.student_search_bar.setPlaceholderText("Search by ID, Name, or Program Code")
        self.student_search_bar.textChanged.connect(self.filter_student_table)
        self.student_search_bar.returnPressed.connect(self.filter_student_table)  # Run search on Enter key press

        self.search_by_label = QComboBox()
        self.search_by_label.setObjectName("searchByLabel")
        self.search_by_label.addItems(["All", "ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"])

        self.clear_student_search_button = QPushButton("")
        self.clear_student_search_button.setMinimumHeight(50)
        self.clear_student_search_button.setMinimumWidth(50)
        self.clear_student_search_button.setIcon(QIcon("icons/clear.png"))
        self.clear_student_search_button.setIconSize(QSize(50,50))
        self.clear_student_search_button.setObjectName("clearStudentSearchButton")
        self.clear_student_search_button.clicked.connect(self.clear_student_search)

        search_layout.addWidget(self.student_search_bar)
        search_layout.addWidget(self.search_by_label)
        search_layout.addWidget(self.clear_student_search_button)
        layout.addLayout(search_layout)

        # Table to display students
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'])
        self.student_table.setSortingEnabled(True)  # Enable sorting
        self.student_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        self.student_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)  # Allow multiple selection
        self.student_table.horizontalHeader().setStretchLastSection(True)  # Stretch last section to fit window
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Resize columns to fit window
        self.student_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Disable cell editing
        self.student_table.verticalHeader().setVisible(False)  # Hide row numbers
        layout.addWidget(self.student_table)

        # Buttons for CRUD operations
        self.student_button_layout = QHBoxLayout()

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.setObjectName("addStudentButton")
        self.add_student_button.setIcon(QIcon("icons/add.png"))
        self.add_student_button.setIconSize(QSize(16, 16))
        self.add_student_button.clicked.connect(self.open_add_student_dialog)

        self.edit_student_button = QPushButton("Edit Student")
        self.edit_student_button.setObjectName("editStudentButton")
        self.edit_student_button.clicked.connect(self.open_edit_student_dialog)
        self.edit_student_button.setIcon(QIcon("icons/edit.png"))

        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.setObjectName("deleteStudentButton")
        self.delete_student_button.clicked.connect(self.delete_students)
        self.delete_student_button.setIcon(QIcon("icons/delete.png"))
        
        self.refresh_student_button = QPushButton("Refresh List")
        self.refresh_student_button.setObjectName("refreshStudentButton")
        self.refresh_student_button.clicked.connect(self.refresh_student_table)
        self.refresh_student_button.setIcon(QIcon("icons/refresh.png"))

        self.student_button_layout.addWidget(self.add_student_button)
        self.student_button_layout.addWidget(self.edit_student_button)
        self.student_button_layout.addWidget(self.delete_student_button)
        self.student_button_layout.addWidget(self.refresh_student_button)
        layout.addLayout(self.student_button_layout)

        self.refresh_student_table()

    def init_program_tab(self):
        layout = QVBoxLayout(self.program_tab)

        # Search bar and Clear Search button
        search_layout = QHBoxLayout()
        self.program_search_bar = QLineEdit()
        self.program_search_bar.setObjectName("programSearchBar")
        self.program_search_bar.setPlaceholderText("Search by Code or Name")
        self.program_search_bar.textChanged.connect(self.filter_program_table)
        self.program_search_bar.returnPressed.connect(self.filter_program_table)  # Run search on Enter key press

        self.clear_program_search_button = QPushButton("")
        self.clear_program_search_button.setMinimumHeight(50)
        self.clear_program_search_button.setMinimumWidth(50)
        self.clear_program_search_button.setIcon(QIcon("icons/clear.png"))
        self.clear_program_search_button.setIconSize(QSize(50,50))
        self.clear_program_search_button.setObjectName("clearProgramSearchButton")
        self.clear_program_search_button.clicked.connect(self.clear_program_search)

        search_layout.addWidget(self.program_search_bar)
        search_layout.addWidget(self.clear_program_search_button)
        layout.addLayout(search_layout)

        # Table to display programs
        self.program_table = QTableWidget()
        self.program_table.setColumnCount(3)
        self.program_table.setHorizontalHeaderLabels(['Code', 'Name', 'College'])
        self.program_table.setSortingEnabled(True)  # Enable sorting
        self.program_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        self.program_table.horizontalHeader().setStretchLastSection(True)  # Stretch last section to fit window
        self.program_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Resize columns to fit window
        self.program_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Disable cell editing
        self.program_table.verticalHeader().setVisible(False)  # Hide row numbers
        layout.addWidget(self.program_table)

        # Buttons for CRUD operations
        self.program_button_layout = QHBoxLayout()
        self.add_program_button = QPushButton("Add Program")
        self.add_program_button.setObjectName("addProgramButton")
        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.add_program_button.setIcon(QIcon("icons/add.png"))
        self.add_program_button.setIconSize(QSize(16, 16))

        self.edit_program_button = QPushButton("Edit Program")
        self.edit_program_button.setObjectName("editProgramButton")
        self.edit_program_button.clicked.connect(self.open_edit_program_dialog)
        self.edit_program_button.setIcon(QIcon("icons/edit.png"))

        self.delete_program_button = QPushButton("Delete Program")
        self.delete_program_button.setObjectName("deleteProgramButton")
        self.delete_program_button.clicked.connect(self.delete_program)
        self.delete_program_button.setIcon(QIcon("icons/delete.png"))

        self.refresh_program_button = QPushButton("Refresh List")
        self.refresh_program_button.setObjectName("refreshProgramButton")
        self.refresh_program_button.clicked.connect(self.refresh_program_table)
        self.refresh_program_button.setIcon(QIcon("icons/refresh.png"))

        self.program_button_layout.addWidget(self.add_program_button)
        self.program_button_layout.addWidget(self.edit_program_button)
        self.program_button_layout.addWidget(self.delete_program_button)
        self.program_button_layout.addWidget(self.refresh_program_button)
        layout.addLayout(self.program_button_layout)

        self.refresh_program_table()

    def init_college_tab(self):
        layout = QVBoxLayout(self.college_tab)

        # Search bar and Clear Search button
        search_layout = QHBoxLayout()
        self.college_search_bar = QLineEdit()
        self.college_search_bar.setObjectName("collegeSearchBar")
        self.college_search_bar.setPlaceholderText("Search by Code or Name")
        self.college_search_bar.textChanged.connect(self.filter_college_table)
        self.college_search_bar.returnPressed.connect(self.filter_college_table)  # Run search on Enter key press

        self.clear_college_search_button = QPushButton("")
        self.clear_college_search_button.setMinimumHeight(50)
        self.clear_college_search_button.setMinimumWidth(50)
        self.clear_college_search_button.setIcon(QIcon("icons/clear.png"))
        self.clear_college_search_button.setIconSize(QSize(50,50))
        self.clear_college_search_button.setObjectName("clearCollegeSearchButton")
        self.clear_college_search_button.clicked.connect(self.clear_college_search)

        search_layout.addWidget(self.college_search_bar)
        search_layout.addWidget(self.clear_college_search_button)
        layout.addLayout(search_layout)

        # Table to display colleges
        self.college_table = QTableWidget()
        self.college_table.setColumnCount(2)
        self.college_table.setHorizontalHeaderLabels(['Code', 'Name'])
        self.college_table.setSortingEnabled(True)  # Enable sorting
        self.college_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire row
        self.college_table.horizontalHeader().setStretchLastSection(True)  # Stretch last section to fit window
        self.college_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Resize columns to fit window
        self.college_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Disable cell editing
        self.college_table.verticalHeader().setVisible(False)  # Hide row numbers
        layout.addWidget(self.college_table)

        # Buttons for CRUD operations
        self.college_button_layout = QHBoxLayout()
        self.add_college_button = QPushButton("Add College")
        self.add_college_button.setObjectName("addCollegeButton")
        self.add_college_button.clicked.connect(self.open_add_college_dialog)
        self.add_college_button.setIcon(QIcon("icons/add.png"))  # Fix icon assignment
        self.add_college_button.setIconSize(QSize(16, 16))

        self.edit_college_button = QPushButton("Edit College")
        self.edit_college_button.setObjectName("editCollegeButton")
        self.edit_college_button.clicked.connect(self.open_edit_college_dialog)
        self.edit_college_button.setIcon(QIcon("icons/edit.png"))

        self.delete_college_button = QPushButton("Delete College")
        self.delete_college_button.setObjectName("deleteCollegeButton")
        self.delete_college_button.clicked.connect(self.delete_college)
        self.delete_college_button.setIcon(QIcon("icons/delete.png"))

        self.refresh_college_button = QPushButton("Refresh List")
        self.refresh_college_button.setObjectName("refreshCollegeButton")
        self.refresh_college_button.clicked.connect(self.refresh_college_table)
        self.refresh_college_button.setIcon(QIcon("icons/refresh.png"))

        self.college_button_layout.addWidget(self.add_college_button)
        self.college_button_layout.addWidget(self.edit_college_button)
        self.college_button_layout.addWidget(self.delete_college_button)
        self.college_button_layout.addWidget(self.refresh_college_button)
        layout.addLayout(self.college_button_layout)

        self.refresh_college_table()

    def delete_confirm(self, message):
        return QMessageBox.question(
            self, f"Delete {message}", f"Are you sure you want to delete the selected {message}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

    def delete_students(self):
        selected_rows = self.student_table.selectionModel().selectedRows()
        delete_confirmation = self.delete_confirm("students")
        if delete_confirmation == QMessageBox.StandardButton.Yes and selected_rows:
            try:
                for index in sorted(selected_rows, reverse=True):
                    student_id = self.student_table.item(index.row(), 0).text()
                    delete_student(student_id)
                self.refresh_student_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete students: {e}")

    def delete_program(self):
        selected_row = self.program_table.currentRow()
        delete_confirmation = self.delete_confirm("program")
        if delete_confirmation == QMessageBox.StandardButton.Yes and selected_row >= 0:
            try:
                program_code = self.program_table.item(selected_row, 0).text()
                delete_program(program_code)
                self.refresh_program_table()
                self.refresh_student_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete program: {e}")

    def delete_college(self):
        selected_row = self.college_table.currentRow()
        delete_confirmation = self.delete_confirm("college")
        if delete_confirmation == QMessageBox.StandardButton.Yes and selected_row >= 0:
            try:
                college_code = self.college_table.item(selected_row, 0).text()
                delete_college(college_code)
                self.refresh_college_table()
                self.refresh_program_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete college: {e}")

    def refresh_table(self, table_widget, list_function, search_bar, column_alignments=None):
        try:
            # Disable sorting before refreshing (fixed a bug)
            table_widget.setSortingEnabled(False)

            # Clear the table
            table_widget.setRowCount(0)  # Remove all rows

            # Fetch data
            data = list_function()

            # Set the number of columns and headers
            table_widget.setColumnCount(len(data.columns))
            table_widget.setHorizontalHeaderLabels(data.columns)

            # Populate the table with data
            for _, row in data.iterrows():
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    if column_alignments and col_index in column_alignments:
                        item.setTextAlignment(column_alignments[col_index])
                    table_widget.setItem(row_position, col_index, item)

            # Resize columns to fit contents
            table_widget.resizeColumnsToContents()

            # Allow columns to stretch to fit the window
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Reapply the search filter
            self.filter_table(table_widget, search_bar, self.search_by_label)

            # Re-enable sorting after refreshing
            table_widget.setSortingEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh table: {e}")

    def refresh_student_table(self):
        self.refresh_table(
            self.student_table,
            list_students,
            self.student_search_bar,
            column_alignments={0: Qt.AlignmentFlag.AlignCenter, 3: Qt.AlignmentFlag.AlignCenter, 4: Qt.AlignmentFlag.AlignCenter}
        )

    def refresh_program_table(self):
        self.refresh_table(
            self.program_table,
            list_programs,
            self.program_search_bar,
            column_alignments={0: Qt.AlignmentFlag.AlignCenter, 2: Qt.AlignmentFlag.AlignCenter}
        )

    def refresh_college_table(self):
        self.refresh_table(
            self.college_table,
            list_colleges,
            self.college_search_bar,
            column_alignments={0: Qt.AlignmentFlag.AlignCenter}
        )

    def filter_table(self, table_widget, search_bar, search_by_combo):
        search_text = search_bar.text().lower()
        search_by = search_by_combo.currentText().lower()

        for row in range(table_widget.rowCount()):
            match = False
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item:
                    header_text = table_widget.horizontalHeaderItem(col).text().lower()
                    if search_by == "gender" and header_text == "gender":
                        if search_text in item.text().lower():
                            match = True
                            break
                    elif search_by == "all" or header_text == search_by:
                        if search_text in item.text().lower():
                            match = True
                            break
            table_widget.setRowHidden(row, not match)

    def filter_student_table(self):
        self.filter_table(self.student_table, self.student_search_bar, self.search_by_label)

    def filter_program_table(self):
        self.filter_table(self.program_table, self.program_search_bar, self.search_by_label)

    def filter_college_table(self):
        self.filter_table(self.college_table, self.college_search_bar, self.search_by_label)

    def clear_student_search(self):
        self.student_search_bar.clear()
        self.search_by_label.setCurrentIndex(0)  
        self.filter_student_table()

    def clear_program_search(self):
        self.program_search_bar.clear()
        self.search_by_label.setCurrentIndex(0)  
        self.filter_program_table()

    def clear_college_search(self):
        self.college_search_bar.clear()
        self.search_by_label.setCurrentIndex(0)
        self.filter_college_table()

    def open_add_student_dialog(self):
        dialog = AddEditStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_student_table()
            self.student_table.resizeColumnsToContents()  # Ensure columns are resized after adding a student
            self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Ensure columns fit window
            
    def open_edit_student_dialog(self):
        selected_rows = self.student_table.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0].row()
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
        else:
            QMessageBox.warning(self, "No Selection", "Please select a student to edit.")

    def open_add_program_dialog(self):
        dialog = AddEditProgramDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_program_table()     
            
    def open_edit_program_dialog(self):
        selected_rows = self.program_table.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0].row()
            try:
                program_data = {
                    'Code': self.program_table.item(selected_row, 0).text(),
                    'Name': self.program_table.item(selected_row, 1).text(),
                    'College': self.program_table.item(selected_row, 2).text()
                }
                dialog = AddEditProgramDialog(self, program_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_program_table()
                    self.refresh_student_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit program: {e}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a program to edit.")        
                
    
                            
    def open_add_college_dialog(self):
        dialog = AddEditCollegeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_college_table()             
                
    def open_edit_college_dialog(self):
        selected_rows = self.college_table.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0].row()
            try:
                college_data = {
                    'Code': self.college_table.item(selected_row, 0).text(),
                    'Name': self.college_table.item(selected_row, 1).text()
                }
                dialog = AddEditCollegeDialog(self, college_data)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.refresh_college_table()
                    self.refresh_program_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit college: {e}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a college to edit.")             
                        

def load_stylesheet(filename):
    """Load a CSS stylesheet from a file."""
    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("style.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = StudentInformationSystem()
    window.show()
    sys.exit(app.exec())