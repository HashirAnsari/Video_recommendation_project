import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
def load_processed_data(file_path="data/processed/viewed_posts_scaled.csv"):
    """
    Load the refined dataset.
    :param file_path: Path to the refined CSV file.
    :return: DataFrame containing the processed data.
    """
    print("Loading processed data...")
    df = pd.read_csv(file_path)
    print(f"Dataset loaded with shape: {df.shape}")
    return df

def clean_text(text):
    """
    Clean text data by removing special characters, emojis, and extra spaces.
    :param text: Input text string.
    :return: Cleaned text string.
    """
    # Remove emojis, hashtags, and non-alphanumeric characters
    text = re.sub(r"[^\w\s]", "", text)  # Remove non-alphanumeric characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def compute_similarity_matrix(features):
    """
    Compute a similarity matrix using cosine similarity.
    :param features: Feature matrix for similarity computation.
    :return: Similarity matrix.
    """
    print("Computing similarity matrix...")
    if not isinstance(features, np.ndarray):
        print("Converting features to array...")
        features = features.toarray()  # Convert sparse matrix to dense array
    similarity_matrix = cosine_similarity(features)
    print("Similarity matrix computed!")
    return similarity_matrix

def validate_features(features):
    """
    Validate that the feature matrix is numeric and non-empty.
    :param features: Feature matrix.
    """
    print("Validating feature matrix...")
    if features is None or features.shape[0] == 0:
        raise ValueError("Feature matrix is empty. Check input data.")
    if not np.issubdtype(features.dtype, np.number):
        raise ValueError("Feature matrix contains non-numeric values.")

def evaluate_recommendations(df, similarity_matrix):
    """
    Evaluate recommendation quality using MAE and RMSE.
    :param df: DataFrame containing user interaction data.
    :param similarity_matrix: Precomputed similarity matrix.
    :return: MAE and RMSE values.
    """
    print("Evaluating recommendations...")

    # Example: Assume ground truth is based on `average_rating_scaled`
    ground_truth = df['average_rating_scaled'].values

    # Simulated predictions: Average similarity scores (mock evaluation)
    predictions = similarity_matrix.mean(axis=1)

    # Ensure equal length (truncate if necessary)
    min_len = min(len(ground_truth), len(predictions))
    ground_truth = ground_truth[:min_len]
    predictions = predictions[:min_len]

    # Calculate MAE and RMSE
    mae = mean_absolute_error(ground_truth, predictions)
    rmse = np.sqrt(mean_squared_error(ground_truth, predictions))

    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    return mae, rmse

import math

def sanitize_recommendations(recommendations):
    for rec in recommendations:
        if isinstance(rec['post_title'], float) and math.isnan(rec['post_title']):
            rec['post_title'] = "No Title Available"  # Replace NaN with a placeholder
    return recommendations



def get_recommendations(username=None, category_id=None, mood=None):
    # Load preprocessed data
    data_path = "data/processed/viewed_posts_refined.csv"
    if not os.path.exists(data_path):
        print(f"Data file {data_path} not found.")
        return []

    data = pd.read_csv(data_path)

    # Debugging inputs and dataset
    print(f"category_id: {category_id} (type: {type(category_id)})")
    print(f"Dataset shape: {data.shape}")
    print(data.head())  # Check the first few rows

    try:
        category_id = int(category_id)  # Convert to integer if possible
    except ValueError:
        print(f"Invalid category_id: {category_id}")
        return []

    # Apply filtering logic
    filtered_data = data[
        (data['username'] == username) &
        (data['category_id'] == category_id) &
        (data['mood'] == mood)
    ]

    # Debugging filtered data
    print(f"Filtered data: {filtered_data}")

    if filtered_data.empty:
        print(f"No data found for username={username}, category_id={category_id}, mood={mood}.")
        return []
    
    
    # Replace NaN values with a default string
    filtered_data['post_title'] = filtered_data['post_title'].fillna('No Title Available')
    # Generate recommendations from the filtered data
    recommendations = filtered_data[['post_id', 'post_title']].to_dict(orient='records')

    return recommendations

    
    # # Convert to recommendations
    # recommendations = filtered_data[['post_id', 'post_title']].to_dict(orient='records')
    # return jsonify({"recommendations": recommendations}), 200




if __name__ == "__main__":
    try:
        # Load processed data
        df = load_processed_data()

        # Clean text data in 'post_title'
        print("Cleaning text data in 'post_title' column...")
        df['post_title'] = df['post_title'].fillna("").apply(clean_text)
        print("Text data cleaned successfully!")

        # Prepare features
        print("Preparing features for similarity calculation...")
        tfidf_vectorizer = TfidfVectorizer()
        features = tfidf_vectorizer.fit_transform(df['post_title'])

        # Validate features
        validate_features(features)

        # Compute similarity matrix
        similarity_matrix = compute_similarity_matrix(features)

        # Evaluate recommendations
        evaluate_recommendations(df, similarity_matrix)

        # Generate recommendations for a sample post_id
        get_recommendations(1225, df, similarity_matrix)

    except Exception as e:
        print(f"Error occurred: {e}")



