FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV NAME GoogleSearchAgent

# Run your main.py script as entrypoint
CMD ["python", "main.py"]