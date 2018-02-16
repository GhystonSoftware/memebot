
FROM python:3
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .
EXPOSE 5000
CMD ["python", "./memebot.py"]
