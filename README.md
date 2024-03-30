## Installation

1. Clone the repository
2. Navigate to the project directory: `cd Architech`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On macOS and Linux: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`
6. Apply the database migrations: `python manage.py migrate`

## Usage

1. Start the development server: `python manage.py runserver`
2. Open your web browser and go to `http://127.0.0.1:8000/`
