### Hi there

Let's update and upgrade the system: `sudo apt update && apt upgrade -y` .
Install Apache: `sudo apt install apache2` .
Check Status of Apache: `systemctl status apache2` .
Verify it using browser: `http://ip-address` .
![image](https://github.com/rahulsharma-rks/awsProjects/assets/27508314/1f8449c9-bd46-48cd-950d-c888e00615ff)
Restart server incase server is not running: `sudo systemctl restart apache2` .
Adjust firewall settings to allow HTTP traffic: `sudo ufw app list` .

# Let's install MySQL:
`sudo apt install mysql-server`
`sudo mysql_secure_installation`
You can access MySQL by: `mysql` .
We need to create database, user and grant him permission:
```
CREATE DATABASE wordpress;
CREATE USER `wordpressuser`@`localhost` IDENTIFIED BY `your_password`;
GRANT ALL PRIVILEGES ON wordpress.* TO `wordpressuser`@`localhost`;
FLUSH PRIVILEGES;
exit;
```

Check if PHP is installed or not: `php -v` .
Let's add software-properties-common : `sudo apt -y install software-properties-common` .
Next we need to install the repository ppa:ondrej/php, which will give us all your versions of PHP: `sudo add-apt-repository ppa:ondrej/php` .
We will update the system, so that package manager can see new packages: `sudo apt-get update` .

# We will be using PHP7.4 .
Install: `sudo apt -y install php7.4`
Check for PHP version which is installed: `php -v` . You should be getting PHP7.4 version as output. 
Next we will install required packages: 
```
sudo apt-get install -y php7.4-cli php7.4-json php7.4-common php7.4-mysql php7.4-zip php7.4-gd php7.4-mbstring php7.4-curl php7.4-xml php7.4-bcmath
```
To check all the information related to PHP:
Navigate to dir: `cd /var/www/html/` .
Create a new file `info.php` and the following code:
```
<?php
phpinfo();
?>
```
Save it and go to your browser and add info.php : `http://ip-address/info.php` .
You will see all the information including php version, packages and extensions.

# WordPress:
Download the latest version: `wget https://wordpress.org/latest.tar.gz` .
Extract it using: `tar -xvf latest.tar.gz` .
```
cp -R wordpress /var/www/html/
chown -R www-data:www-data /var/www/html/wordpress/
chmod -R 755 /var/www/html/wordpress/
mkdir /var/www/html/wordpress/wp-content/uploads
chown -R www-data:www-data /var/www/html/wordpress/wp-content/uploads/
```

To install WordPress: 
Go to your browser and add wordpress at the end of ip-address: `http://ip-address/wordpress` .
You will be presented with wordpress installation page, add database detaila and continue to setup.
![image](https://github.com/rahulsharma-rks/awsProjects/assets/27508314/58bc64aa-2773-44de-8798-ae10f0d9bc31)

**Happy Blogging!**

