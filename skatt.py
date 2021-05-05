#!/usr/bin/env python3
import datetime
import sys
import tabulate
import argparse

from cryptotax.kraken import parse_kraken_csv
from cryptotax.wallet import Wallet
from cryptotax.exchange_rate import ExchangeRate
from cryptotax.coin import SEK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tax Calculator for crypto', add_help=True)
    parser.add_argument('--kraken_file', dest='kraken_file', required=True, type=str, help='Path to kraken .csv')
    parser.add_argument('--tax_currency', dest='tax_currency', default='SEK', help='Currency used for taxing, only SEK atm')
    parser.add_argument('--fiscal_year', dest='fiscal_year', default=2020, type=int, help='The fiscal year. Max 2020 (2021 when exchange rates available)')
    parser.add_argument('--num_lines', dest='N', type=int, required=False, default=None, help='Number of lines to parse (debugging)')
    parser.add_argument('--csv_export', dest='csv_export', default=None, help='Create a csv with the result')
    parser.add_argument('--precision', dest='precision', required=True, type=int, help='Precision of output values. Should be 0 when handing the data in, but should be higher if you actually want to know the real numbers')
    args = parser.parse_args()

    rates = ExchangeRate('EUR', args.tax_currency)
    wallet = Wallet(args.fiscal_year, rates, SEK)

    trs = list(parse_kraken_csv(args.kraken_file))

    N = len(trs)
    if args.N:
        N = args.N

    for tr in trs[:N]:
        wallet.transact(tr)

    print("End state of wallet. Negative fiat should be expected. Negative crypto indicates incomplete data or bug")
    print("\n".format(wallet))
    
    
    wallet.print_k4(filename=args.csv_export, precision=args.precision)