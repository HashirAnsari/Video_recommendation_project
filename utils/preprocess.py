import os
import json
import pandas as pd

import random

def load_json_files(directory):
    """
    Load all JSON files from a directory into a single DataFrame.

    Args:
        directory (str): Path to the directory containing JSON files.

    Returns:
        pd.DataFrame: Combined data as a Pandas DataFrame.
    """
    data_list = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            file_path = os.path.join(directory, file)
            print(f"Loading file: {file_path}")
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Check if 'posts' key exists and is a list
                if isinstance(data, dict) and "posts" in data and isinstance(data["posts"], list):
                    data_list.extend(data["posts"])  # Extract the list of posts
                else:
                    print(f"Unexpected data format in file: {file_path}. Expected a dictionary with a 'posts' key.")
    return pd.DataFrame(data_list)

def add_mood_column(input_path, output_path):
    """
    Adds a mood column to the dataset and saves it to the specified output file.

    Parameters:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to save the updated CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_path)

    # List of possible moods
    moods = ["happy", "calm", "energetic", "neutral"]

    # Generate moods (Random example; replace with logic based on data)
    if 'mood' not in df.columns:
        df['mood'] = [random.choice(moods) for _ in range(len(df))]
    else:
        print("Mood column already exists. Skipping creation.")

    # Save the updated dataset
    df.to_csv(output_path, index=False)
    print(f"Updated dataset with mood column saved to {output_path}")


def preprocess_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the raw data to clean and structure it for recommendations.
    """
    # Ensure column names are strings before processing
    raw_data.columns = [str(col).lower().strip() for col in raw_data.columns]

    # Debugging: Check the columns
    print(f"Columns after processing: {raw_data.columns}")

    # Check for required columns and rename as necessary
    if "id" not in raw_data.columns or "title" not in raw_data.columns:
        print("Required columns 'id' and 'title' are missing. Preprocessing aborted.")
        return pd.DataFrame()

    # Rename columns for consistency
    processed_data = raw_data.rename(columns={"id": "post_id", "title": "post_title"})

    # Remove rows with missing critical values
    processed_data = processed_data.dropna(subset=["post_id", "post_title"])

    # Debugging: Print a sample of processed data
    print(f"Sample processed data: {processed_data.head()}")

    return processed_data



def save_processed_data(df: pd.DataFrame, save_path: str):
    """
    Save the processed data to a CSV file.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        save_path (str): Path to save the processed data as a CSV file.
    """
    if df.empty:
        print("Processed data is empty. Nothing to save.")
        return

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Processed data saved to {save_path}")


def preprocess_raw_data(raw_directory: str, processed_path: str):
    """
    Complete preprocessing pipeline: load raw data, preprocess it, and save the processed data.

    Args:
        raw_directory (str): Path to the directory containing raw JSON files.
        processed_path (str): Path to save the processed data as a CSV file.
    """
    print("Loading raw data...")
    raw_data = load_json_files(raw_directory)
    print(f"Loaded data: {raw_data.shape if not raw_data.empty else 'No data found'}")

    if raw_data.empty:
        print("No raw data found. Check if JSON files exist in the raw directory.")
        return

    print("Preprocessing data...")
    processed_data = preprocess_data(raw_data)
    print(f"Processed data: {processed_data.shape if not processed_data.empty else 'No data after processing'}")

    print("Saving processed data...")
    save_processed_data(processed_data, processed_path)
    print("Data preprocessing complete.")



