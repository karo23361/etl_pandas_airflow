FROM apache/airflow:2.9.1-python3.10

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    requests \
    openpyxl \
    pyarrow \
    beautifulsoup4 \
    lxml
