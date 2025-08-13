from functions.transact import transaction
from headers.SendOnChain_headers import headers
from dotenv import load_dotenv
import requests
import os
from web3 import Web3
import random
import time
from typing import Tuple

# -----------------------
# Constants | Константи
# -----------------------
SLEEP_SECONDS_MIN = 1       # EN: minimum random delay between tx; UA: мінімальна випадкова пауза між транзакціями
SLEEP_SECONDS_MAX = 10      # EN: maximum random delay between tx; UA: максимальна випадкова пауза між транзакціями
VERIFY_URL = "https://api.pharosnetwork.xyz/task/verify"  # EN/UA: verification endpoint | endpoint верифікації
TASK_ID = 103               # EN/UA: task identifier used in verification | ідентифікатор завдання для верифікації

# EN: Load .env, connect to RPC, derive account address from PRIVATE_KEY.
# UA: Завантажити .env, під’єднатися до RPC, отримати адресу з PRIVATE_KEY.
def load_env_and_connect() -> Tuple[Web3, str, str]:
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    private_key = os.getenv("PRIVATE_KEY")

    if not rpc_url:
        raise RuntimeError("❌ RPC_URL not found in environment (.env).")
    if not private_key:
        raise RuntimeError("❌ PRIVATE_KEY not found in environment (.env).")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise RuntimeError("❌ Unable to connect to the network.")

    # EN: Derive checksum address from private key (explicit).
    # UA: Отримуємо checksum-адресу з приватного ключа (явно).
    account = Web3.to_checksum_address(web3.eth.account.from_key(private_key).address)
    return web3, private_key, account


# EN: Read recipient; blank = send to self (original behavior).
# UA: Зчитати адресу отримувача; порожньо = надсилаємо собі (оригінальна поведінка).
def read_address_input(default_account: str) -> str:
    raw = input("Enter address to send tokens (leave blank to send to yourself): ").strip()
    if len(raw) == 0:
        return default_account
    try:
        return Web3.to_checksum_address(raw)
    except ValueError:
        raise ValueError("❌ Invalid address: cannot convert to checksum format.")


# EN: Read amount in ETH and return wei as int.
#     If user enters 0 -> random in [0.000001 .. 0.0001] ETH, step 0.000001.
#     IMPORTANT: keep truncation logic (int(eth * 1e18)) exactly as original.
# UA: Зчитати суму в ETH і повернути wei як int.
#     Якщо користувач вводить 0 -> випадково в [0.000001 .. 0.0001] ETH, крок 0.000001.
#     ВАЖЛИВО: залишаємо логіку ТРАНКУВАННЯ (int(eth * 1e18)) як в оригіналі.
def read_amount_wei() -> int:
    raw = input("Enter amount to send (enter 0 for random between 0.000001 and 0.0001 ETH): ").strip()
    try:
        eth_value = float(raw)
    except ValueError:
        raise ValueError("❌ Amount must be a number (e.g., 0.001).")

    if eth_value != 0.0:
        return int(eth_value * 10**18)  # truncation preserved | збережено транкування

    random_eth = (random.randint(1, 100) / 1_000_000.0)  # EN/UA: [1e-6 .. 1e-4] ETH
    return int(random_eth * 10**18)  # truncation preserved | збережено транкування


# EN: Read number of transactions from user (must be positive integer).
# UA: Зчитати кількість транзакцій від користувача (додатне ціле число).
def read_num_transactions() -> int:
    raw = input("Enter number of transactions to send: ").strip()
    if not raw.isdigit():
        raise ValueError("❌ Number of transactions must be a positive integer.")
    num = int(raw)
    if num <= 0:
        raise ValueError("❌ Number of transactions must be greater than 0.")
    return num


# EN: Send a single transaction (data='0x' preserved) and verify via POST to VERIFY_URL.
#     Returns True if server msg == 'task verified successfully', else False.
# UA: Відправити одну транзакцію (data='0x' без змін) і верифікувати через POST на VERIFY_URL.
#     Повертає True, якщо msg == 'task verified successfully', інакше False.
def send_and_verify_once(
    web3: Web3,
    private_key: str,
    from_account: str,
    to_address: str,
    wei_value: int,
    http_session: requests.Session
) -> bool:
    tx_hash = transaction(web3, private_key, to_address, "0x", wei_value)

    json_data = {
        "address": from_account,
        "task_id": TASK_ID,
        "tx_hash": tx_hash,
    }

    try:
        resp = http_session.post(VERIFY_URL, headers=headers, json=json_data, timeout=30)
        resp.raise_for_status()  # EN: bubble up 4xx/5xx; UA: дає зрозумілу помилку при 4xx/5xx
        data = resp.json()
    except requests.RequestException as e:
        print(f"❌ Verification error (network/HTTP): {e}")
        return False
    except ValueError:
        print("❌ Failed to parse verification JSON response.")
        return False

    return data.get("msg") == "task verified successfully"


# EN: Orchestrate inputs and loop; keeps original timing and verification logic.
# UA: Оркестрація інпутів і циклу; зберігає оригінальні паузи та логіку верифікації.
def main() -> None:
    web3, private_key, account = load_env_and_connect()
    to_address = read_address_input(account)
    wei_value = read_amount_wei()
    num_transactions = read_num_transactions()

    with requests.Session() as session:
        for i in range(num_transactions):
            print(f"Transaction {i+1} begin")

            try:
                ok = send_and_verify_once(web3, private_key, account, to_address, wei_value, session)
            except Exception as e:
                # EN: guard against unexpected runtime errors during a single tx.
                # UA: захист від неочікуваних помилок під час однієї транзакції.
                print(f"❌ Error while sending transaction: {e}")
                ok = False

            if ok:
                print("✅ Task verified successfully")
            else:
                print("❌ Task verification failed")

            print(f"Transaction {i+1} end\n")
            time.sleep(random.randint(SLEEP_SECONDS_MIN, SLEEP_SECONDS_MAX))  # EN/UA: random pause


if __name__ == "__main__":
    main()
