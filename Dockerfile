FROM python:slim

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY . /app

EXPOSE 9000

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000","--reload"]
