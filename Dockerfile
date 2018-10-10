FROM python:3.6

RUN mkdir /opt/discord-statusbot/
COPY . /opt/discord-statusbot/
RUN pip install -r /opt/discord-statusbot/requirements.txt

ENTRYPOINT ["python", "/opt/discord-statusbot/bin/bot.py"]
