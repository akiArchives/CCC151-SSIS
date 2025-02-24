# Simple Student Information System

## Overview
This project is a simple Student Information System that allows users to manage students, programs, and colleges. It provides a graphical user interface (GUI) built with PyQt6 and uses CSV files for data storage.

## Features
- Add, edit, delete, and list students
- Add, edit, delete, and list programs
- Add, edit, delete, and list colleges
- Search functionality for students, programs, and colleges
- Data validation and error handling

## Installation
1. Clone the repository or download the source code.
2. Ensure you have Python installed (version 3.6 or higher).
3. Install the required dependencies using pip:
    ```sh
    pip install pandas pyqt6
    ```

## Usage
1. Navigate to the project directory.
2. Run the `gui.py` file to start the application:
    ```sh
    python gui.py
    ```

## Project Structure
- `gui.py`: Main GUI application file.
- `student_handler.py`: Handles CRUD operations for students.
- `program_handler.py`: Handles CRUD operations for programs.
- `college_handler.py`: Handles CRUD operations for colleges.
- `csv_handler.py`: Utility functions for reading and writing CSV files.
- `csv-files/`: Directory where CSV files are stored.

## CSV Files
The application uses the following CSV files for data storage:
- `Student.csv`: Stores student information.
- `Program.csv`: Stores program information.
- `College.csv`: Stores college information.

