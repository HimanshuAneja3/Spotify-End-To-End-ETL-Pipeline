# Spotify End-to-End ETL Pipeline

This project aims to create an ETL pipeline for extracting data from the Spotify API and storing it in a target location. The pipeline handles the extraction of music-related data from Spotify, performs necessary transformations, and loads the processed data into a specified storage location.

## Objective

The goal of this project is to build a robust and scalable ETL pipeline that can:
- Connect to the Spotify API securely.
- Extract relevant data (such as tracks, albums, artists, playlists).
- Transform the raw data into a structured format suitable for analysis and storage.
- Load the transformed data into a target location (e.g., database, data warehouse).

## Technologies Used

- Python
- Spotify API
- AWS S3
- AWS Lambda
- AWS Glue
- AWS Athena

## Project Structure

### 1. Data Extraction

- **Spotify API Authentication:** Securely connect to the Spotify API using OAuth tokens.
- **Data Extraction Scripts:** Python scripts to extract data on tracks, albums, artists, and playlists. These scripts are scheduled to run at regular intervals to fetch the latest data.

### 2. Data Storage

- **AWS S3:** Raw data extracted from the Spotify API is stored in Amazon S3 in JSON format. Each type of data (tracks, albums, artists, playlists) is stored in separate S3 buckets for better organization and retrieval.

### 3. Data Transformation

- **AWS Lambda:** AWS Lambda functions are triggered whenever new data is uploaded to the S3 buckets. These functions perform the necessary transformations on the raw data, such as:
  - Cleaning and validating the data.
  - Normalizing and structuring the data into a tabular format.
  - Enriching the data with additional metadata if necessary.

### 4. Data Loading

- **AWS Glue:** AWS Glue jobs are used to further transform and catalog the data. The transformed data is stored back in S3 in a columnar format (e.g., Parquet) to optimize storage and query performance.
- **AWS Athena:** Amazon Athena is used to query the processed data stored in S3. Glue Data Catalog tables are created to organize the data, making it easily queryable using standard SQL queries.

### 5. Automation and Scheduling

- **AWS Step Functions:** AWS Step Functions orchestrate the entire ETL process, ensuring that each step is executed in the correct sequence and handling any errors or retries.
- **CloudWatch Events:** AWS CloudWatch Events are used to trigger the Lambda functions and Step Functions workflows at scheduled intervals, ensuring that the ETL pipeline runs automatically and consistently.

## Detailed Workflow

1. **Authentication:**
   - A Python script using the `spotipy` library authenticates with the Spotify API using client credentials.

2. **Data Extraction:**
   - The script fetches data from Spotify endpoints and stores the raw JSON data in respective S3 buckets (`s3://spotify-data/raw/tracks/`, `s3://spotify-data/raw/albums/`, etc.).

3. **Triggering Transformations:**
   - Uploading data to S3 triggers Lambda functions, which read the raw data, transform it, and store the transformed data in a different S3 bucket (`s3://spotify-data/transformed/`).

4. **Further Transformation with AWS Glue:**
   - Glue jobs transform the data into a columnar format like Parquet and catalog it in the AWS Glue Data Catalog.

5. **Querying with AWS Athena:**
   - Glue Data Catalog tables are created, making the data queryable with Amazon Athena. Users can run SQL queries to analyze the Spotify data directly in the S3 storage.

## Benefits

- **Scalability:** The use of AWS services ensures that the pipeline can handle large volumes of data and scale as needed.
- **Automation:** The entire ETL process is automated, from data extraction to transformation and loading, reducing manual intervention and the risk of errors.
- **Cost-Effective:** Using AWS's serverless architecture (Lambda, Glue, Athena) helps in managing costs efficiently, as you only pay for the resources when they are used.
- **Flexibility:** The modular structure allows easy updates and modifications to the pipeline as needed.

## Conclusion

This ETL pipeline provides a robust and scalable solution for extracting, transforming, and loading Spotify data into a target storage location, enabling efficient analysis and reporting. The use of AWS services ensures that the pipeline is both cost-effective and highly available.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/spotify-etl-pipeline.git
   cd spotify-etl-pipeline
