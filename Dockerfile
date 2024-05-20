FROM paddlepaddle/paddle:2.3.2-gpu-cuda11.2-cudnn8   

WORKDIR /app

COPY requirements.txt .

RUN pip install pip==21.1.1 && \
    pip install -r requirements.txt

RUN apt update && \
    apt install ffmpeg -y

COPY . .

CMD bash