FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV NAME FestivalInformationAgent

# Run your app.py script as entrypoint
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]