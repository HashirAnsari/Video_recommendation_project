# import pandas as pd
# import json
# import os
# import re


# def safe_json_load(row):
#     """
#     Safely parse a JSON string. If parsing fails, return an empty dictionary.
#     """
#     try:
#         return json.loads(row) if pd.notna(row) else {}
#     except json.JSONDecodeError:
#         return {}

# def refine_viewed_posts(input_file: str, output_file: str):
#     print("Loading dataset...")
#     df = pd.read_csv(input_file)
#     print(f"Dataset loaded with shape: {df.shape}")

#     # Fix 'category' column parsing
#     print("Parsing 'category' column...")

#     def parse_category(row):
#         if pd.notna(row):
#             try:
#                 # Replace single quotes with double quotes for valid JSON
#                 row = re.sub(r"'", '"', row)
#                 data = json.loads(row)
#                 return pd.Series({'category_id': data.get('id'), 'category_name': data.get('name')})
#             except json.JSONDecodeError:
#                 return pd.Series({'category_id': None, 'category_name': None})
#         else:
#             return pd.Series({'category_id': None, 'category_name': None})

#     # Apply parsing and split into two new columns
#     category_data = df['category'].apply(parse_category)
#     df['category_id'] = category_data['category_id']
#     df['category_name'] = category_data['category_name']

#     print("Sample of parsed 'category' data:")
#     print(df[['category_id', 'category_name']].head())

#     # Scale average_rating column
#     if 'average_rating' in df.columns:
#         scaler = MinMaxScaler()
#         df['average_rating_scaled'] = scaler.fit_transform(df[['average_rating']])
#     else:
#         print("Column 'average_rating' not found. Ensure the dataset includes this column.")

#     # Save processed file
#     df.to_csv(output_file, index=False)

#     # Save the refined dataset
#     print(f"Saving refined data to {output_file}...")
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
#     df.to_csv(output_file, index=False)
#     print("Refined data saved successfully!")

# from utils.preprocess import add_mood_column

# if __name__ == "__main__":
#     input_file = "data/processed/viewed_posts_refined.csv"
#     output_file = "data/processed/viewed_posts_refined.csv"

#     add_mood_column(input_file, output_file)



# def load_data(file_path):
#     """
#     Load and return the refined data.
#     """
#     try:
#         return pd.read_csv(file_path)
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return None

# if __name__ == "__main__":
#     input_file = "data/processed/viewed_posts.csv"
#     output_file = "data/processed/viewed_posts_refined.csv"
#     refine_viewed_posts(input_file, output_file)

#-------------------------------------------------------------------------------

import sys
import os
import pandas as pd
import json
import re

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)

# Import the add_mood_column function
import importlib.util
spec = importlib.util.spec_from_file_location("preprocess", "./utils/preprocess.py")
preprocess = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preprocess)

add_mood_column = preprocess.add_mood_column



def safe_json_load(row):
    """
    Safely parse a JSON string. If parsing fails, return an empty dictionary.
    """
    try:
        return json.loads(row) if pd.notna(row) else {}
    except json.JSONDecodeError:
        return {}


def refine_viewed_posts(input_file: str, output_file: str):
    print("Loading dataset...")
    df = pd.read_csv(input_file)
    print(f"Dataset loaded with shape: {df.shape}")

    # Fix 'category' column parsing
    print("Parsing 'category' column...")

    def parse_category(row):
        if pd.notna(row):
            try:
                # Replace single quotes with double quotes for valid JSON
                row = re.sub(r"'", '"', row)
                data = json.loads(row)
                return pd.Series({'category_id': data.get('id'), 'category_name': data.get('name')})
            except json.JSONDecodeError:
                return pd.Series({'category_id': None, 'category_name': None})
        else:
            return pd.Series({'category_id': None, 'category_name': None})

    # Apply parsing and split into two new columns
    category_data = df['category'].apply(parse_category)
    df['category_id'] = category_data['category_id']
    df['category_name'] = category_data['category_name']

    print("Sample of parsed 'category' data:")
    print(df[['category_id', 'category_name']].head())

    # Save the refined dataset before adding the mood column
    print(f"Saving intermediate refined data to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

    # Add the mood column
    print("Adding mood column...")
    add_mood_column(output_file, output_file)

    print("Refined data saved successfully!")


if __name__ == "__main__":
    input_file = "data/processed/viewed_posts.csv"
    output_file = "data/processed/viewed_posts_refined.csv"
    refine_viewed_posts(input_file, output_file)


