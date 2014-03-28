import flask
import urllib
import pprint
import oauth2
from splitwise import app
import functools


try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class OAuthException(Exception):
    pass


class SplitwiseApiResponse(object):
    def __init__(self, (response, raw_data)):
        content_type = response['content-type'].split(';')
        if len(content_type) == 2:
            content_type, encoding = content_type
            encoding = encoding.split('charset=')[1]
            raw_data = unicode(raw_data, encoding, 'replace')
        else:
            content_type = content_type[0]

        #assert content_type == 'application/json', (
        #    'Only application/json data is supported')
        if content_type != 'application/json':
            app.logger.error('Only application/json data is supported, got %r',
                             content_type)

        self.response = response
        self.raw_data = raw_data
        self.data = flask.json.loads(raw_data)

    def __getitem__(self, key):
        return self.data[key]

    @property
    def status(self):
        return int(self.response['status'])

    def __unicode__(self):
        return self.raw_data

    def __str__(self):
        return self.raw_data

    def __repr__(self):
        return '<%s[%s] %s>' % (
            self.__class__.__name__,
            self.status,
            pprint.pformat(self.data),
        )

    def __html__(self):
        return flask.jsonify(self.data)


class SplitwiseRemoteApp(object):
    # Splitwise api info
    API_VERSION = 3
    API_BASE_URL = 'https://secure.splitwise.com/'
    API_URL = API_BASE_URL + 'api/v%.1f/' % API_VERSION
    API_REQUEST_TOKEN_URL = API_URL + 'get_request_token'
    API_ACCESS_TOKEN_URL = API_URL + 'get_access_token'
    API_AUTHORIZE_URL = API_BASE_URL + 'authorize'

    def __init__(
            self,
            token_key=app.config['API_KEY'],
            token_secret=app.config['API_SECRET'],
            base_url=API_URL,
            request_token_url=API_REQUEST_TOKEN_URL,
            access_token_url=API_ACCESS_TOKEN_URL,
            authorize_url=API_AUTHORIZE_URL,
    ):
        self.token_key = token_key
        self.token_secret = token_secret
        self.base_url = base_url
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.consumer = oauth2.Consumer(key=token_key, secret=token_secret)

    @property
    def client(self):
        return oauth2.Client(self.consumer, self.token)

    def get_token(self):
        if not getattr(self, '_token', None):
            token_string = flask.session.get('token')
            if token_string:
                self.token = token_string

        return getattr(self, '_token', None)

    def set_token(self, token_or_string):
        if isinstance(token_or_string, basestring):
            if token_or_string:
                self._token = oauth2.Token.from_string(token_or_string)
        elif isinstance(token_or_string, oauth2.Token):
            self._token = token_or_string
            flask.session['token'] = token_or_string.to_string()
        else:
            raise TypeError('Unknown type %r, cannot convert %r to token' % (
                type(token_or_string), token_or_string))

    def del_token(self):
        self._token = None
        flask.session.pop('token', None)

    token = property(get_token, set_token, del_token,
                     ':type: :class:`oauth2.Token`')

    def request(self, url, method, body=''):
        url = urlparse.urljoin(self.base_url, url)
        app.logger.info('%s %s (%r)', method, url, body)
        response = SplitwiseApiResponse(self.client.request(url, method, body))
        if 200 <= response.status < 300:
            return response
        else:
            flask.abort(response.status)

    def get_url(self, url, **query):
        query = dict((k, v) for k, v in query.iteritems() if v)
        parsed = list(urlparse.urlparse(url))
        parsed[4] = urllib.urlencode(query)
        full_url = urlparse.urlunparse(parsed)
        return full_url

    def get_body(self, body):
        body = dict((k, v) for k, v in body.iteritems() if v is not None)
        return urllib.urlencode(body)

    def get(self, url, **query):
        return self.request(self.get_url(url, **query), 'GET')

    def post(self, url, **body_params):
        body = self.get_body(body_params)
        return self.request(url, 'POST', body)

    def put(self, url, **body_params):
        body = self.get_body(body_params)
        return self.request(url, 'PUT', body)

    def authorize(self, callback):
        client = oauth2.Client(self.consumer)
        response, content = client.request(self.request_token_url, 'POST')
        if int(response['status']) not in (200, 201):
            raise OAuthException(
                'Failed to generate request token, error: %r' % response)

        # Set the oauth_token and oauth_token_secret for the session
        request_token = dict(urlparse.parse_qsl(content))
        token = oauth2.Token(request_token['oauth_token'],
                             request_token['oauth_token_secret'])
        token.set_callback(callback)
        self.token = token
        return flask.redirect(self.get_url(
            self.authorize_url,
            oauth_token=token.key,
            oauth_callback=token.get_callback_url(),
        ))

    def authorized_handler(self, f):
        @functools.wraps(f)
        def authorized_handler():
            token = splitwise.token
            if not token:
                return self.authorize(flask.request.url)

            token.set_verifier(flask.request.args.get('auth_verifier'))
            splitwise.token = token

            response = self.get_current_user()
            return f(response)

        return authorized_handler

    # API methods
    def get_currencies(self):
        return self.get('get_currencies')['currencies']

    def get_categories(self):
        return self.get('get_categories')['categories']

    def parse_sentence(self, kwargs):
        assert kwargs.get('input'), '`input` is a required argument'
        return self.post('parse_sentence', **kwargs)

    # Users
    def get_current_user(self):
        return self.get('get_current_user')['user']

    def get_user(self, user_id):
        return self.get('get_user/%d' % user_id)['user']

    def update_user(self, user_id, kwargs):
        # TODO: According to the Splitwise API docs this should be PUT so it it
        # breaks, try that instead ;)
        return self.post('update_user/%d' % user_id, **kwargs)['user']

    # Groups
    def get_groups(self):
        return self.get('get_groups')['groups']

    def get_group(self, group_id):
        return self.get('get_group/%d' % group_id)['group']

    def create_group(self, kwargs):
        return self.get('create_group', **kwargs)['group']

    def delete_group(self, group_id):
        return self.post('delete_group/%d' % group_id)['success']

    def add_user_to_group(self, group_id, kwargs):
        return self.post('add_user_to_group', group_id=group_id, **kwargs).data

    def remove_user_from_group(self, group_id, user_id):
        return self.post('remove_user_from_group', group_id=group_id,
                         user_id=user_id)

    # Expenses
    def get_expenses(self, kwargs):
        return self.get('get_expenses', **kwargs)['expenses']

    def get_expense(self, expense_id):
        return self.get('get_expense/%d' % expense_id)['expense']

    def create_expense(self, kwargs):
        return self.post('create_expense', **kwargs).data

    def update_expense(self, expense_id, kwargs):
        print 'expense id', expense_id, kwargs
        return self.post('update_expense/%d' % expense_id, **kwargs)

    def delete_expense(self, expense_id):
        return self.get('delete_expense/%d' % expense_id)['success']

    # Friends
    def get_friends(self):
        return self.get('get_friends')['friends']

    def get_friend(self, friend_id):
        return self.get('get_friend/%d' % friend_id)['friend']

    def create_friend(self, kwargs):
        return self.get('create_friend', **kwargs)['friend']

    def create_friends(self, kwargs):
        return self.get('create_friends', **kwargs)['friends']

    def delete_friend(self, friend_id):
        return self.get('delete_friend/%d' % friend_id)['success']


splitwise = SplitwiseRemoteApp()
