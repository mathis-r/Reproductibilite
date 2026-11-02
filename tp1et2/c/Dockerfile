FROM gcc:15

WORKDIR /app

COPY . /app

RUN gcc -o main main.c
RUN gcc -o banking banking.c
RUN gcc -o llm associativity_llm.c
CMD ["./run_c.sh"]
