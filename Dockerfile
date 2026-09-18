# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV TZ Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt upgrade -y && apt-get install -y --no-install-recommends procps net-tools

WORKDIR /app

# Module copy
COPY . /app

# Install pip requirements
# RUN apt-get install -y cron
RUN python -m pip install --no-input --upgrade pip
RUN python -m pip install --no-input -r /app/requirements.txt
RUN chmod +x /app/main.sh

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser
ENV PATH="/home/root/.local/bin:${PATH}"

CMD ["./main.sh"]
