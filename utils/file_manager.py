"""
FileManager - Handles all CSV file operations for the application.
Responsible for reading, writing, and creating CSV data files.
"""

import os
import pandas as pd
from pathlib import Path


class FileManager:
    """Manages CSV file operations using Pandas."""

    def __init__(self, data_folder="data"):
        self.data_folder = Path(data_folder)
        self._ensure_data_folder()

    def _ensure_data_folder(self):
        if not self.data_folder.exists():
            self.data_folder.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, filename):
        return self.data_folder / filename

    def file_exists(self, filename):
        return self.get_file_path(filename).exists()

    def create_file_if_missing(self, filename, columns):
        path = self.get_file_path(filename)
        if not path.exists():
            df = pd.DataFrame(columns=columns)
            df.to_csv(path, index=False)
        return path

    def read_csv(self, filename):
        path = self.get_file_path(filename)
        try:
            if not path.exists():
                return pd.DataFrame()
            df = pd.read_csv(path)
            return df
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return pd.DataFrame()

    def write_csv(self, filename, dataframe):
        path = self.get_file_path(filename)
        try:
            dataframe.to_csv(path, index=False)
            return True
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            return False

    def append_row(self, filename, row_dict, columns):
        df = self.read_csv(filename)
        if df.empty:
            df = pd.DataFrame(columns=columns)
        new_row = pd.DataFrame([row_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        self.write_csv(filename, df)
        return df

    def delete_row_by_id(self, filename, id_column, id_value):
        df = self.read_csv(filename)
        if df.empty:
            return df
        df = df[df[id_column].astype(str) != str(id_value)]
        self.write_csv(filename, df)
        return df

    def update_row_by_id(self, filename, id_column, id_value, updated_dict):
        df = self.read_csv(filename)
        if df.empty:
            return df
        mask = df[id_column].astype(str) == str(id_value)
        if mask.any():
            for key, value in updated_dict.items():
                if key in df.columns:
                    df.loc[mask, key] = value
            self.write_csv(filename, df)
        return df

    def generate_id(self, filename, id_column, prefix):
        df = self.read_csv(filename)
        if df.empty or id_column not in df.columns:
            return f"{prefix}001"
        existing_ids = df[id_column].astype(str)
        numbers = []
        for uid in existing_ids:
            num_part = uid.replace(prefix, "")
            try:
                numbers.append(int(num_part))
            except ValueError:
                continue
        if not numbers:
            return f"{prefix}001"
        next_num = max(numbers) + 1
        return f"{prefix}{next_num:03d}"