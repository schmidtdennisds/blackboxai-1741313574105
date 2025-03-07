# Fresco Learning Platform

A modern learning platform featuring lecture management, synchronized transcripts, and user authentication.

## Tailwind CSS Setup

The project uses Tailwind CSS for styling, with two different configurations:

### Development
In development mode, Tailwind CSS is loaded via CDN for quick iterations and development ease:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### Production
For production, we use a compiled and optimized version of Tailwind CSS:
1. The source file is at `static/css/tailwind-base.css`
2. Configuration is in `tailwind.config.js`
3. Compiled output goes to `static/css/tailwind.css`

To rebuild the production CSS:
```bash
# Install dependencies
npm install

# Build and minify the CSS
npx tailwindcss -i ./static/css/tailwind-base.css -o ./static/css/tailwind.css --minify
```

### Custom Styles
Custom styles and Tailwind overrides are in `static/css/styles.css`. This file is loaded after Tailwind to allow proper cascading of styles.

## Project Structure

- `/templates` - Flask HTML templates
- `/static` - Static assets (CSS, JS, images)
- `/components` - Reusable HTML components
- `/admin` - Admin interface templates
- `/store` - E-commerce related templates
- `/about` - About section templates
- `/uploads` - User uploaded content

## Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
python app.py
```

## Production Deployment

The application is configured for deployment on Render with the following files:
- `Procfile` - Process configuration
- `render.yaml` - Render platform configuration
- `requirements.txt` - Python dependencies
