FROM python:3-alpine

RUN apk add --no-cache zlib-dev tiff-dev openjpeg musl libwebp libjpeg-turbo lcms2 freetype gcc

COPY requirements_frozen.txt .
RUN LIBRARY_PATH=/lib:/usr/lib pip install -r requirements_frozen.txt

COPY bot.py .
CMD ["python", "bot.py"]
