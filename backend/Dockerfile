#Start with an official lightweight Python 3.10 environment.
FROM python:3.10-slim 

#Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies (important for cv2 + mediapipe)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

#Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#Copy the entire backend folder into the container.
COPY . .

#Expose port 10000 for the FastAPI server. This is the command that starts your backend when the container runs.
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]

