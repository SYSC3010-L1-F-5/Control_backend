FROM python:alpine

ADD VERSION .

WORKDIR /backend
COPY requirement.txt ./
RUN RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD flask run --no-debugger --host=0.0.0.0 --port=5000