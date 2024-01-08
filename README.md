# Flask User Management Web App

This is a simple Flask web application for managing user records. It allows you to perform CRUD operations (Create, Read, Update, Delete) on user data with image uploads.

## Setup

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Configure the application:

    - Set the database URI and other configurations in `config.py` or through environment variables.
    - Ensure that the `UPLOAD_FOLDER` is set to the desired directory for storing user images.

3. Initialize the database:

    ```bash
    python app.py
    ```

4. Run the application:

    ```bash
    python app.py
    ```

Access the application at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage

- Visit the home page to view existing users and add new ones.
- Click on "Agregar" to add a new user or "Modificar" to edit an existing user.
- Upload user images with supported formats (png, jpg, jpeg, gif).
- View and manage user records in the "Registros" section.
- Delete users as needed.

## File Structure

- `app.py`: Main application file containing Flask routes and configurations.
- `config.py`: Configuration file for the application.
- `templates/`: HTML templates for rendering pages.
- `static/`: Static files such as CSS, JavaScript, and user-uploaded images.

## Dependencies

- Flask
- Flask-SQLAlchemy
- Werkzeug

## Notes

- Ensure that you have a secure deployment configuration for production use.
- Validate and sanitize user inputs to prevent security vulnerabilities.
- Customize the application based on your specific requirements.

Feel free to contribute and enhance the functionality of this simple user management application.

## TODO
- Test the app with a workflow to get the badge