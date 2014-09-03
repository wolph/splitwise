import flask
import urllib
import pprint
import requests_oauthlib
from splitwise import app
import functools
from flask.ext import restful


class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SplitwiseApiResponse):
            return obj.data

        return flask.json.JSONEncoder.default(self, obj)


restful.representations.json.settings['cls'] = JSONEncoder
app.json_encoder = JSONEncoder

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class OAuthException(Exception):
    pass


class NotLoggedInException(OAuthException):
    ERROR = 'Invalid API Request: you are not logged in'


class SplitwiseApiResponse(object):
    def __init__(self, response):
        self.response = response
        self.raw_data = response.text
        try:
            self.data = response.json()
        except ValueError:
            app.logger.error('Non-JSON response from the API, got:\n%s' %
                             response.text)
            raise

        if self.data.get('error') == NotLoggedInException.ERROR:
            raise NotLoggedInException(self)
        elif self.data.get('error'):
            app.logger.error('Got error: %s', self.data['error'])

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def status(self):
        return int(self.response.status_code)

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
            token_key=app.config.get('API_KEY'),
            token_secret=app.config.get('API_SECRET'),
            base_url=API_URL,
            request_token_url=API_REQUEST_TOKEN_URL,
            access_token_url=API_ACCESS_TOKEN_URL,
            authorize_url=API_AUTHORIZE_URL,
            callback_url=None,
    ):
        self.base_url = base_url
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.callback_url = callback_url
        self.token_key = token_key
        self.token_secret = token_secret

    @property
    def client(self):
        return self.get_client()

    def get_client(self, callback_url=None):
        callback_url = (callback_url or
                        flask.url_for('authorized', _external=True))
        return requests_oauthlib.OAuth1Session(
            self.token_key,
            client_secret=self.token_secret,
            verifier=flask.session.get('oauth_verifier'),
            resource_owner_key=flask.session.get('oauth_token'),
            resource_owner_secret=flask.session.get('oauth_token_secret'),
            callback_uri=callback_url or self.callback_url,
        )

    def request(self, url, method, data=None):
        assert self.token_key and self.token_secret, (
            'Dont forget to set the  `API_KEY` and `API_SECRET` in the config')
        url = urlparse.urljoin(self.base_url, url)
        app.logger.info('[%s] %s %r', method, url, data)

        raw_response = self.client.request(method, url, data)
        response = SplitwiseApiResponse(raw_response)

        return response

    def get_url(self, url, **query):
        query = dict((k, v) for k, v in query.iteritems() if v is not None)
        parsed = list(urlparse.urlparse(url))
        parsed[4] = urllib.urlencode(query)
        full_url = urlparse.urlunparse(parsed)
        return full_url

    def get_body(self, body):
        body = dict((k, v) for k, v in body.iteritems() if v is not None)
        return urllib.urlencode(body)

    def get(self, url, **query):
        url = self.get_url(url, **query)
        return self.request(url, 'GET')

    def post(self, url, **body_params):
        return self.request(url, 'POST', body_params)

    def put(self, url, **body_params):
        return self.request(url, 'PUT', body_params)

    def logout(self):
        for k in ('oauth_token', 'oauth_token_secret', 'oauth_verifier'):
            if k in flask.session:
                del flask.session[k]

    def authorize(self, callback=None):
        self.logout()
        client = self.get_client(callback)
        response = client.fetch_request_token(self.request_token_url)
        flask.session['oauth_token'] = response['oauth_token']
        flask.session['oauth_token_secret'] = response['oauth_token_secret']
        return flask.redirect(client.authorization_url(self.authorize_url))

    def authorized_handler(self, f):
        @functools.wraps(f)
        def authorized_handler():
            if not flask.session.get('oauth_token_secret'):
                return self.authorize(flask.request.url)

            response = self.client.parse_authorization_response(
                flask.request.url)
            flask.session['oauth_verifier'] = response['oauth_verifier']

            response = splitwise.client.fetch_access_token(
                splitwise.access_token_url)
            flask.session['oauth_token'] = response['oauth_token']
            flask.session['oauth_token_secret'] = response['oauth_token_secret']

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
        expenses = self.get('get_expenses', **kwargs)
        if expenses.get('error'):
            return expenses

        count = len(expenses['expenses'])
        total = count + kwargs['offset']
        if count == kwargs['limit']:
            total += 1
        expenses['total'] = total
        for expense in expenses['expenses']:
            expense['group_id'] = expense['group_id'] or 0
        return expenses

    def get_expense(self, expense_id):
        return dict(
            expenses=[self.get('get_expense/%d' % expense_id)['expense']])

    def create_expense(self, kwargs):
        return self.post('create_expense', **kwargs).data

    def update_expense(self, expense_id, kwargs):
        return self.get('update_expense/%d' % expense_id, **kwargs).data

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


class SplitwiseFlaskApp(SplitwiseRemoteApp):
    def request(self, url, method, body=''):
        try:
            response = SplitwiseRemoteApp.request(self, url, method, body)
        except NotLoggedInException:
            flask.abort(401)

        if 200 <= response.status < 300:
            return response
        else:
            flask.abort(response.status, response=response.data)


splitwise = SplitwiseFlaskApp()

