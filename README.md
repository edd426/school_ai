```markdown
# Starting MySQL Server on MacBook

This guide outlines the steps to start and manage your MySQL server on a MacBook.

## Initial Setup (If not already done)

1. Install Homebrew:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install MySQL:
   ```
   brew install mysql
   ```

3. Secure MySQL installation:
   ```
   mysql_secure_installation
   ```
   Follow the prompts to set a root password and configure security options.

## Starting the MySQL Server

1. Start MySQL service using Homebrew:
   ```
   brew services start mysql
   ```

2. Verify MySQL service status:
   ```
   brew services list
   ```
   Look for `mysql` in the list. It should show as `started`.

## Stopping the MySQL Server

If you need to stop the MySQL server:

```
brew services stop mysql
```

## Restarting the MySQL Server

To restart the MySQL server:

```
brew services restart mysql
```

## Logging into MySQL

To log in to the MySQL shell:

```
mysql -u root -p
```
Enter your password when prompted.

## Checking MySQL Server Status

To check if MySQL server is running:

```
ps aux | grep mysql
```
If MySQL is running, you'll see multiple lines of output.

## Troubleshooting

If you encounter issues starting MySQL:

1. Check MySQL error logs:
   ```
   tail -f /usr/local/var/mysql/*.err
   ```

2. Ensure proper permissions:
   ```
   sudo chown -R _mysql:_mysql /usr/local/var/mysql
   ```

3. Reinstall MySQL if persistent issues occur:
   ```
   brew uninstall mysql
   brew install mysql
   ```

Remember to secure your MySQL installation and regularly backup your databases.
```