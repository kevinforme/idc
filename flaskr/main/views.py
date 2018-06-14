import datetime

from flask import current_app, abort, request, render_template, flash, redirect, url_for
from flask_login import current_user

from flaskr import db
from flaskr.main.forms import NoticeForm, EventForm, EventDetailForm, ResourceForm
from flaskr.models import Notice, Event, EventDetail, Resource, EventClass, ResourceClass
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
    page_event = request.args.get('page', 1, type=int)
    pagination_event = Event.query.filter_by(end=False).order_by(Event.start_time.desc()).paginate(page_event,
                                                                                                   per_page=10,
                                                                                                   error_out=False)
    events = pagination_event.items
    notices = Notice.query.order_by(Notice.timestamp.desc()).all()
    return render_template('index.html', events=events, pagination_event=pagination_event, notices=notices)


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
        event = Event(author=current_user._get_current_object(), name=form.name.data,
                      eventclass=EventClass.query.filter_by(classname=form.label.data).first())
        db.session.add(event)
        flash('发布成功')
        return redirect(url_for('main.index'))
    return render_template('edit_event.html', form=form)


@main.route('/event_detail/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    event_details = event.event_details.order_by(EventDetail.timestamp.asc()).all()
    ended = event.end
    return render_template('event_detail.html', event_details=event_details, event=event, ended=ended)


@main.route('/edit_detail/<int:id>', methods=['GET', 'POST'])
def edit_detail(id):
    form = EventDetailForm()
    event = Event.query.get_or_404(id)
    if form.validate_on_submit():
        eventdetail = EventDetail(body=form.body.data, event=event, user=current_user._get_current_object())
        db.session.add(eventdetail)
        return redirect(url_for('main.event_detail', id=event.id))
    return render_template('edit_detail.html', form=form)


@main.route('/end_event/')
def end_event():
    page = request.args.get('page', 1, type=int)
    label = request.args.get('eventclass', 1, type=int)
    klass = {1: '机房建设', 2: '客户施工', 3: '机房维护'}
    eventclass = EventClass.query.filter_by(classname=klass[label]).first()
    pagination = Event.query.filter_by(end=True, eventclass=eventclass).order_by(Event.start_time.desc()).paginate(page,
                                                                                                                   per_page=10,
                                                                                                                   error_out=False)
    events = pagination.items
    return render_template('end_event.html', events=events, pagination=pagination, label=label, Event=Event,
                           eventclass=eventclass)


@main.route('/go_end/<int:id>')
def go_end(id):
    event = Event.query.get_or_404(id)
    event.end = True
    event.end_time = datetime.datetime.utcnow()
    db.session.add(event)
    return redirect(url_for('main.index'))


@main.route('/resource')
def resource():
    resource_class = request.args.get('resource_class', 'profession', type=str)
    klass = ResourceClass.query.filter_by(name=resource_class).first()
    page = request.args.get('page', 1, type=int)
    pagination = Resource.query.filter_by(klass=klass).order_by(Resource.timestamp.desc()).paginate(
        page, per_page=12,
        error_out=False)
    resources = pagination.items
    return render_template('resource.html', resources=resources, pagination=pagination, resource_class=resource_class)


@main.route('/edit_resource', methods=['GET', 'POST'])
def edit_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        klass = ResourceClass.query.filter_by(name=form.resourceClass.data).first()
        resource = Resource(body=form.body.data, link=form.link.data, author=current_user._get_current_object(),
                            klass=klass)
        db.session.add(resource)
        return redirect(url_for('main.resource'))
    return render_template('edit_resource.html', form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    keywords = request.form.get('keywords')
    page_notice = request.args.get('page', 1, type=int)
    pagination_notice = Notice.query.filter(Notice.body.like('%' + keywords + '%')).order_by(
        Notice.timestamp.desc()).paginate(page_notice, per_page=7,
                                          error_out=False)
    notices = pagination_notice.items
    events = Event.query.filter_by(end=False).order_by(Event.start_time.desc()).all()
    return render_template('index.html', notices=notices, events=events, pagination_notice=pagination_notice)


@main.route('/delete_notice/<int:id>')
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    return redirect(url_for('main.index'))
