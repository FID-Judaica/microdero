import deromanize
import argparse
from .server import start_server


def main():
    import sys
    config_file = sys.argv[1]
    start_server(config_file,
                 deromanize.front_mid_end_decode,
                 auto_reload=True,
                 host='localhost',
                 port=4891)


if __name__ == '__main__':
    main()
