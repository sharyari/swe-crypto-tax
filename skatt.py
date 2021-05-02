#!/usr/bin/env python3
import datetime
import sys
from copy import deepcopy

import tabulate
from cryptotax.kraken import parse_kraken_csv
from cryptotax.wallet import Wallet


if __name__ == '__main__':
    trs = list(parse_kraken_csv("trades.csv"))
    wallet = Wallet()
    N = int(sys.argv[1])
    for tr in trs[:N]:
#        print(tr)
        wallet.transact(tr)
#        print(wallet)
#        print("\n")
    tax_lines = list(wallet.aggregate_taxes())
    first_row = ["antal", "beteckning", "försäljningspris", "omkostnadsbelopp", "förlust", "vinst"]
    total_earn = sum([l[5] for l in tax_lines])
    total_loss = sum([l[4] for l in tax_lines])
    print(tabulate.tabulate(tax_lines))
    print("{} {} {}".format(total_earn, total_loss, total_earn-total_loss))
