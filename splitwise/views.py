import datetime
import flask
import functools
from splitwise import app
from splitwise.api import splitwise
from flask.ext import restful
from flask.ext.restful import reqparse


def api_bool(value):
    if value in ('y', 't', 'true', 'yes', '1'):
        return 'true'
    else:
        return 'false'


def api_date(value):
    date = datetime.date(*[int(v) for v in value.split('-')])
    return date


class Api(restful.Api):
    def unauthorized(self, response):
        return response


class Resource(restful.Resource):
    pass


class Expenses(Resource):
    def get(self, expense_id=None):
        if expense_id:
            return self.get_expense(expense_id)
        else:
            return self.get_expenses()

    def get_expense(self, expense_id):
        return splitwise.get_expense(expense_id)

    def get_expenses(self):
        parser = reqparse.RequestParser()
        parser.add_argument('group_id', type=int)
        parser.add_argument('friendship_id', type=int)
        parser.add_argument('dated_after', type=api_date)
        parser.add_argument('dated_before', type=api_date)
        parser.add_argument('updated_after', type=api_date)
        parser.add_argument('updated_before', type=api_date)
        parser.add_argument('limit', type=int, default=20)
        parser.add_argument('offset', type=int, default=0)
        kwargs = parser.parse_args()

        if app.config.get('OFFLINE'):
            data = flask.json.load(open('offline/expenses.json'))
            expenses = data['expenses']

            if kwargs['group_id'] is not None:
                expenses = [e for e in expenses
                            if (e['group_id'] or 0) == kwargs['group_id']]

            if kwargs['offset']:
                expenses = expenses[kwargs['offset']:]

            if kwargs['limit']:
                expenses = expenses[:kwargs['limit']]

            data['expenses'] = expenses
            return data
        else:
            return splitwise.get_expenses(kwargs)

    def put(self):
        parser = reqparse.RequestParser()
        if flask.request.values.get('input'):
            parser.add_argument('input', type=str, required=True)
            parser.add_argument('group_id', type=int)
            parser.add_argument('friend_id', type=int)
            parser.add_argument('autosave', type=api_bool)
            return splitwise.parse_sentence(parser.parse_args())

        else:
            parser.add_argument('payment', type=float, required=True)
            parser.add_argument('cost', type=float, required=True)
            parser.add_argument('description', type=str, required=True)
            parser.add_argument('group_id', type=int)
            parser.add_argument('friendship_id', type=int)
            parser.add_argument('details', type=str)
            parser.add_argument(
                'creation_method', type=str,
                choices=('iou', 'quickadd', 'payment', 'split'))
            parser.add_argument('date', type=str)
            parser.add_argument(
                'repeat_interval', type=str,
                choices=('never', 'weekly', 'fortnightly',
                         'monthly', 'yearly'))
            parser.add_argument('currency_code', type=str)
            parser.add_argument('category_id', type=int)

            for i in range(10):
                for param in ('user_id', 'first_name', 'last_name', 'email',
                              'paid_share', 'owed_share'):
                    parser.add_argument('users__%d__%s' % (i, param), type=str)

            return splitwise.create_expense(parser.parse_args())

    def delete(self, expense_id):
        return splitwise.delete_expense(expense_id)

    def post(self, expense_id):
        parser = reqparse.RequestParser()
        parser.add_argument('group_id', type=int)
        parser.add_argument('friendship_id', type=int)
        parser.add_argument('expense_bundle_id', type=int)
        parser.add_argument('description', type=str)
        parser.add_argument('details', type=str)
        parser.add_argument('payment', type=int)
        parser.add_argument('cost', type=int)
        parser.add_argument('date', type=api_date)
        parser.add_argument('category_id', type=int)
        parser.add_argument('users__user_id', type=int)
        parser.add_argument('users__paid_share', type=int)
        parser.add_argument('users__owed_share', type=int)
        return splitwise.update_expense(expense_id, parser.parse_args())


class User(Resource):
    def get(self, user_id=None):
        if user_id:
            return splitwise.get_user(user_id)
        else:
            return splitwise.get_current_user()

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('locale', type=str)
        parser.add_argument('date_format', type=str)
        parser.add_argument('default_currency', type=str)
        parser.add_argument('default_group_id', type=int)

        parser.add_argument('notification_settings__added_as_friend',
                            type=api_bool)
        parser.add_argument('notification_settings__added_to_group',
                            type=api_bool)
        parser.add_argument('notification_settings__expense_added',
                            type=api_bool)
        parser.add_argument('notification_settings__expense_updated',
                            type=api_bool)
        parser.add_argument('notification_settings__bills', type=api_bool)
        parser.add_argument('notification_settings__payments', type=api_bool)
        parser.add_argument('notification_settings__monthly_summary',
                            type=api_bool)
        parser.add_argument('notification_settings__announcements',
                            type=api_bool)

        return splitwise.update_user(user_id, parser.parse_args())


class Groups(Resource):
    def get(self, group_id=None):
        if group_id:
            return self.get_group(group_id)
        else:
            return self.get_groups()

    def get_group(self, group_id):
        if app.config.get('OFFLINE'):
            groups = flask.json.load(open('offline/groups.json'))
            for group in groups:
                if group['id'] == group_id:
                    return group
            else:
                return groups[0]
        else:
            return splitwise.get_group(group_id)

    def get_groups(self):
        if app.config.get('OFFLINE'):
            return flask.json.load(open('offline/groups.json'))
        else:
            return splitwise.get_groups()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('group_type', type=str)
        parser.add_argument('country_code', type=str)
        for i in range(10):
            for param in ('first_name', 'last_name', 'email', 'user_id'):
                parser.add_argument('users__%d__%s' % (i, param), type=str)

        return splitwise.create_group(parser.parse_args())

    def delete(self, group_id):
        return splitwise.delete_group(group_id)


class GroupUser(Resource):
    def post(self, group_id, user_id=None):
        if user_id:
            kwargs = dict(user_id=user_id)
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', type=str, required=True)
            parser.add_argument('last_name', type=str, required=True)
            parser.add_argument('email', type=str, required=True)
            kwargs = parser.parse_args()

        return splitwise.add_user_to_group(group_id, kwargs).data

    def delete(self, group_id, user_id):
        return splitwise.remove_user_from_group(group_id, user_id).data


class Friends(Resource):
    def get(self, friend_id=None):
        if friend_id:
            return self.get_friend(friend_id)
        else:
            return self.get_friends()

    def get_friends(self):
        return splitwise.get_friends()

    def get_friend(self, friend_id):
        return splitwise.get_friend(friend_id)

    def delete(self, friend_id):
        return splitwise.delete_friend(friend_id)

    def post(self):
        parser = reqparse.RequestParser()
        if flask.request.values.get('user_first_name') \
                or flask.request.values.get('user_first_name'):
            parser.add_argument('user_first_name', type=str, required=True)
            parser.add_argument('user_last_name', type=str)
            parser.add_argument('user_email', type=str, required=True)
            return splitwise.create_friend(parser.parse_args())

        else:
            for i in range(10):
                parser.add_argument('friends__%d__user_first_name' % i,
                                    type=str)
                parser.add_argument('friends__%d__user_last_name' % i,
                                    type=str)
                parser.add_argument('friends__%d__user_email' % i, type=str)
            return splitwise.create_friends(parser.parse_args())


class Currencies(Resource):
    def get(self):
        if app.config.get('OFFLINE'):
            return flask.json.load(open('offline/currencies.json'))
        else:
            return splitwise.get_currencies()


class Categories(Resource):
    def get(self):
        return splitwise.get_categories()


rest_api = Api(app)
rest_api.add_resource(Expenses, '/expenses/', '/expenses/<int:expense_id>')
rest_api.add_resource(User, '/users/', '/users/<int:user_id>')
rest_api.add_resource(Groups, '/groups/', '/groups/<int:group_id>')
rest_api.add_resource(GroupUser, '/groups/<int:group_id>/user',
                      '/groups/<int:group_id>/user/<int:user_id>')
rest_api.add_resource(Currencies, '/currencies/')
rest_api.add_resource(Categories, '/categories/')
rest_api.add_resource(Friends, '/friends/', '/friends/<int:friend_id>')


def view_decorator(f):
    @functools.wraps(f)
    def _view_decorator(*args, **kwargs):
        context = dict()
        ret = f(context, *args, **kwargs)
        if not ret or isinstance(ret, dict):
            return flask.render_template('%s.html' % f.__name__, **context)
        else:
            return ret

    return _view_decorator


@app.route('/login/')
@app.errorhandler(401)
def login():
    next = flask.request.args.get('next') or flask.request.referrer
    callback_url = flask.url_for('authorized', next=next, _external=True)
    return splitwise.authorize(callback=callback_url)


@app.route('/')
@view_decorator
def index(context):
    pass


@app.route('/')
@view_decorator
def upload(context):
    pass


@app.route('/authorized/')
@splitwise.authorized_handler
def authorized(user):
    next_url = flask.request.args.get('next')
    if user:
        flask.session['user'] = user
        flask.flash('You are now logged in as %(first_name)s %(last_name)s'
                    % user)
    else:
        flask.abort(401)

    return flask.redirect(next_url or flask.url_for('index'))

