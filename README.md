# Dhruv Mishra Portfolio

A Flask-based personal portfolio website for showcasing projects, skills, internships, certificates, achievements, coding profiles, and contact details.

## Tech Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- Gunicorn for production deployment

## Project Structure

```txt
portFolio/
|-- app.py
|-- requirements.txt
|-- Procfile
|-- render.yaml
|-- components/
|   |-- index.html
|   |-- projects.html
|   |-- project_detail.html
|   |-- experience_detail.html
|   |-- skill_detail.html
|   `-- partials/
|-- data/
|   `-- portfolio_content.json
|-- src/
|   |-- styles.css
|   |-- pp.png
|   `-- uploads/
`-- portfolio_store.py
```

## Run Locally

1. Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd portFolio
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the app:

```bash
python app.py
```

6. Open the site:

```txt
http://127.0.0.1:5000
```

## Deploy To Render

This project is already configured for Render using `render.yaml` and `Procfile`.

### Step 1: Push Code To GitHub

If this project is not already in a GitHub repository, run:

```bash
git init
git add .
git commit -m "Initial portfolio deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

### Step 2: Create Render Web Service

1. Go to Render.
2. Click **New**.
3. Select **Web Service**.
4. Connect your GitHub account.
5. Select this portfolio repository.

### Step 3: Confirm Render Settings

Render should read `render.yaml` automatically. If you need to enter settings manually, use:

```txt
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Step 4: Environment Variable

Add this environment variable if Render does not generate it automatically:

```txt
PORTFOLIO_SECRET_KEY=your-long-random-secret-key
```

### Step 5: Deploy

Click **Deploy Web Service**.

After the build finishes, Render will provide a live URL like:

```txt
https://your-portfolio.onrender.com
```

## Important Deployment Note

This app stores portfolio content in:

```txt
data/portfolio_content.json
```

Uploaded files are stored inside:

```txt
src/uploads/
```

On free hosting, changes made through the admin panel may not persist permanently after redeploys or service restarts unless you use persistent storage or move the content to a database.

## Production Start Command

```bash
gunicorn app:app
```
