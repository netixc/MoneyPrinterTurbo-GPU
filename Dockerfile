# Use NVIDIA CUDA devel image (needed for NVENC compilation)
FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /MoneyPrinterTurbo

# Set directory permissions
RUN chmod 777 /MoneyPrinterTurbo

ENV PYTHONPATH="/MoneyPrinterTurbo"
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Install build dependencies and Python 3.11
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    git \
    imagemagick \
    build-essential \
    yasm \
    pkg-config \
    libx264-dev \
    libx265-dev \
    libnuma-dev \
    libvpx-dev \
    libfdk-aac-dev \
    libmp3lame-dev \
    libopus-dev \
    libass-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install NVIDIA Video Codec SDK headers
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git /tmp/nv-codec-headers \
    && cd /tmp/nv-codec-headers \
    && make install \
    && cd / \
    && rm -rf /tmp/nv-codec-headers

# Download and compile FFmpeg with NVENC support
RUN wget -O /tmp/ffmpeg.tar.bz2 https://ffmpeg.org/releases/ffmpeg-7.1.tar.bz2 \
    && tar -xjf /tmp/ffmpeg.tar.bz2 -C /tmp \
    && cd /tmp/ffmpeg-7.1 \
    && ./configure \
        --prefix=/usr/local \
        --enable-gpl \
        --enable-nonfree \
        --enable-cuda-nvcc \
        --enable-libnpp \
        --enable-nvenc \
        --enable-cuvid \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libvpx \
        --enable-libfdk-aac \
        --enable-libmp3lame \
        --enable-libopus \
        --enable-libass \
        --enable-libfreetype \
        --enable-gnutls \
        --extra-cflags=-I/usr/local/cuda/include \
        --extra-ldflags=-L/usr/local/cuda/lib64 \
    && make -j$(nproc) \
    && make install \
    && ldconfig \
    && cd / \
    && rm -rf /tmp/ffmpeg-7.1 /tmp/ffmpeg.tar.bz2

# Set Python 3.11 as default and link custom FFmpeg
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && ln -sf /usr/local/bin/ffmpeg /usr/bin/ffmpeg \
    && ln -sf /usr/local/bin/ffprobe /usr/bin/ffprobe

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Fix security policy for ImageMagick
RUN sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --ignore-installed blinker -r requirements.txt

# Replace imageio_ffmpeg bundled binary with our custom NVENC-enabled FFmpeg
RUN ln -sf /usr/local/bin/ffmpeg /usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2

# Now copy the rest of the codebase into the image
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "./webui/Main.py","--browser.serverAddress=127.0.0.1","--server.enableCORS=True","--browser.gatherUsageStats=False"]
