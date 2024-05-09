# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script files to the working directory
COPY ./ipfs_sync ./ipfs_sync

# Set the entry point command to run the script
ENTRYPOINT ["python", "-m", "ipfs_sync.main"]
