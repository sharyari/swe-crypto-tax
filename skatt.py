#!/usr/bin/env python3
import datetime
import sys
import tabulate
import argparse

from cryptotax.kraken import parse_kraken_csv
from cryptotax.wallet import Wallet
from cryptotax.exchange_rate import ExchangeRate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tax Calculator for crypto', add_help=True)
    parser.add_argument('--kraken_file', dest='kraken_file', required=True, type=str, help='Path to kraken .csv')
    parser.add_argument('--tax_currency', dest='tax_currency', default='SEK', help='Currency used for taxing, only SEK atm')
    parser.add_argument('--fiscal_year', dest='fiscal_year', default=2020, type=int, help='The fiscal year. Max 2020 (2021 when exchange rates available)')
    parser.add_argument('--num_lines', dest='N', type=int, required=False, default=None, help='Number of lines to parse (debugging)')
    args = parser.parse_args()

    rates = ExchangeRate('EUR', args.tax_currency)
    wallet = Wallet(args.fiscal_year, rates, args.tax_currency)

    trs = list(parse_kraken_csv(args.kraken_file))

    N = len(trs)
    if args.N:
        N = args.N

    for tr in trs[:N]:
        wallet.transact(tr)

    print(wallet)
    all_rows = list(wallet.get_taxes())
    k4 = [["antal", "beteckning", "försäljningspris", "omkostnadsbelopp", "förlust", "vinst"]]
    k4.extend(all_rows)
    print(tabulate.tabulate(k4))