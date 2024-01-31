import csv
from typing import Any

from web3 import Web3

from rpcs import RPCS


def get_wallets() -> list[str] | bool:
    wallets = []

    with open('wallets.txt', 'r') as file:
        for line in file:
            wallets.append(line.strip())

    if wallets:
        return wallets
    else:
        print("wallets.txt - is empty")
        return False


def get_native_balances(wallet: str) -> bool | dict[str | Any, str | Any]:
    balances = {"wallet": wallet}

    for network, rpc in RPCS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            address_checksum = Web3.to_checksum_address(wallet)

            balance_native_token_wei = w3.eth.get_balance(address_checksum)
            balance_native_token = balance_native_token_wei / 10 ** 18
            balances[network] = round(balance_native_token, 4)

        except Exception as error:
            print(f"Something wrong | {error}")
            return False

    return balances


def main():
    wallets = get_wallets()

    if wallets:
        with open('balances.csv', 'w', newline='') as csvfile:
            fieldnames = ["wallet"] + list(RPCS.keys())
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csv_writer.writeheader()

            for wallet in wallets:
                balances = get_native_balances(wallet)
                if balances:
                    csv_writer.writerow(balances)


if __name__ == '__main__':
    main()
