# Video_recommendation_system



## Project Overview
This project is focused on creating a recommendation system for motivational videos using APIs from the Empowerverse App. The system leverages user interaction data and video metadata to provide personalized video recommendations. The solution addresses challenges like the cold-start problem and implements robust evaluation metrics.

## Features
- Fetching video metadata and user interaction data using APIs with pagination.
- Content-based recommendation system.
- Addressing cold-start problem scenarios.
- API endpoints to provide recommendations based on username, category, and mood.
- Evaluation of recommendations using MAE and RMSE metrics.

---

## Project Directory Structure
```
video-recommendation/
├── app.py                # Main Flask application
├── requirements.txt      # List of required Python libraries
├── data/                 # Folder for raw and preprocessed data
│   ├── raw/              # Raw data fetched from APIs
│   └── processed/        # Preprocessed/cleaned data files
├── models/               # Folder for recommendation algorithm logic
│   └── content_based.py  # Content-based filtering logic
├── utils/                # Utility functions
│   ├── fetch_data.py     # API data fetching logic
│   ├── preprocess.py     # Data preprocessing functions
|   ├── __init__.py       #
|   ├── refined_data.py   # Refining data and saving.
├── tests/                # Folder for testing scripts
│   └── test_endpoints.py # Script to test API endpoints
├── templates/            # HTML templates for web interface (optional for API-only projects)
│   └── index.html        # Example template for web UI
├── static/               # Static files (CSS, JS, images) for the web interface


```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/HashirAnsari/Video_recommendation_system.git
   cd video-recommendation
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Access the application at:
   ```
   http://127.0.0.1:5000
   ```

---

## API Endpoints

### 1. **`/recommendations`**
- **Method**: POST
- **Description**: Returns personalized video recommendations based on user input.
- **Request Payload**:
  ```json
  {
    "username": "<string>", # username example :- kinha , MinalJoshi , ankur_raj , abasss00
    "category_id": <integer>, # category_id example :- 2 , 22 , 25 , 8
    "mood": "<string>" # Happy , energetic , calm , neutral
  }
  ```
- **Response**:
  ```json
  {
    "recommendations": [
      {

        "title": "<string>",
        
      }
    ]
  }
  ```

### 2. **`/health`**
- **Method**: GET
- **Description**: Health check endpoint to ensure the application is running.
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

---

## Key Files and Their Roles

### `app.py`
The main Flask application that defines routes, loads data, and handles requests.

### `content_based.py`
Contains the logic for content-based recommendation system. It computes similarity scores and recommends videos based on video metadata.

### `fetch_data.py`
Includes functions for fetching video metadata and user interaction data from APIs. Handles pagination to retrieve large datasets efficiently.

### `preprocess.py`
Contains data preprocessing functions such as cleaning text data, handling missing values, and preparing feature vectors for similarity calculations.

### index.html
A simple web interface template for user interaction and viewing recommendations.

### refined_data.py 
Handles data refinement and preprocessing, including cleaning and feature extraction.  

---

## Data Workflow
1. **Fetch Data**: Retrieve raw video and user data using APIs.
2. **Preprocess Data**: Clean and transform data for use in the recommendation system.
3. **Compute Similarity**: Use preprocessed data to compute similarity matrices for recommendations.
4. **Generate Recommendations**: Serve recommendations based on user input.

---

## Evaluation
Evaluation metrics implemented include:
- **Mean Absolute Error (MAE)**
- **Root Mean Square Error (RMSE)**

---

## Testing
### Running Tests
- Use the provided `test_endpoints.py` to test API endpoints.
  ```bash
  python tests/test_endpoints.py
  ```

### Example Output
- The tests ensure all endpoints return the correct response format and handle errors gracefully.

---

## Future Enhancements
- Add collaborative filtering logic for improved personalization.
- Introduce hybrid recommendation models.
- Enhance user interface for better user experience.
- Optimize performance for large-scale datasets.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

---

## License
This project is licensed under the MIT License.

## Acknowledgments
- Empowerverse App: For providing APIs and video metadata.
- Open-source libraries and contributors.

