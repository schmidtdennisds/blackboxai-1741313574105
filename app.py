from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, flash, session, abort, send_file
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
import os
import urllib.parse
from datetime import datetime, timedelta

# Set up paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
if os.environ.get('FLASK_ENV') == 'production':
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'instance', 'uploads')
    DB_PATH = 'sqlite:///instance/fresco.db'
else:
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
    DB_PATH = 'sqlite:///fresco.db'

# Create necessary directories
os.makedirs(os.path.join(DATA_DIR, 'instance'), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-please-change')
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DB_PATH)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(os.environ.get('SESSION_LIFETIME', 60)))

# Enable HTTPS redirect in production
if os.environ.get('FLASK_ENV') == 'production':
    from flask_talisman import Talisman
    Talisman(app, force_https=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))
    duration = db.Column(db.Integer)  # in minutes
    media_path = db.Column(db.String(200))
    transcript_path = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
# Admin routes
@app.route('/admin/upload')
@login_required
def admin_upload():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin/upload.html')

@app.route('/lecture/<int:lecture_id>')
@login_required
def view_lecture(lecture_id):
    lecture = Lecture.query.get_or_404(lecture_id)
    if not lecture.published and not current_user.is_admin:
        abort(404)
    return render_template('lecture-view.html', lecture=lecture)

@app.route('/admin/lectures')
@login_required
def admin_lectures():
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        # Admin sees all lectures
        pagination = Lecture.query.order_by(Lecture.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False)
    else:
        # Regular users see only published lectures
        pagination = Lecture.query.filter_by(published=True).order_by(
            Lecture.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    lectures = pagination.items
    template = 'admin/lectures.html' if current_user.is_admin else 'lectures.html'
    return render_template(template, lectures=lectures, pagination=pagination)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    users = pagination.items
    return render_template('admin/users.html', users=users, pagination=pagination)

@app.route('/')
def index():
    # Get featured lectures (only published ones)
    query = Lecture.query.filter_by(published=True)
    if not current_user.is_authenticated or not current_user.is_admin:
        query = query.filter_by(featured=True)
    
    featured_lectures = query.order_by(Lecture.created_at.desc()).limit(3).all()
    return render_template('index.html', featured_lectures=featured_lectures)

# Template filters
@app.template_filter('datetime')
def format_datetime(value):
    if value is None:
        return ""
    return value.strftime('%b %d, %Y')

@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, str):
        s = s.encode('utf8')
    return urllib.parse.quote_plus(s)

# Auth routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate input
        if not email or not password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('signup.html')

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'error')
            return render_template('signup.html')

        try:
            # Create new user
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_lectures'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember-me' in request.form
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.permanent = True
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin_lectures')
            return redirect(next_page)
        
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/upload', methods=['POST'])
@login_required
def upload_lecture():
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    try:
        # Handle file uploads
        media_file = request.files.get('media')
        transcript_file = request.files.get('transcript')
        
        if not media_file or not transcript_file:
            return jsonify({'success': False, 'message': 'Missing files'}), 400

        # Save files
        media_filename = secure_filename(media_file.filename)
        transcript_filename = secure_filename(transcript_file.filename)
        
        media_path = os.path.join(app.config['UPLOAD_FOLDER'], media_filename)
        transcript_path = os.path.join(app.config['UPLOAD_FOLDER'], transcript_filename)
        
        media_file.save(media_path)
        transcript_file.save(transcript_path)

        # Create lecture record
        lecture = Lecture(
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            difficulty=request.form.get('difficulty'),
            duration=int(request.form.get('duration')),
            media_path=media_filename,
            transcript_path=transcript_filename,
            featured=bool(request.form.get('featured')),
            published=bool(request.form.get('published'))
        )

        db.session.add(lecture)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Lecture uploaded successfully',
            'lecture_id': lecture.id
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/components/<path:filename>')
def serve_component(filename):
    try:
        return send_from_directory('components', filename)
    except Exception:
        abort(404)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico') if os.path.exists('static/favicon.ico') else abort(404)

# Static page routes - Root level
@app.route('/about')
def about_page():
    try:
        return send_from_directory(app.root_path, 'about.html')
    except Exception:
        abort(404)

@app.route('/community')
def community_page():
    try:
        return send_from_directory(app.root_path, 'community.html')
    except Exception:
        abort(404)

@app.route('/dashboard')
def dashboard_page():
    try:
        return send_from_directory(app.root_path, 'dashboard.html')
    except Exception:
        abort(404)

@app.route('/gallery')
def gallery_page():
    try:
        return send_from_directory(app.root_path, 'gallery.html')
    except Exception:
        abort(404)

@app.route('/lecture-enhanced')
def lecture_enhanced_page():
    try:
        return send_from_directory(app.root_path, 'lecture-enhanced.html')
    except Exception:
        abort(404)

@app.route('/lecture')
def lecture_page():
    try:
        return send_from_directory(app.root_path, 'lecture.html')
    except Exception:
        abort(404)

@app.route('/notes')
def notes_page():
    try:
        return send_from_directory(app.root_path, 'notes.html')
    except Exception:
        abort(404)

@app.route('/signin')
def signin_page():
    try:
        return send_from_directory(app.root_path, 'signin.html')
    except Exception:
        abort(404)

@app.route('/subscription')
def subscription_page():
    try:
        return send_from_directory(app.root_path, 'subscription.html')
    except Exception:
        abort(404)

# About section routes
@app.route('/about/archive')
def about_archive():
    try:
        return send_from_directory(os.path.join(app.root_path, 'about'), 'archive.html')
    except Exception:
        abort(404)

@app.route('/about/bibliography')
def about_bibliography():
    try:
        return send_from_directory(os.path.join(app.root_path, 'about'), 'bibliography.html')
    except Exception:
        abort(404)

@app.route('/about/media')
def about_media():
    try:
        return send_from_directory(os.path.join(app.root_path, 'about'), 'media.html')
    except Exception:
        abort(404)

@app.route('/about/model')
def about_model():
    try:
        return send_from_directory(os.path.join(app.root_path, 'about'), 'model.html')
    except Exception:
        abort(404)

@app.route('/about/timeline')
def about_timeline():
    try:
        return send_from_directory(os.path.join(app.root_path, 'about'), 'timeline.html')
    except Exception:
        abort(404)

# Donate section routes
@app.route('/donate/general')
def donate_general():
    try:
        return send_from_directory(os.path.join(app.root_path, 'donate'), 'general.html')
    except Exception:
        abort(404)

@app.route('/donate/unlocking')
def donate_unlocking():
    try:
        return send_from_directory(os.path.join(app.root_path, 'donate'), 'unlocking.html')
    except Exception:
        abort(404)

# Store section routes
@app.route('/store/cart')
def store_cart():
    try:
        return send_from_directory(os.path.join(app.root_path, 'store'), 'cart.html')
    except Exception:
        abort(404)

@app.route('/store/checkout')
def store_checkout():
    try:
        return send_from_directory(os.path.join(app.root_path, 'store'), 'checkout.html')
    except Exception:
        abort(404)

@app.route('/store/products')
def store_products():
    try:
        return send_from_directory(os.path.join(app.root_path, 'store'), 'products.html')
    except Exception:
        abort(404)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

def init_db():
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@fresco.com').first()
        if not admin:
            admin = User(email='admin@fresco.com', is_admin=True)
            admin.set_password('admin123')  # Change this in production
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        print("Database initialized!")

# Initialize database on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
