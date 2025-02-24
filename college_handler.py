import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries
from program_handler import list_programs

def add_college(college_data):
    add_entry('College.csv', college_data)

def delete_college(college_code):
    programs = list_programs()
    if college_code in programs['College'].values:
        raise Exception("Cannot delete college: Programs are associated with this college.")
    delete_entry('College.csv', 'Code', college_code)

def update_college(college_code, updated_data):
    update_entry('College.csv', 'Code', college_code, updated_data)

def list_colleges():
    return list_entries('College.csv')