FROM python:latest

# Bundle app source
ADD . /

# Install python requirements
RUN pip install -r requirements.txt

# Set argument for environment that can be set at build and will be used in the container via ENV
ARG environ=dev
ENV MY_ENVIRONMENT=$environ


ENTRYPOINT ["python", "/load_csv.py"]
