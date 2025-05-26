# Use official Python image
FROM python:3.12.6 

# Set work directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron job
RUN echo "0 3 * * * python /app/django_project/cron_jobs/expire_subscriptions.py" > /etc/cron.d/expire_subscriptions
RUN chmod 0644 /etc/cron.d/expire_subscriptions
RUN crontab /etc/cron.d/expire_subscriptions

# Ensure cron runs in the background
RUN touch /var/log/cron.log

# Expose port
EXPOSE 8000

# Run migrations and start the server
CMD service cron start && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000