#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
from datetime import datetime
import pytz
from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieves a user based on a user id.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Performs some routines before each request's resolution.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.
    """
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    """Retrieves the timezone for a web page.
    """
    timezone = request.args.get('timezone', '').strip()
    if timezone:
        try:
            pytz.timezone(timezone)  # Validate the timezone
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user and g.user.get('timezone'):
        timezone = g.user['timezone']
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """The home/index page.
    """
    timezone = get_timezone()
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        current_time = datetime.utcnow()
        tz = pytz.UTC

    formatted_time = format_datetime(
        current_time,
        format='full',
        locale=g.user['locale']
        if g.user and g.user.get('locale') else 'en'
    )

    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
