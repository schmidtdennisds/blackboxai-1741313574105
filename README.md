# Fresco Learning Platform

A modern learning platform featuring lecture management, synchronized transcripts, and user authentication.

## Features

- User authentication and role-based access control
- Lecture management with audio/video playback
- Synchronized transcript viewing
- Waveform visualization
- Note-taking capabilities
- Discussion system
- Admin panel for content management

## Deployment on Render

1. Fork or clone this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add the following environment variables:
     - `SECRET_KEY`: (Render will auto-generate this)
     - `FLASK_ENV`: production
     - `DATABASE_URL`: sqlite:///fresco.db

The application will be automatically deployed and available at your Render URL.

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Default Admin Account

- Email: admin@fresco.com
- Password: admin123 (change this in production)

## Environment Variables

- `SECRET_KEY`: Secret key for session management
- `FLASK_ENV`: Set to 'production' for production environment
- `DATABASE_URL`: Database connection URL
- `UPLOAD_FOLDER`: Path for uploaded files
- `SESSION_LIFETIME`: Session lifetime in minutes (default: 60)

## Security Features

- CSRF protection
- Secure password hashing
- HTTPS enforcement in production
- Session management
- Role-based access control

## File Structure

```
fresco-learning/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Procfile           # Render deployment configuration
├── render.yaml        # Render service configuration
├── templates/         # HTML templates
│   ├── admin/        # Admin panel templates
│   └── ...           # Other templates
└── uploads/          # Media storage
