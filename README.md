# Engage IQ Lauri Backend

## Prerequisites
- **Python**: 3.12.6
- **Django**: 5.1.4
- **PostgreSQL**: Ensure it is installed and configured.
- **Virtual Environment**: Recommended for package isolation.

---

## Project Setup Steps

### 0. **Install PostgreSQL**
- Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).
- During installation, ensure you include **pgAdmin** for database management.

### 1. **Clone the Repository**
```bash
git clone -b dev-backend https://github.com/Cplus-Soft-Limited/email-generation-bot.git
cd backend
```

### 2. **Set Up a Virtual Environment**
It is highly recommended to use a virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```

### 3. **Install Required Dependencies**
Install all required packages using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. **Set Up the Database**
#### Create the PostgreSQL Database:
1. Open **pgAdmin** and log in using your PostgreSQL credentials.
2. Right-click on **Databases** → Click **Create** → **Database**.
3. Fill in the following details:
   - **Database name**: (e.g., `your_database_name`)
   - **Owner**: Select an existing user (e.g., `postgres`) or create a new one.
4. Save the database configuration.

#### Update the `.env` File:
Get the existing credentials from **Hamid** or set your own, then update the `.env` file:
```plaintext
# Database credentials
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_password
DB_HOST=localhost  # or the host address if remote
DB_PORT=5432       # Default PostgreSQL port

# Email credentials
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_default_email
```
OPENAI_API_KEY=add your openai api key here
### 5. **Apply Migrations**
Run the following command to set up your database tables:
```bash
python manage.py migrate
```

### 6. **Create a Superuser**
Create a superuser account for accessing the Django admin interface:
```bash
python manage.py createsuperuser
```

### 7. **Load Initial Data**
Run the following scripts to load prompts and subscription plans into the database:
```bash
python load_prompts.py
```
```bash
python update_subscription_plans.py
```

### 8. **Run the Development Server**
Start the Django development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/admin` to access the admin interface.
You can acess the server at this http://143.198.102.57:8000  and http://143.198.102.57:8001 i have used the tmux and PM2
---

## Additional Information

### Branch Details
- **`dev-backend`**: The active development branch where all new features and updates are being worked on.

---

## Notes:
1. Make sure to obtain the `.env` file data, including database credentials and SMTP email details, from **Hamid** or create your own.
2. The project is configured to use PostgreSQL. Ensure you have created the database and updated the `.env` file accordingly.
3. Test the SMTP setup to ensure email functionalities work as expected.
