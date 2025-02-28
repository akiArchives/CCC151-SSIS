import pandas as pd
from csv_handler import add_entry, delete_entry, update_entry, list_entries, write_csv
from student_handler import list_students, update_student_program_code



def add_program(program_data):
    add_entry('Program.csv', program_data)

def delete_program(program_code):
    students = list_students()
    if program_code in students['Program Code'].values:
        raise Exception("Cannot delete program: Students are associated with this program.")
    delete_entry('Program.csv', 'Code', program_code)

def update_program(program_code, updated_data):
    #Get the old program code before updating
    programs = list_programs()
    old_code = program_code
    
    # Update the program in the Program.csv
    update_entry('Program.csv', 'Code', program_code, updated_data)
    
    # If the program code is being changed, update the students' program codes
    if 'Code' in updated_data and updated_data['Code'] != old_code:
        new_code = updated_data['Code']
        update_student_program_code(old_code, new_code)

def list_programs():
    return list_entries('Program.csv')

def update_program_college_code(old_code, new_code):
    programs = list_programs()
    programs.loc[programs['College'] == old_code, 'College'] = new_code
    write_csv('Program.csv', programs)  # Use write_csv to save changes to the CSV file