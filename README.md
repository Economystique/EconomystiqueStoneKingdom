# Economystique
#This is the newly redesigned and converted Economystique. 
#From QT to Flask framework.

A comprehensive inventory and sales management system built with Flask.

## Features

- User Authentication
- Dashboard with Sales Analytics
- Inventory Management
- Point of Sale (POS) System
- Sales Tracking and Forecasting
- Account Management

## Requirements

- Python 3.8 or higher
- SQLite3
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/economystique.git
cd economystique
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
economystique/
├── app.py              # Main application file
├── init_db.py         # Database initialization script
├── requirements.txt   # Python dependencies
├── static/           # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/        # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── ...
└── db/              # Database directory
    └── users_db.db
```

## Development

- The application uses Flask for the backend
- Frontend is built with HTML, CSS, and JavaScript
- SQLite is used for data storage
- Chart.js for data visualization
- Font Awesome for icons

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.