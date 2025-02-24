import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries
from student_handler import list_students

def add_program(program_data):
    add_entry('Program.csv', program_data)

def delete_program(program_code):
    students = list_students()
    if program_code in students['Program Code'].values:
        raise Exception("Cannot delete program: Students are associated with this program.")
    delete_entry('Program.csv', 'Code', program_code)

def update_program(program_code, updated_data):
    update_entry('Program.csv', 'Code', program_code, updated_data)

def list_programs():
    return list_entries('Program.csv')