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
import asyncio
import deromanize
import functools
import json
import pathlib
import yaml
from aiohttp import web
dump = functools.partial(json.dumps, ensure_ascii=False, separators=(',', ':'))


class Server:
    def __init__(self, profile_path, derom_function=None, auto_reload=False):
        """microdero.Server for shooting deromanized json around the internet

            - profile_path: yaml profile for a key generator.
            - derom_function: function that takes a KeyGenerator and a word as
              input and returns ReplacementList.
        """
        self.profile_path = pathlib.Path(profile_path)
        self.getkeys()
        self.derom = derom_function
        self.reload = auto_reload

        self.app = web.Application()
        self.run = functools.partial(web.run_app, self.app)
        self.routes()

    def routes(self):
        """aiohttp routes defined here. Override this method if you wish to use
        custom routes.
        Default routes:

            self.app.router.add_get('/{word}', self.simple)
            self.app.router.add_post('/', self.post)
        """
        self.app.router.add_get('/{word}', self.simple)
        self.app.router.add_post('/', self.post)

    def getkeys(self):
        self.profile_mtime = self.profile_path.stat().st_mtime
        self.keys = deromanize.KeyGenerator(
            yaml.safe_load(open(self.profile_path)))

    async def decode(self, word, stat=True):
        if self.reload:
            new_mtime = self.profile_path.stat().st_mtime
            if self.profile_mtime != new_mtime:
                self.getkeys()
                await asyncio.sleep(0)
        decoded = self.derom(self.keys, word)
        await asyncio.sleep(0)
        decoded.prune()
        if stat:
            decoded.makestat()
        return decoded.serializable()

    async def simple(self, request):
        word = request.match_info['word']
        return web.Response(text=dump(await self.decode(word)))

    async def post(self, request):
        data = await request.post()
        words = data.get('words')
        word = data.get('word')
        kwargs = {}
        if data.get('raw'):
            kwargs['stat'] = False
        if words:
            words = json.loads(words)
            responce = []
            for word in words:
                responce.append(await self.decode(word, **kwargs))
        elif word:
            responce = await self.decode(word, **kwargs)

        return web.Response(text=dump(responce))


def start_server(profile_path, derom_function, *args,
                 auto_reload=False, **kwargs):
    """
    - profile_path: yaml profile for a key generator.
    - derom_function: function that takes a KeyGenerator and a word as
      input and returns ReplacementList.

    *args and **kwargs are passed on to aiohttp.web.run_app()
    """
    myserver = Server(profile_path, derom_function)
    myserver.run(*args, **kwargs)
