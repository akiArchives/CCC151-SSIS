import pandas as pd
from csv_handler import read_csv, write_csv

def add_student(student_data):
    try:
        df = read_csv('Student.csv')
        df = pd.concat([df, pd.DataFrame([student_data])], ignore_index=True)
        write_csv('Student.csv', df)
    except Exception as e:
        raise Exception(f"Error adding student: {e}")

def delete_student(student_id):
    try:
        df = read_csv('Student.csv')
        df = df[df['ID Number'] != student_id]
        write_csv('Student.csv', df)
    except Exception as e:
        raise Exception(f"Error deleting student: {e}")

def update_student(student_id, updated_data):
    try:
        df = read_csv('Student.csv')
        for key, value in updated_data.items():
            df.loc[df['ID Number'] == student_id, key] = value
        write_csv('Student.csv', df)
    except Exception as e:
        raise Exception(f"Error updating student: {e}")

def list_students():
    try:
        students = read_csv('Student.csv')
        return students
    except Exception as e:
        raise Exception(f"Error listing students: {e}")