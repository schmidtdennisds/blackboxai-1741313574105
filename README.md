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
     - `DATABASE_URL`: sqlite:///instance/fresco.db
     - `UPLOAD_FOLDER`: instance/uploads

Important Notes:
- The database and uploads will be stored in the `instance` directory within your application
- The first time you access the application, it will automatically create the database and admin user
- Make sure to change the admin password after first login

## Default Admin Account

- Email: admin@fresco.com
- Password: admin123 (change this immediately after first login)

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

## Environment Variables

- `SECRET_KEY`: Secret key for session management
- `FLASK_ENV`: Set to 'production' for production environment
- `DATABASE_URL`: Database connection URL (defaults to sqlite:///instance/fresco.db in production)
- `UPLOAD_FOLDER`: Path for uploaded files (defaults to instance/uploads in production)
- `SESSION_LIFETIME`: Session lifetime in minutes (default: 60)

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
└── instance/         # Application instance folder (created automatically)
    ├── fresco.db     # SQLite database
    └── uploads/      # Media storage
```

## After Deployment

1. Access your application at the Render URL
2. Log in with the default admin credentials
3. Immediately change the admin password
4. Start uploading lectures and managing content
5. Monitor the application logs in Render dashboard for any issues

## Troubleshooting

If you encounter database errors:
1. Check the Render logs to ensure the database is being created
2. Verify the DATABASE_URL environment variable is set correctly
3. Check if the application can write to the instance directory
4. Ensure the uploads directory exists in the instance folder

For any other issues, check the application logs in the Render dashboard.
