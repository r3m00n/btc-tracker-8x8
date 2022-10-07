import argparse
import requests

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

def getBtcPrice():
    source = requests.get("https://api.coinbase.com/v2/prices/spot?currency=USD").json()
    return source.get('data').get('amount')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=2, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=args.cascaded or 1, block_orientation=args.block_orientation,
                     rotate=args.rotate or 0, blocks_arranged_in_reverse_order=args.reverse_order)
    
    while True:
        btcPrice = getBtcPrice().replace(".", ",")
        if(len(btcPrice.split(",")[1]) == 1): btcPrice += "0"
        msg = btcPrice[:-6] + "." + btcPrice[-6:] + "$"
        print(msg)
        show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)