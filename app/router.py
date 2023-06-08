from flask import render_template, request, session, redirect, url_for, flash
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, VaccinationCentre, Admin, Booking

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('login.html', form=form, error='Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

from flask import request

@app.route('/user/dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('search_query')

    if search_query:
        centres = VaccinationCentre.query.filter(VaccinationCentre.name.ilike(f'%{search_query}%')).all()
    else:
        centres = VaccinationCentre.query.all()

    form = RegistrationForm()

    if form.validate_on_submit():
        centre_id = form.centre_id.data
        centre = VaccinationCentre.query.get(centre_id)
        if centre and centre.slots > 0:
            # Register the user for the selected centre
            # Decrease the slots count by 1
            centre.slots -= 1
            db.session.commit()
            return redirect(url_for('user_dashboard'))
        else:
            flash('Registration failed. The selected vaccination centre is fully booked.')

    return render_template('user_dashboard.html', centres=centres, form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        ad = Admin.query.filter_by(username=username, password=password).first()

        if ad:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', form=form, error='Invalid username or password')

    return render_template('admin_login.html', form=form)


@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin'))

    centres = VaccinationCentre.query.all()

    if request.method == 'POST':
        dosage_details = {}
        for centre in centres:
            dosage_details[centre] = Booking.query.filter_by(centre_id=centre.id).count()

        return render_template('admin_dashboard.html', centres=centres, dosage_details=dosage_details)

    return render_template('admin_dashboard.html', centres=centres)


@app.route('/register', methods=['POST'])
def register():
    centre_id = request.form.get('centre_id')
    centre = VaccinationCentre.query.get(centre_id)
    if centre and centre.slots > 0:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        booking = Booking.query.filter_by(user_id=user_id, centre_id=centre_id).first()
        if booking:
            flash('You have already booked a slot for this vaccination centre.')
            return redirect(url_for('user_dashboard'))
        else:
            booking = Booking(user=user, centre=centre, centre_name=centre.name, working_hours=centre.working_hours)
            db.session.add(booking)
            centre.slots -= 1
            db.session.commit()
            return redirect(url_for('user_dashboard'))
    else:
        flash('Registration failed. The selected vaccination centre is fully booked.')
        return redirect(url_for('user_dashboard'))




@app.route('/admin/add_centre', methods=['GET', 'POST'])
def add_centre():
    if 'admin' not in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        name = request.form['name']
        working_hours = request.form['working_hours']
        slots = request.form['slots']
        centre = VaccinationCentre(name=name, working_hours=working_hours, slots=slots)
        db.session.add(centre)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_centre.html')

@app.route('/admin/remove_centre/<int:centre_id>', methods=['POST'])
def remove_centre(centre_id):
    if 'admin' not in session:
        return redirect(url_for('admin'))
    centre = VaccinationCentre.query.get(centre_id)
    db.session.delete(centre)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
