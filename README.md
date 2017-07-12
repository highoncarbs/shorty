# Shorty

> A URL shortening service built using Flask & Mysql. 

![Demo image of Shorty](./desc/hero_final.gif)
## Getting Started

Clone or download this repository.

```
git clone https://github.com/PadamSethia/shorty.git

cd shorty/

python ./app.py
```

## Prerequisites

This project requires Flask and MySQL . 
And MySQLdb python module for connection.
You can install it using the following commands . 

```
pip install flask

```
For mysql as backend

```
sudo apt install mysql-server

sudo apt-get install libmysqlclient-dev

pip install MySQL-python
```
Now run the following command to create the MySQL table 

```
python ./create_table.py
```
Configure the MySQL database credentials in ```config.py```
Set the host , user , password and database name for MySQL connection.

Also under MySQL shell set 
```
set autocommit = 0
```
This takes care of the concurrency issue.

## Projects Used
* [Skeleton CSS Framework](http://getskeleton.com)
* [Clipboard.js](https://clipboardjs.com)
## License
This project is licensed under the MIT Licene.
