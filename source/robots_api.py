# -*- coding: utf-8 -*-
import re
import time

import requests


class LoginBot:

    LOGIN_URL = 'http://moonid.net/account/login/'

    def __init__(self, user, password):
        self.user = user
        self.password = password

        self.session = requests.Session()
        req1 = self.session.get(self.LOGIN_URL)
        parse_rule = re.compile(
            r'csrfmiddlewaretoken(\'|\")? value=(\'|\")(\w+)')
        self.params = {'csrfmiddlewaretoken': re.search(
            parse_rule, req1.text).groups()[2]}

        self.do_login(user, password)

    def do_login(self, user, password):
        params = self.params.copy()
        params.update({'username': user, 'password': password})
        self.session.post(self.LOGIN_URL, params)


class KnightFightFactory:

    class Bot(LoginBot):

        KF_LOGIN_URL = 'http://moonid.net/api/account/connect/140'
        BASE_URL = 'http://br2.knightfight.moonid.net/index.php'

        def do_login(self, user, password):
            super().do_login(user, password)
            self.session.get(self.KF_LOGIN_URL)

        def do_missions(self):
            return

            while True:
                self.do_login(self.user, self.password)
                self.session.get(self.BASE_URL + '?ac=job&filter=4')

                params = self.params.copy()
                req1 = self.session.get(self.BASE_URL + '?ac=raubzug')
                compare = '<select name="gesinnung" size="1" class="input">'

                if not compare in req1.text:
                    print('no more missions, stopping')
                    break

                params.update({'ac': 'raubzug',
                               'sac': 'mission',
                               'gesinnung': '2',
                               'jagdzeit': '10',
                               'x': '170',
                               'y': '30'})

                print('starting a new mission')
                self.session.post(self.BASE_URL, params)
                time.sleep(630)

        def go_to_work(self):
            req1 = self.session.get(self.BASE_URL + '?ac=job&filter=4')
            job_url = re.search(
                r'\?ac=job&amp;sac=startjob&amp;qid=\d+', req1.text).group().\
                replace('amp;', '')

            print('going to work')
            self.session.get(self.BASE_URL + job_url)

    @classmethod
    def make_bot(Class, user, password):
        return Class.Bot(user, password)
