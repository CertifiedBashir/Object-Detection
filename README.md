# Object Detection & OCR Web Application

This is a Flask-based web application that allows users to upload images and automatically extracts text from them using **EasyOCR**. It keeps a history of all uploaded images and their extracted texts, saving this information to a MySQL database.

## Features
- **Image Upload:** Supports common image formats (JPG, PNG, BMP, TIFF, WebP).
- **Automatic Text Extraction:** Uses EasyOCR behind the scenes to find and extract text from images.
- **History Tracking:** All uploaded images and their OCR results are saved to a database for easy retrieval and viewing.

## Technology Stack
- **Backend Framework:** Flask
- **Database ORM:** Flask-SQLAlchemy
- **Database Migrations:** Flask-Migrate
- **Database Engine:** MySQL (connected via PyMySQL)
- **Machine Learning / OCR:** EasyOCR

---

## Configuration & Setup Guide

Follow these steps to configure the application and run it on your local device.

### 1. Prerequisites
- **Python 3.8+** installed on your machine.
- **MySQL Server** installed and running locally (or remotely).
- (Optional but recommended) A C++ compiler or build tools if required by EasyOCR on Windows.

### 2. Clone or Prepare the Repository
Make sure you are in the root directory of this project (`Object Detection`).

### 3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies:
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 4. Install Dependencies
You need to install the required Python packages. Run the following command in your activated virtual environment:
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate python-dotenv PyMySQL easyocr
```

> **Note:** The first time you run EasyOCR, it will download the pre-trained OCR models automatically.

### 5. Database Configuration
1. Open the `.env` file in the root directory.
2. Update the database credentials to match your MySQL setup:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=object_detection_db
   ```
3. Ensure that the database `object_detection_db` actually exists in your MySQL server. You can create it by logging into MySQL and running:
   ```sql
   CREATE DATABASE object_detection_db;
   ```

### 6. Apply Database Migrations
Set up the tables in your database by running the Flask migrations:
```bash
# If the migrations folder does not exist yet:
flask db init

# Create the initial migration
flask db migrate -m "Initial migration"

# Apply the migration to the database
flask db upgrade
```

### 7. Run the Application
Start the Flask development server:
```bash
python app.py
```
*(Alternatively, you can run `flask run`)*

The application should now be running locally. Open your web browser and navigate to:
**http://127.0.0.1:5000**

## Usage
1. Go to the home page at `http://127.0.0.1:5000`.
2. Select an image from your computer using the upload form.
3. Submit the image. The app will process it, run OCR, and return the extracted text.
4. You can view the history of all processed images by navigating to the `/history` endpoint or checking the corresponding UI if available.
