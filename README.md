# There are no guarantees of correctness given here, and you shouldn't be expecting it from random github project either. DYOR! This is written by someone who doesn't know economics and it's all just a hack.

# What does this do, and does it work in my country?
This program was written in order to generate tax information for a swedish tax declaration (k4). They don't require anything fancy or special, so it's not unlikely that this would work for some other country as well.

The input to this program should be the *full* transaction history, or at least start from some point before the start of the fiscal year where you know you did not have any crypto. Otherwise the calculations will lead to *higher* taxes.
Given this data, it will simulate all the transactions and for each crypto currency keep track of the average cost of crypto. Each time crypto is sold it generates a *taxevent* and saved internally.
The program does not return all tax events, but instead two lines for each crypto:
1. The aggregated cost of buying and selling crypto X for each taxevent that lead to a net profit (at the time it happened)
1. The aggregated cost of buying and selling crypto X for each taxevent that lead to a net loss

Swedish law does not (to my knowledge) require anything fancy at all, so this might be what you need for your country as well. If so, you would still need to provide the program with lists of exchange rates.

# What doesn't it do?
1. Calculate things correctly. You should at least assume it doesn't
1. This program cannot handle transactions where cryto was sold for some other crypto (e.g. BTC for ETH).
1. Calculate correctly given incomplete transaction history (if you're declaring for 2020 and you bought crypto in 2018, the cost at that time is important)
1. Handle staking rewards (I don't have access to such data. My guess would be that doing nothing at all to handle them actually is the correct calculation, but I havn't thought it through)

# Accepted input
1. Kraken transactions (in their format)
1. Binance transactions (ongoing)
1. I've tried to isolate this, so given a transaction list from some other source, it could be easy to extend. Send it to me

# Exchange Rates

The program requires exchange rate information between the crypto currency you want to declare in (e.g. SEK) and the currency used for the transaction. It has built-in support for EUR/SEK, other exchange rates can be added.
Let's say the taxes to be declared are in AUD, and the transactions being made are in USD, then creating a file USDAUD.csv or AUDUSD.csv with the same format as the existing EURSEK.csv would do the trick.


# Notes about swedish tax rules
## Schablonmodellen
Swedish rules for stocks allow for something called "schablonmodellen" - if the prior cost is unknown, one may pay 20% of the total sell-price in taxes. This does NOT apply to crypto currencies


## Currency denominations and amount precision
It may be nice to know that the tax office does not
1. accept float numbers (they admit to this being a flaw on their side)
1. care about the denominations used
1. care about the actual amounts of crypto (just the cost)
So if you sold 0.01 BTC, you have to declare that as 1 BTC. But since they don't care about the denomination either, this program will convert it to mBTC, i.e. 0.01 BTC => 10 mBTC.


## Questions
Call the tax office if you have questions. It's not like a regular support number, they're both nice and helpful!

