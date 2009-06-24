# Python module for Remember The Milk API
# http://intellectronica.net/python-rtm
# Free Software, released under the LGPLv3 License. See LICENSING.
# Author: Tom Berger <tom.berger@gmail.com>

from urllib import urlencode, urlopen
from md5 import md5
from simplejson import loads as parse_json


API_URL = 'http://api.rememberthemilk.com/services/rest/'
AUTH_URL = 'http://www.rememberthemilk.com/services/auth/'


class RTMError(Exception):
    pass


class MagicDict(dict):
    def __init__(self, *args, **kwargs):
        if kwargs:
            newdict = kwargs
        else:
            newdict = args[0]
        for k, v in newdict.items():
            if isinstance(v, dict):
                newdict[k] = MagicDict(v)
            elif isinstance(v, (list, tuple)):
                newlist = []
                for i in v:
                    if isinstance(i, dict):
                        newlist.append(MagicDict(i))
                    else:
                        newlist.append(i)
                newdict[k] = newlist
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k


class Category(object):
    def __init__(self, rtm, category_name):
        self.rtm = rtm
        self.category_name = category_name

    def __getattr__(self, attr):
        return Method(self.rtm, self.category_name, attr)


class Method(object):
    def __init__(self, rtm, category_name, method_name):
        self.rtm = rtm
        self.category_name = category_name
        self.method_name = method_name

    def __call__(self, **kwargs):
        return self.rtm.get(
            method='rtm.%s.%s' % (self.category_name, self.method_name),
            auth_token=self.rtm.token,
            **kwargs)


class RTMClient(object):
    def __init__(self, api_key, secret, token=None):
        self.api_key = api_key
        self.secret = secret
        self._token = token
        self._frob = None

    def __getattr__(self, attr):
        return Category(self, attr)

    def sign(self, params):
        data = self.secret +''.join(
            k + params[k] for k in sorted(params.keys()))
        return md5(data).hexdigest()

    def fetch(self, url, **kwargs):
        if kwargs:
            url = url + '?' + urlencode(kwargs)
        return urlopen(url).read()

    def get(self, **params):
        params['api_key'] = self.api_key
        params['format'] = 'json'
        params['api_sig'] = self.sign(params)

        json = self.fetch(API_URL, **params)

        data = MagicDict(parse_json(json))
        rsp = data.rsp

        if rsp.stat == 'fail':
            raise RTMError, '%s (%s)' % (
                rsp.err.msg, rsp.err.code)
        else:
            return rsp

    @property
    def auth_url(self):
        params = {
            'api_key': self.api_key,
            'perms'  : 'delete',
            'frob'   : self.frob
            }
        params['api_sig'] = self.sign(params)
        return AUTH_URL + '?' + urlencode(params)

    @property
    def token(self):
        if self._token is None:
            frob = self._frob
            rsp = self.get(method='rtm.auth.getToken', frob=frob)
            self._token = rsp.auth.token
        return self._token

    @property
    def frob(self):
        if self._frob is None:
            rsp = self.get(method='rtm.auth.getFrob')
            self._frob = rsp.frob
        return self._frob
