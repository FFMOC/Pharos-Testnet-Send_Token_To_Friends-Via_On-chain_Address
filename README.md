# Pharos Testnet — Send Tokens to Friends (On-chain Address)

This script automates the Pharos testing stage:
- Sends and confirms transactions
- Credits points
- Reduces manual work and speeds up the process

⚠️ This is a working prototype and can be improved for personal needs.

## 🚀 Quick Start

1. Clone the repository:
git clone https://github.com/FFMOC/Pharos-Testnet-Send_Token_To_Friends-Via_On-chain_Address.git

2. Create a virtual environment:
python -m venv venv

3. Install dependencies:
pip install -r requirements.txt

4. Configure environment variables:
Create a .env file in the project root and add:
```
RPC_URL = "https://testnet.dplabs-internal.com"   # You can use your own RPC
PRIVATE_KEY = "your private key"                  # Not sent anywhere; code is open
```
5. Run:
python SendOnChain.py

----------------------------------------------------------------------------------------------------------------------------------------------------------

# Pharos Testnet — Відправка токенів друзям (On-chain адреса)

Скрипт автоматизує етап тестування Pharos:
- Відправляє та підтверджує транзакції
- Нараховує поінти
- Зменшує ручну роботу та прискорює процес

⚠️ Це робочий прототип, його можна вдосконалювати під власні потреби.

## 🚀 Швидкий старт

1. Клонування репозиторію:
git clone https://github.com/FFMOC/Pharos-Testnet-Send_Token_To_Friends-Via_On-chain_Address.git

2. Створення віртуального середовища:
python -m venv venv

3. Встановлення залежностей:
pip install -r requirements.txt

4. Налаштування змінних середовища:
Створіть файл .env у кореневій папці проєкту та додайте:
```
RPC_URL = "https://testnet.dplabs-internal.com"   # Можете використати власний RPC
PRIVATE_KEY = "ваш приватний ключ"                # Не передається нікуди, код можна перевірити
```
5. Запуск:
python SendOnChain.py


