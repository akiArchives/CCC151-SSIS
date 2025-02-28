import pandas as pd
import os

CSV_FOLDER = 'csv-files'

def ensure_csv_files_exist():
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)
    
    files = {
        'Student.csv': ['ID Number', 'First Name', 'Last Name', 'Year Level', 'Gender', 'Program Code'],
        'Program.csv': ['Code', 'Name', 'College'],
        'College.csv': ['Code', 'Name']
    }
    for filename, columns in files.items():
        filepath = os.path.join(CSV_FOLDER, filename)
        if not os.path.exists(filepath):
            try:
                df = pd.DataFrame(columns=columns)
                df.to_csv(filepath, index=False)
            except Exception as e:
                raise Exception(f"Error creating {filepath}: {e}")

def read_csv(filename):
    filepath = os.path.join(CSV_FOLDER, filename)
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} not found.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"File {filepath} is empty or has no valid data.")
    except pd.errors.ParserError:
        raise ValueError(f"File {filepath} contains invalid data.")
    except Exception as e:
        raise Exception(f"Error reading {filepath}: {e}")

def write_csv(filename, df):
    filepath = os.path.join(CSV_FOLDER, filename)
    try:
        df.to_csv(filepath, index=False)
    except Exception as e:
        raise Exception(f"Error writing to {filepath}: {e}")

def add_entry(filename, entry_data):
    try:
        df = read_csv(filename)
        df = pd.concat([df, pd.DataFrame([entry_data])], ignore_index=True)
        write_csv(filename, df)
    except Exception as e:
        raise Exception(f"Error adding entry to {filename}: {e}")

def delete_entry(filename, key_column, key_value):
    try:
        df = read_csv(filename)
        df = df[df[key_column] != key_value]
        write_csv(filename, df)
    except Exception as e:
        raise Exception(f"Error deleting entry from {filename}: {e}")

def update_entry(filename, key_column, key_value, updated_data):
    try:
        df = read_csv(filename)
        for key, value in updated_data.items():
            df.loc[df[key_column] == key_value, key] = value
        write_csv(filename, df)
    except Exception as e:
        raise Exception(f"Error updating entry in {filename}: {e}")

def list_entries(filename):
    try:
        return read_csv(filename)
    except Exception as e:
        raise Exception(f"Error listing entries from {filename}: {e}")