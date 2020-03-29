
# Environment for the microservice ThreadSanitizer.
# Clang 6 is installed from the Ubuntu repository.
# Clang 10 is installed from the official LLVM repository.
# To use Clang 10, a "-10" postfix should be added in most cases.
# e.g. clang -> clang-10, clang++ -> clang++-10
# Please check /usr/bin for all the available Clang 10 tools.

# Pull base image.
FROM ubuntu:18.04

# Add user
RUN groupadd -g 9999 rds && \
    useradd -r -u 9999 -g rds -m -d /home/rds rds

# Install packages.
RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        dialog \
        software-properties-common \
        wget && \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    add-apt-repository -y 'deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-10 main' && \
    apt-get update && \
    apt-get install -y \ 
        bc \
        build-essential \
        clang-10 \
        cmake \
        curl \
        gdb \
        git \
        python3-dev \
        time \
        vim && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/*

# Install API framework
RUN apt-get update && \
    apt-get install -y \
    python3-flask

# Setup environment.
RUN ln -s /usr/bin/clang-10 /usr/bin/clang
RUN ln -s /usr/bin/clang++-10 /usr/bin/clang++
ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++

# Switch user and working directory.
USER rds
WORKDIR /home/rds
COPY [".bashrc", "/home/rds/"]

# Define default command.
CMD ["bash"]
