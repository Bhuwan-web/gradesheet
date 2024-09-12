# GradeSheet

**GradeSheet** is a Django-based web application designed to manage student records and grades. The project is built to be primarily used with a frontend interface, but it also supports RESTful operations through Django Rest Framework (DRF). For debugging and development purposes, the Django Debug Toolbar is integrated.

## Features

- **Student Record Management**: Manage student data, subjects, and grades.
- **REST API Support**: Exposes API endpoints for integration with other systems.
- **Frontend Interface**: Designed to interact with a frontend application.
- **Django Debug Toolbar**: Debugging tools for monitoring SQL queries, cache usage, and performance.

## Project Structure

- `gradesheet/`: Main project folder.
- `student_record/`: App responsible for handling student-related functionality.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd gradesheet
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Development Tools

- **Django Debug Toolbar**: Installed to help debug performance and SQL issues. To enable it, ensure `DEBUG = True` in the settings file.
- **Django Rest Framework (DRF)**: Provides API endpoints for the `student_record` app.

## API Endpoints

The REST API is available under `/api/`, allowing integration with external services.

## Contributing

Feel free to submit issues or pull requests for any improvements or fixes!

## License

[MIT License](LICENSE)
