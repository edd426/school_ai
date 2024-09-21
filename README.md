# School Database Setup Guide for MacBook

This guide outlines the steps to set up a MySQL server, configure the environment, and initialize a school database on a MacBook.

## 1. MySQL Server Setup

### Install MySQL

1. Install Homebrew if not already installed:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install MySQL:
   ```
   brew install mysql
   ```

### Configure MySQL

1. Start MySQL service:
   ```
   brew services start mysql
   ```

2. Secure MySQL installation:
   ```
   mysql_secure_installation
   ```
   - When prompted to set a root password, use: Swordfish
   - Answer 'Y' to all other prompts for secure configuration

3. Verify MySQL service status:
   ```
   brew services list
   ```
   MySQL should show as 'started'.

## 2. Environment Setup

### Install pipx

1. Install pipx if not already installed:
   ```
   brew install pipx
   pipx ensurepath
   ```

### Install Poetry

1. Use pipx to install Poetry:
   ```
   pipx install poetry
   pipx ensurepath
   source ~/.zshrc
   ```

### Clone and Set Up the Project

1. Clone the project repository (replace with your actual repo URL):
   ```
   git clone https://github.com/edd426/school_ai.git
   cd school-database-project
   ```

2. Install project dependencies:
   ```
   poetry install
   ```

### Create .env File

1. Create a .env file in the project root:
   ```
   echo "MYSQL_PASSWORD='Swordfish'" > .env
   ```
2. Also pass your ANTHROPIC_API_KEY to the .env file. Be sure to fill in with your actual key:
   ```
   echo "ANTHROPIC_API_KEY='<Your Antrhopic API Key Here>'"

## 3. Initialize the Database for the First Time

1. Activate the Poetry environment:
   ```
   poetry shell
   ```

2. Run the database initializer script:
   ```
   python database_initializer.py
   ```

## FastAPI Server

1. Run the FastApi server:
```
poetry run uvicorn main:app --reload
```
2. Access the API documentation at `http://127.0.0.1:8000/docs`.

3. Run the tests using pytest:
```
poetry run pytest
```

## Additional MySQL Commands

- Start MySQL server: `brew services start mysql`
- Stop MySQL server: `brew services stop mysql`
- Restart MySQL server: `brew services restart mysql`
- Log into MySQL shell: `mysql -u root -p` (enter password when prompted)
- Check MySQL status: `ps aux | grep mysql`

## Troubleshooting

If you encounter issues with MySQL:

1. Check MySQL error logs:
   ```
   tail -f /usr/local/var/mysql/*.err
   ```

2. Ensure proper permissions:
   ```
   sudo chown -R _mysql:_mysql /usr/local/var/mysql
   ```

3. If problems persist, consider reinstalling MySQL:
   ```
   brew uninstall mysql
   brew install mysql
   ```

Remember to regularly backup your databases and keep your MySQL installation secure.
