#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import robots_api


def main():
    args = argparse.ArgumentParser(description='RedMoon Bot')
    args.add_argument('-b', '--bot', type=str, help='Bot class')
    args.add_argument('-u', '--user', type=str, help='User name')
    args.add_argument('-p', '--password', type=str, help='User passwd')

    kwargs = vars(args.parse_args())
    bot = kwargs.pop('bot')
    BotFactoryClass = getattr(robots_api, bot + 'Factory')

    create_bot(BotFactoryClass, **kwargs)


def create_bot(factory, user, password):
    bot = factory.make_bot(user, password)
    bot.do_missions()
    bot.go_to_work()
    return bot


if __name__ == '__main__':
    main()
