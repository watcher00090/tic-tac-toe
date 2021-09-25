# Ubuntu 20:04 LTS
FROM ubuntu:20.04 

SHELL ["/bin/bash", "-c"]

RUN mkdir /home/tic-tac-toe

WORKDIR /home/tic-tac-toe

RUN apt update
# Make 'python' refer to python3
RUN apt install -y python-is-python3

# Install Go
RUN mkdir downloads
RUN apt install -y curl
RUN curl -L "https://golang.org/dl/go1.17.1.linux-amd64.tar.gz" -o downloads/go1.17.1.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf downloads/go1.17.1.linux-amd64.tar.gz
RUN bash -c 'echo "export PATH=$PATH:/usr/local/go/bin" >> /etc/profile'
ENV PATH="$PATH:/usr/local/go/bin"
ENV CODE_PATH="/home/tic-tac-toe"

RUN mkdir src
RUN mkdir bin

COPY *.go   src/
COPY go.mod src/

WORKDIR /home/tic-tac-toe/src

RUN go build -o ../bin/tic-tac-toe

WORKDIR /home/tic-tac-toe

RUN mkdir test
COPY test/* test/