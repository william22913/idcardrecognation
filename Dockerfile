FROM python:3.10.9

COPY . .
RUN pip install numpy
RUN pip install opencv-python-headless
RUN pip install scikit-image
RUN pip install scipy
RUN pip install git+https://github.com/william22913/face_recognition
RUN pip install Flask
RUN pip install requests

CMD ["python", "Main.py"]