import pickle
import pandas as pd

class DatabaseManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        try:
            with open(self.filepath, 'rb') as f:
                df = pickle.load(f)
        except (FileNotFoundError, EOFError):
            df = pd.DataFrame(columns=['name', 'date', 'start_time', 'end_time', 'category'])
        return df

    def save_data(self, df):
        with open(self.filepath, 'wb') as f:
            pickle.dump(df, f)