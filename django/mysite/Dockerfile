# pull official base image
FROM python:3.10.12

# 작업 디렉토리 설정
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc python3-dev default-libmysqlclient-dev build-essential pkg-config libgl1-mesa-glx  && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
# 의존성 파일 복사 및 설치
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip && pip install -r requirements.txt
# 프로젝트 파일 복사
COPY . /usr/src/app 
# 로그 디렉토리 권한 설정
RUN chmod 755 /usr/src/app/logs
# 장고 설정
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput


