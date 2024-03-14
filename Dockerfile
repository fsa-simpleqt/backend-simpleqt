FROM python:3.11.8-bullseye

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

COPY --chown=user ./requirements.txt /code/requirements.txt
COPY --chown=user . .

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD python main.py