FROM python:3.9-slim
COPY env.yml env.yml
RUN conda env create -n 
COPY . .
CMD ["uvicorn", "blog.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

