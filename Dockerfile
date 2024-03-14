FROM python:3.11.8-bullseye

ENV HOME=/home/user

WORKDIR $HOME/code

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

COPY --chown=user:user ./requirements.txt $HOME/code/requirements.txt

COPY --chown=user:user . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r $HOME/code/requirements.txt

EXPOSE 7860

CMD python main.py