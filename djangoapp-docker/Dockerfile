# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE djangoapp.settings

# Set the working directory in the container
WORKDIR /app


# Install dependencies using Pipenv
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY ./djangoapp/ /app/

# Expose port 8000 (adjust as needed)
EXPOSE 8000

# Start the Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
