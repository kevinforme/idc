from flask import current_app, abort, request, render_template, flash, redirect, url_for
from flask_login import current_user

from flaskr import db
from flaskr.main.forms import NoticeForm, EventForm, EventDetailForm
from flaskr.models import Notice, Event, EventDetail
from . import main


@main.route('/shutdown')
def shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'shutting down...'


@main.route('/')
def index():
    page_notice = request.args.get('page', 1, type=int)
    pagination_notice = Notice.query.order_by(Notice.timestamp.desc()).paginate(page_notice, per_page=7,
                                                                                error_out=False)
    notices = pagination_notice.items
    events = Event.query.order_by(Event.timestamp.desc()).all()
    return render_template('index.html', notices=notices, events=events, pagination_notice=pagination_notice)


@main.route('/edit_notice', methods=['GET', 'POST'])
def edit_notice():
    form = NoticeForm()
    if form.validate_on_submit():
        notice = Notice(author=current_user._get_current_object(), body=form.body.data)
        db.session.add(notice)
        flash('发布成功')
        return redirect(url_for('main.index'))
    return render_template('edit_notice.html', form=form)


@main.route('/edit_event', methods=['GET', 'POST'])
def edit_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(author=current_user._get_current_object(), name=form.name.data)
        db.session.add(event)
        flash('发布成功')
        return redirect(url_for('main.index'))
    return render_template('edit_event.html', form=form)


@main.route('/event_detail/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    event_details = event.event_details.order_by(EventDetail.timestamp.asc()).all()
    return render_template('event_detail.html', event_details=event_details,event=event)


@main.route('/edit_detail/<int:id>', methods=['GET', 'POST'])
def edit_detail(id):
    form = EventDetailForm()
    event = Event.query.get_or_404(id)
    if form.validate_on_submit():
        eventdetail = EventDetail(body=form.body.data, event=event,user=current_user._get_current_object())
        db.session.add(eventdetail)
        return redirect(url_for('main.event_detail',id=event.id))
    return render_template('edit_detail.html', form=form)
