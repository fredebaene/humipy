# HumiPy

A Python application to keep track of humidity.

## Application

This application allows for keeping track of humidity at various locations. A 
database is required. The `db_management.sql` file lists the tables required 
by the application.

The application enables the user to manage locations, sensors, and the 
placement of sensors at various locations. After proper installation of the 
sensors, measurements are sent to the database. The user can consult these 
measurements via the command line.

## Installation

To install the application, create a virtual environment with Python 3.10 or 
higher, and then install the application from GitHub:

```
pip install git+https://github.com/fredebaene/humipy.git
```