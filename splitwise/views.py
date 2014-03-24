import flask
import functools
from splitwise import app
from splitwise.api import splitwise
from flask.ext import restful


class Api(restful.Api):
    def unauthorized(self, response):
        return response


class Resource(restful.Resource):
    pass


class Expenses(Resource):
    def get(self):
        return splitwise.get_expenses()
        return flask.json.load(open('expenses.json'))['expenses']


class Expense(Resource):
    def get(self, expense_id):
        expenses = flask.json.load(open('expenses.json'))
        for expense in expenses['expenses']:
            if expense_id == expense['id']:
                return expense


class Users(Resource):
    def get(self, user_id=None):
        if user_id:
            return splitwise.get_user(user_id)
        else:
            return splitwise.get_current_user()


class Groups(Resource):
    def get(self):
        return splitwise.get_groups()


class Group(Resource):
    def get(self, group_id):
        return splitwise.get_group(group_id)


rest_api = Api(app)
rest_api.add_resource(Expenses, '/expenses/')
rest_api.add_resource(Expense, '/expenses/<int:expense_id>/')
rest_api.add_resource(Users, '/users/')
rest_api.add_resource(Groups, '/groups/')
rest_api.add_resource(Group, '/groups/<int:group_id>')


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
@app.errorhandler(403)
def login():
    next = flask.request.args.get('next') or flask.request.referrer
    callback_url = flask.url_for('authorized', next=next, _external=True)
    return splitwise.authorize(callback=callback_url)


@app.route('/')
@view_decorator
def index(context):
    #context['expenses'] = splitwise.get_expenses()
    context['expenses'] = flask.json.load(open('expenses.json'))


@app.route('/authorized/')
@splitwise.authorized_handler
def authorized(response):
    next_url = flask.request.args.get('next')
    if response is None:
        flask.flash(u'You need to give permission to use this app.')
    else:
        flask.session['user'] = response['user']
        flask.flash('You are now logged in as %(first_name)s %(last_name)s'
                    % response['user'])

    return flask.redirect(next_url or flask.url_for('index'))

