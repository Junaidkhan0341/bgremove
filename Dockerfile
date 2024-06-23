FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Pre-download the U2Net model
RUN python -c "from rembg import remove; from PIL import Image; import io; image = Image.new('RGB', (1, 1)); remove(image)"

CMD ["python", "app.py"]
