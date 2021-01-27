from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from snowflake.controllers.api.response import not_found
from snowflake.models.notification import *
from ..db import db

blueprint = Blueprint('notifications', __name__)


def build_redirect(notification: Notification):
    if notification.type == TYPE_APPRECIATION:
        return url_for('index.index') + f"#appreciation-{notification.object_id}"
    elif notification.type == TYPE_COMMENT_ON_APPRECIATION_RECEIVED \
            or notification.type == TYPE_COMMENT_ON_APPRECIATION_GIVEN:
        return url_for('index.index') + f"#appreciation-{notification.object.appreciation.id}"
    elif notification.type == TYPE_ONE_ON_ONE_SETUP or TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED:
        return url_for('one_on_one.one_on_one', _id=notification.object.id)


@login_required
@blueprint.route('/<_id>/open', methods=['GET'])
def open_notification(_id):
    notification = Notification.get(_id)
    if not notification:
        return not_found()

    notification.read = True
    db.session.add(notification)
    db.session.commit()

    return redirect(build_redirect(notification))


@login_required
@blueprint.route('')
def notifications():
    return render_template('notifications.html', notifications=Notification.get_by_user(current_user))