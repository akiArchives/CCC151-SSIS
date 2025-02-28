import os
import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries, write_csv


def add_student(student_data):
    add_entry('Student.csv', student_data)

def delete_student(student_id):
    delete_entry('Student.csv', 'ID Number', student_id)

def update_student(student_id, updated_data):
    update_entry('Student.csv', 'ID Number', student_id, updated_data)

def list_students():
    return list_entries('Student.csv')

def update_student_program_code(old_code, new_code):
    students = list_students()
    students.loc[students['Program Code'] == old_code, 'Program Code'] = new_code
    write_csv('Student.csv', students)