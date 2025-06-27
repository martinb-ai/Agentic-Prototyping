import pandas as pd

# TODO: Implement your data loading logic here

def load_data():
    """Loads data for the application, e.g., from a CSV or database."""
    # Example: Create a dummy dataframe
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data)
    return df
