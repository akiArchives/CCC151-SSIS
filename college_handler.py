import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries
from program_handler import list_programs, update_program_college_code

def add_college(college_data):
    add_entry('College.csv', college_data)

def delete_college(college_code):
    programs = list_programs()
    if college_code in programs['College'].values:
        raise Exception("Cannot delete college: Programs are associated with this college.")
    delete_entry('College.csv', 'Code', college_code)

def update_college(college_code, updated_data):
    # Get the old college code before updating
    colleges = list_colleges()
    old_code = college_code
    
    # Update the college in the College.csv
    update_entry('College.csv', 'Code', college_code, updated_data)
    
    # If the college code is being changed, update the programs' college codes
    if 'Code' in updated_data and updated_data['Code'] != old_code:
        new_code = updated_data['Code']
        update_program_college_code(old_code, new_code)

def list_colleges():
    return list_entries('College.csv')