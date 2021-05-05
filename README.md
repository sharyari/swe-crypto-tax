# swe-crypto-tax
Calculate taxable events given the transaction history

At the moment, this requires that the starting point is a state where there are no crypto in the wallet. This could be the beginning of the wallet.
If not, one would have to start from a point in time where the average cost of all cryptos are known.


# Notes
Swedish rules for stocks allow for something called "schablonmodellen" - if the prior cost is unknown, one may pay 20% of the total sell-price in taxes. This does NOT apply to crypto currencies

The tax offices does not
1. accept float numbers (anywhere)
1. care about the denominations used
1. care about the actual amounts of crypto (just the cost)
So if you sold 0.01 BTC, you have to declare that as 1 BTC. But since they don't care about the denomination either, this program will convert it to mBTC, i.e. 0.01 BTC => 10 mBTC.

