FROM python:latest

# see: https://github.com/seleniumbase/SeleniumBase/blob/84cbe3f88ece7164ed8fa1eec42cb0949a0d1398/Dockerfile#L2

# RUN apt-get clean && apt-get -y update && apt-get install -y chromium-driver

#======================
# Install Common Fonts
#======================
RUN apt-get update
RUN apt-get install -y \
    fonts-liberation \
    fonts-liberation2 \
    fonts-font-awesome \
    fonts-terminus \
    fonts-powerline \
    fonts-open-sans \
    fonts-mononoki \
    fonts-roboto \
    fonts-lato

#============================
# Install Linux Dependencies
#============================
RUN apt-get update
RUN apt-get install -y \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libu2f-udev \
    libvulkan1 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2

#==========================
# Install useful utilities
#==========================
RUN apt-get update
RUN apt-get install -y xdg-utils ca-certificates

#=================================
# Install Bash Command Line Tools
#=================================
RUN apt-get update
RUN apt-get -qy --no-install-recommends install \
    curl \
    sudo \
    unzip \
    vim \
    wget \
    xvfb

RUN apt-get update
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN seleniumbase get chromedriver --path

CMD ["python", "main.py"]