import pandas as pd
from csv_handler import read_csv, write_csv
from student_handler import list_students

def add_program(program_data):
    try:
        df = read_csv('Program.csv')
        df = pd.concat([df, pd.DataFrame([program_data])], ignore_index=True)
        write_csv('Program.csv', df)
    except Exception as e:
        raise Exception(f"Error adding program: {e}")

def delete_program(program_code):
    try:
        # Check if any Students are associated with this Program
        students = list_students()
        if program_code in students['Program Code'].values:
            raise Exception("Cannot delete program: Students are associated with this program.")

        # Delete the program
        df = read_csv('Program.csv')
        df = df[df['Code'] != program_code]
        write_csv('Program.csv', df)
    except Exception as e:
        raise Exception(f"Error deleting program: {e}")
    
def update_program(program_code, updated_data):
    try:
        df = read_csv('Program.csv')
        for key, value in updated_data.items():
            df.loc[df['Code'] == program_code, key] = value
        write_csv('Program.csv', df)
    except Exception as e:
        raise Exception(f"Error updating program: {e}")

def list_programs():
    try:
        return read_csv('Program.csv')
    except Exception as e:
        raise Exception(f"Error listing programs: {e}")