import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries

def add_student(student_data):
    add_entry('Student.csv', student_data)

def delete_student(student_id):
    delete_entry('Student.csv', 'ID Number', student_id)

def update_student(student_id, updated_data):
    update_entry('Student.csv', 'ID Number', student_id, updated_data)

def list_students():
    return list_entries('Student.csv')