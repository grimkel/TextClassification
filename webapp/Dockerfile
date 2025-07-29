FROM python:3.10.18

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

RUN pip3 install -r ./requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]