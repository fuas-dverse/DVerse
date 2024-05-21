# Python Agents Health Check

## Development

In order to work further on this tomorrow, I created this readme file in order to remember what I did today. So how can you run this application  (it is not finished completely).

First of all, you need to install the requirements. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

After that, you can run the application by running the following command:

```bash
python app.py
```

This will start the application on port 8080. You can access the application by going to the following URL:

```bash
http://localhost:8080
```

To test if the Flask application is consuming massages from kafka you can run the following file.

```bash
python send_kafka_messages.py
```
