"""
Strategy

Entry: If stock gaps down below the low of the previous day when it opens.

Taking Profits: Take profit on the first profitable openining. This means wait to sell until the stock has actually opened higher than the latest entry.

"""


import config
import logging
import alpaca_trade_api as ata
from datetime import datetime as dt

api = ata.REST(key_id=config.API_KEY_ID, secret_key=config.API_SECRET)

logging.basicConfig(level=logging.INFO, filename='alpaca_gap_down_bot.log',
                    format='%(asctime)s:%(levelname)s:%(message)s', )

SYMBOL = 'MSFT'
QUANTITY = 1

in_position = False
buy_price = 0

while True:
    # Get prices 1 minute after nyse opens
    if dt.utcnow().hour-4 == 9 and dt.utcnow().minute == 31:
        market_data = api.get_bars(symbol=SYMBOL, timeframe=ata.rest.TimeFrame.Day, limit=2)
        previous_low = market_data[0].l
        current_open = market_data[1].o

        if not in_position:
            if current_open < previous_low:
                try:
                    buy_order = api.submit_order(symbol=SYMBOL, qty=QUANTITY, side='buy', type='market')
                    buy_price = current_open
                    in_position = True
                    logging.info(f'{buy_order}')
                except Exception as e:
                    logging.error(f'{e}')
        else:
            if current_open > buy_price:
                try:
                    sell_order = api.submit_order(symbol=SYMBOL, qty=QUANTITY, side='sell', type='market')
                    in_position = False
                    logging.info(f'{sell_order}')
                except Exception as e:
                    logging.error(f'{e}')
