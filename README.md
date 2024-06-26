<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-06-10 18:31:13
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2024-04-13 10:36:13
 * @FilePath: \tradingview_to_exchange\README.md
 * @Description: 
-->
# tradingview to exchange(TV2EX) BOT

![GitHub](https://img.shields.io/github/license/hibana2077/tradingview_to_exchange)
![GitHub last commit](https://img.shields.io/github/last-commit/hibana2077/tradingview_to_exchange)
![GitHub issues](https://img.shields.io/github/issues/hibana2077/tradingview_to_exchange)
![GitHub stars](https://img.shields.io/github/stars/hibana2077/tradingview_to_exchange?style=social)
![GitHub forks](https://img.shields.io/github/forks/hibana2077/tradingview_to_exchange?style=social)

English | [中文](./doc/README_TW.md)

## Introduction

![Python](https://img.shields.io/badge/python-3.11-blue?style=plastic-square&logo=python)
![Astro](https://img.shields.io/badge/Astro-latest-FFD700?style=plastic-square&logo=astro)
![Fastapi](https://img.shields.io/badge/fastapi-latest-009688?style=plastic-square&logo=fastapi)
![Mongodb](https://img.shields.io/badge/mongodb-latest-47A248?style=plastic-square&logo=mongodb)
![Openai](https://img.shields.io/badge/openai-latest-412991?style=plastic-square&logo=openai)
![Docker](https://img.shields.io/badge/docker-latest-2496ED?style=plastic-square&logo=docker)
[![Binance](https://img.shields.io/badge/binance--%2d10%25-F0B90B?style=plastic-square&logo=binance)](https://www.binance.com/en/activity/referral-entry/MYB23J?fromActivityPage=true&ref=LIMIT_TJMU1KAZ)
[![Okex](https://img.shields.io/badge/okex--%2d10%25-000000?style=plastic-square&logo=okex)](https://www.okx.com/join/18323483)

This is a Crypto trading bot that can automatically trade on the exchange based on the tradingview alert.

User only need to deploy docker image on the server and set the tradingview alert to the bot.

## Features

- [x] Support Spot Trading and Futures Trading
- [x] Support Binance, Okex
- [x] Support multiple trading pairs
- [x] Support multiple trading strategies

## Installation

### 1. Install Docker

- [Install Docker](https://docs.docker.com/engine/install/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Clone the repository

```bash
git clone https://github.com/hibana2077/tradingview_to_exchange
```

### 3. Run the docker-compose

```bash
cd tradingview_to_exchange
docker-compose up -d
```

You can set account information in the `docker-compose.yml` file.

### 4. Setup firewall

- Open port 80 and 27017 on the server

### 5. Login to the web

- Open the browser and clikc the [link](https://hibana2077-gpt-news-generator-srcmain-0osgu0.streamlit.app/)
- Login with the default account and password and host address(if you don't change the account information in the `docker-compose.yml` file)
    - Account: admin
    - Password: admin
    - Host: IP address of the server

