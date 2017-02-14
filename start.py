#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zbot, config

# Server start
###
application = zbot.tornado.web.Application([
    (r"/", zbot.RootHandler),
    (r"/bot%s" % config.BOT_TOKEN, zbot.MainHandler)
], debug=True)

# Set WebHook
###
if __name__ == '__main__':
    while True:
        try:
            set_hook = zbot.api.get(config.URL + "setWebhook?url=%s" % config.MyURL)
            if set_hook.status_code != 200:
                logging.error("Can't set hook: %s. Quit." % set_hook.text)
                exit(1)

            application.listen(8888)
            zbot.tornado.ioloop.IOLoop.current().start()

        except KeyboardInterrupt:
            print("Goodbye.")
        break
