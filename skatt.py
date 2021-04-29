#!/usr/bin/env python3
import datetime
import sys
from copy import deepcopy

from cryptotax.kraken import parse_kraken_csv
from cryptotax.wallet import Wallet


if __name__ == '__main__':
    trs = list(parse_kraken_csv("trades.csv"))
    wallet = Wallet()
    N = int(sys.argv[1])
    for tr in trs[:N]:
        print(tr)
        wallet.transact(tr)
        print(wallet)
        print("\n")
    print(wallet.taxes)
    print(sum(wallet.taxes))
