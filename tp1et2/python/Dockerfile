FROM python:3.14-slim

WORKDIR /app

COPY . /app

RUN chmod +x run_py.sh main.py banking.py associativity_llm.py

CMD ["./run_py.sh"]
