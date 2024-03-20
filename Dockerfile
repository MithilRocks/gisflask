FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./

COPY tests.py ./

# Install GDAL
RUN apt-get update
RUN apt-get install libgdal-dev -y
RUN apt-get install g++ -y

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py

# Define environment variable
ENV MBTILES=static/opgrsp_gb.mbtiles

# Run the tests
RUN python -m unittest tests.py -v

# Run the flask app when the container launches
CMD ["flask", "run", "--port=5000"]