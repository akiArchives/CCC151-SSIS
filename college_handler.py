import pandas as pd
from csv_handler import read_csv, write_csv

def add_college(college_data):
    try:
        df = read_csv('College.csv')
        df = pd.concat([df, pd.DataFrame([college_data])], ignore_index=True)
        write_csv('College.csv', df)
    except Exception as e:
        raise Exception(f"Error adding college: {e}")

def delete_college(college_code):
    try:
        df = read_csv('College.csv')
        df = df[df['Code'] != college_code]
        write_csv('College.csv', df)
    except Exception as e:
        raise Exception(f"Error deleting college: {e}")

def update_college(college_code, updated_data):
    try:
        df = read_csv('College.csv')
        for key, value in updated_data.items():
            df.loc[df['Code'] == college_code, key] = value
        write_csv('College.csv', df)
    except Exception as e:
        raise Exception(f"Error updating college: {e}")

def list_colleges():
    try:
        return read_csv('College.csv')
    except Exception as e:
        raise Exception(f"Error listing colleges: {e}")