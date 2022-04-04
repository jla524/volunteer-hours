"""
A Flask application for logging volunteer hours
"""
from flask import Flask, request, render_template, make_response

from volunteer_hours.api.ragic import Ragic
from volunteer_hours.common.member import Member

app = Flask(__name__)
member = Member()


@app.route('/')
def main_screen() -> str:
    """
    The main page for scanning QR code
    :return: content from index.html
    """
    member.reset_member()
    content = render_template('index.html')
    return content


@app.route('/action', methods=['GET', 'POST'])
def action_screen() -> str:
    """
    The action page for selecting an event to sign in/out for
    :return: content from action.html with events from Ragic
    """
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        member.member_id = member_id
        response = make_response("{{'response': {member_id}}")
        response.headers = {'Content-Type': 'application/json'}
        return response

    name = member.get_member_name()
    events = member.get_event_names()
    content = render_template('action.html', name=name, events=events)
    return content


@app.route('/sent')
def sent_screen() -> str:
    """
    The sent screen to show that the hours have been logged
    :return: content from sent.html with a response from Ragic
    """
    event_name = request.args.get('event')
    event_id = member.get_event_id(event_name)
    message = Ragic().log_hours(member.member_id, event_id)
    content = render_template('sent.html', message=message)
    return content
