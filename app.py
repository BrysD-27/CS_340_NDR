from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_[your_onid]'
app.config['MYSQL_PASSWORD'] = '[your_db_password]'
app.config['MYSQL_DB'] = 'cs340_[your_onid]'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/supplies')
def supplies():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT supplyID, supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription
        FROM Supplies;
    """)
    supplies_data = cur.fetchall()
    return render_template("supplies.html", supplies=supplies_data)

@app.route('/drivers')
def drivers():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT driverID, firstName, lastName, phone, email, emergencyContactName,
               emergencyContactPhone, activeStatus, driverDetails
        FROM Drivers;
    """)
    drivers_data = cur.fetchall()
    return render_template("drivers.html", drivers=drivers_data)

@app.route('/recipients')
def recipients():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT recipientID, organizationName, streetAddress, city, state, zip,
               contactName, email, phone, description
        FROM Recipients;
    """)
    recipients_data = cur.fetchall()
    return render_template("recipients.html", recipients=recipients_data)

@app.route('/deliveries')
def deliveries():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT deliveryID, recipientID, driverID, campaignName, deliveredDateTime, notes
        FROM Deliveries;
    """)
    deliveries_data = cur.fetchall()
    return render_template("deliveries.html", deliveries=deliveries_data)

@app.route('/deliveries-supplies')
def deliveries_supplies():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT deliverySupplyID, deliveryID, supplyID, supplyQuantity
        FROM DeliveriesSupplies;
    """)
    ds_data = cur.fetchall()
    return render_template("deliveries_supplies.html", deliveries_supplies=ds_data)

if __name__ == '__main__':
    app.run(port=9313, debug=True)