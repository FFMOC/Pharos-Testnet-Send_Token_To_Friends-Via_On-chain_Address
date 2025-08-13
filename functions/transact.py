from eth_account import Account

def transaction(web3, PRIVATE_KEY, TO, data, value=0):
    account = Account.from_key(PRIVATE_KEY)
    from_address = account.address


    nonce = web3.eth.get_transaction_count(from_address)
    chain_id = web3.eth.chain_id
    gas_price = web3.eth.gas_price

    tx = {
        "from": from_address,
        "to": TO,
        "value": value,
        "data": data,
        "nonce": nonce,
        "chainId": chain_id,
        "gasPrice": gas_price,
    }

    estimated_gas = web3.eth.estimate_gas(tx)
    tx["gas"] = estimated_gas

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"🚀 Send transaction: {web3.to_hex(tx_hash)}")

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    status = "✅ Transaction Successfully" if receipt.status == 1 else "❌ Transaction Failed"
    print(f"{status} | Block: {receipt.blockNumber} | Gas: {receipt.gasUsed}")

    return web3.to_hex(tx_hash)


    