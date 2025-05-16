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
        SELECT d.deliveryID,
            r.organizationName AS recipientName,
            CONCAT(dr.firstName, ' ', dr.lastName) AS driverName,
            d.campaignName, d.deliveredDateTime, d.notes
        FROM Deliveries d
        JOIN Recipients r ON d.recipientID = r.recipientID
        JOIN Drivers dr ON d.driverID = dr.driverID;
    """)
    deliveries_data = cur.fetchall()

    # Get recipients for dropdown
    cur.execute("SELECT recipientID, organizationName FROM Recipients;")
    recipients_list = cur.fetchall()

    # Get drivers for dropdown
    cur.execute("SELECT driverID, firstName, lastName FROM Drivers WHERE activeStatus = 1;")
    drivers_list = cur.fetchall()

    return render_template(
        "deliveries.html",
        deliveries=deliveries_data,
        recipients=recipients_list,
        drivers=drivers_list
    )
@app.route('/deliveries-supplies')
def deliveries_supplies():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ds.deliverySupplyID,
               ds.deliveryID,
               s.supplyBrand,
               s.supplyModel,
               ds.supplyQuantity
        FROM DeliveriesSupplies ds
        JOIN Supplies s ON ds.supplyID = s.supplyID;
    """)

    ds_data = cur.fetchall()

    # Get deliveries for dropdown
    cur.execute("SELECT deliveryID FROM Deliveries;")
    deliveries_list = cur.fetchall()

    # Get supplies for dropdown
    cur.execute("SELECT supplyID, supplyBrand, supplyModel FROM Supplies;")
    supplies_list = cur.fetchall()

    return render_template(
        "deliveries_supplies.html",
        deliveries_supplies=ds_data,
        deliveries=deliveries_list,
        supplies=supplies_list
    )

@app.route("/edit-supply/<int:id>")
def edit_supply(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT supplyID, supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription
        FROM Supplies
        WHERE supplyID = %s
    """, (id,))

    supply = cur.fetchone()
    return render_template("edit_supply.html", supply=supply)

@app.route("/edit-driver/<int:id>")
def edit_driver(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT driverID, firstName, lastName, phone, email, emergencyContactName,
               emergencyContactPhone, activeStatus, driverDetails
        FROM Drivers
        WHERE driverID = %s
    """, (id,))

    driver = cur.fetchone()
    return render_template("edit_driver.html", driver=driver)

@app.route("/edit-recipient/<int:id>")
def edit_recipient(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT recipientID, organizationName, streetAddress, city, state, zip,
               contactName, email, phone, description
        FROM Recipients
        WHERE recipientID = %s
    """, (id,))

    recipient = cur.fetchone()
    return render_template("edit_recipient.html", recipient=recipient)

@app.route("/edit-delivery/<int:id>")
def edit_delivery(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.deliveryID,
               d.recipientID,
               r.organizationName AS recipientName,
               d.driverID,
               CONCAT(dr.firstName, ' ', dr.lastName) AS driverName,
               d.campaignName,
               d.deliveredDateTime,
               d.notes
        FROM Deliveries d
        JOIN Recipients r ON d.recipientID = r.recipientID
        JOIN Drivers dr ON d.driverID = dr.driverID
        WHERE d.deliveryID = %s
    """, (id,))

    delivery = cur.fetchone()

    # Get recipients for dropdown
    cur.execute("SELECT recipientID, organizationName FROM Recipients")
    recipients = cur.fetchall()

    # Get drivers for dropdown
    cur.execute("SELECT driverID, firstName, lastName FROM Drivers")
    drivers = cur.fetchall()

    return render_template("edit_delivery.html", delivery=delivery, recipients=recipients, drivers=drivers)

@app.route("/edit-delivery-supply/<int:id>")
def edit_delivery_supply(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT ds.deliverySupplyID,
               ds.deliveryID,
               ds.supplyID,
               s.supplyBrand,
               s.supplyModel,
               ds.supplyQuantity
        FROM DeliveriesSupplies ds
        JOIN Supplies s ON ds.supplyID = s.supplyID
        WHERE ds.deliverySupplyID = %s
    """, (id,))
    ds = cur.fetchone()

    # For deliveries dropdowns
    cur.execute("SELECT deliveryID FROM Deliveries")
    deliveries = cur.fetchall()

    # For supplies dropdowns
    cur.execute("SELECT supplyID, supplyBrand, supplyModel FROM Supplies")
    supplies = cur.fetchall()

    return render_template("edit_delivery_supply.html", ds=ds, deliveries=deliveries, supplies=supplies)

if __name__ == '__main__':
    app.run(port=9315, debug=True)