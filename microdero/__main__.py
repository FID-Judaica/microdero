# Copyright 2017, Goethe University
#
# This library is free software; you can redistribute it and/or
# modify it either under the terms of:
#
#   the EUPL, Version 1.1 or – as soon they will be approved by the
#   European Commission - subsequent versions of the EUPL (the
#   "Licence"). You may obtain a copy of the Licence at:
#   https://joinup.ec.europa.eu/software/page/eupl
#
# or
#
#   the terms of the Mozilla Public License, v. 2.0. If a copy of the
#   MPL was not distributed with this file, You can obtain one at
#   http://mozilla.org/MPL/2.0/.
#
# If you do not alter this notice, a recipient may use your version of
# this file under either the MPL or the EUPL.
import argparse
import deromanize
from .server import start_server


def main():
    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('config_file', help='a yaml config file for deromanize')
    add('-p', '--port', type=int, default=4891)
    add('-s', '--host', default='localhost')
    add('--path', help='path for a Unix socket')

    args = parser.parse_args()
    if args.path:
        args.host, args.port = None, None

    start_server(args.config_file,
                 deromanize.front_mid_end_decode,
                 auto_reload=True,
                 host=args.host,
                 port=args.port,
                 path=args.path)


if __name__ == '__main__':
    main()
