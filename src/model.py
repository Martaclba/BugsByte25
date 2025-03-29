

# process
import pandas as pd

def load_model(path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(path)
    print(df)