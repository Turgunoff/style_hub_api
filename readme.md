# StyleHub

## Description

StyleHub is a web application that allows users to upload and share their style.

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/Turgunoff/style_hub_api.git
   cd style_hub_api
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your database credentials and other configuration.

5. Set up the database

   ```bash
   alembic upgrade head
   ```

6. Run the application
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

DATABASE_URL=postgresql://username:password@localhost:5432/styleh
