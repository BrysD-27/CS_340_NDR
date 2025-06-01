from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_davibrys'
app.config['MYSQL_PASSWORD'] = '5517'
app.config['MYSQL_DB'] = 'cs340_davibrys'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['SECRET_KEY'] = 'nothing'


mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # Supplies managed (sum of current inventory)
    cur.execute("SELECT COALESCE(SUM(currentInventory), 0) AS total_supplies FROM Supplies")
    total_supplies = cur.fetchone()['total_supplies']

    # Active drivers
    cur.execute("SELECT COUNT(*) AS active_drivers FROM Drivers WHERE activeStatus = TRUE")
    active_drivers = cur.fetchone()['active_drivers']

    # Completed deliveries
    cur.execute("SELECT COUNT(*) AS completed_deliveries FROM Deliveries WHERE deliveredDateTime IS NOT NULL")
    completed_deliveries = cur.fetchone()['completed_deliveries']

    return render_template(
        'index.html',
        supplies_count=total_supplies,
        drivers_count=active_drivers,
        deliveries_count=completed_deliveries
    )

# SUPPLY CRUD METHODS
@app.route('/supplies')
def supplies():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT supplyID, supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription
        FROM Supplies;
    """)
    supplies_data = cur.fetchall()
    return render_template("supplies.html", supplies=supplies_data)

# Create Supply
@app.route('/add-supply', methods=['POST'])
def add_supply():
    try:
        brand = request.form['supplyBrand']
        model = request.form['supplyModel']
        category = request.form['supplyCategory']
        inventory = request.form['currentInventory']
        description = request.form.get('unitDescription', None)
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Supplies (supplyBrand, supplyModel, supplyCategory, currentInventory, unitDescription)
            VALUES (%s, %s, %s, %s, %s)
        """, (brand, model, category, inventory, description))
        mysql.connection.commit()
        flash('Supply added!', 'success')
    except Exception as e:
        print("Error adding supply:", e)
        flash('Error adding supply.', 'danger')
    return redirect(url_for('supplies'))

# Route to Edit Supply
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

# Update Supply
@app.route('/update-supply/<int:id>', methods=['POST'])
def update_supply(id):
    try:
        brand = request.form['supplyBrand']
        model = request.form['supplyModel']
        category = request.form['supplyCategory']
        inventory = request.form['currentInventory']
        description = request.form.get('unitDescription', None)
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Supplies
            SET supplyBrand=%s, supplyModel=%s, supplyCategory=%s, currentInventory=%s, unitDescription=%s
            WHERE supplyID=%s
        """, (brand, model, category, inventory, description, id))
        mysql.connection.commit()
        flash('Supply updated!', 'success')
    except Exception as e:
        print("Error updating supply:", e)
        flash('Error updating supply.', 'danger')
    return redirect(url_for('supplies'))


# Delete Supply
@app.route('/delete-supply/<int:id>', methods=['POST'])
def delete_supply(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Supplies WHERE supplyID = %s", (id,))
        mysql.connection.commit()
        flash('Supply deleted!', 'success')
    except Exception as e:
        print("Error deleting supply:", e)
        flash('Error deleting supply.', 'danger')
    return redirect(url_for('supplies'))

# DRIVERS CRUD METHODS
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

# Create Driver
@app.route('/add-driver', methods=['POST'])
def add_driver():
    try:
        first = request.form['firstName']
        last = request.form['lastName']
        phone = request.form['phone']
        email = request.form['email']
        emergency_name = request.form.get('emergencyContactName')
        emergency_phone = request.form.get('emergencyContactPhone')
        active = bool(request.form.get('activeStatus', False))
        details = request.form.get('driverDetails', '')
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Drivers
                (firstName, lastName, phone, email, emergencyContactName, emergencyContactPhone, activeStatus, driverDetails)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first, last, phone, email, emergency_name, emergency_phone, active, details))
        mysql.connection.commit()
        flash('Driver added!', 'success')
    except Exception as e:
        print("Error adding driver:", e)
        flash('Error adding driver.', 'danger')
    return redirect(url_for('drivers'))

# Route to Edit Driver
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

# Update Driver
@app.route('/update-driver/<int:id>', methods=['POST'])
def update_driver(id):
    try:
        first = request.form['firstName']
        last = request.form['lastName']
        phone = request.form['phone']
        email = request.form['email']
        emergency_name = request.form.get('emergencyContactName')
        emergency_phone = request.form.get('emergencyContactPhone')
        active = bool(request.form.get('activeStatus', False))
        details = request.form.get('driverDetails', '')
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Drivers
            SET firstName=%s, lastName=%s, phone=%s, email=%s,
                emergencyContactName=%s, emergencyContactPhone=%s,
                activeStatus=%s, driverDetails=%s
            WHERE driverID=%s
        """, (first, last, phone, email, emergency_name, emergency_phone, active, details, id))
        mysql.connection.commit()
        flash('Driver updated!', 'success')
    except Exception as e:
        print("Error updating driver:", e)
        flash('Error updating driver.', 'danger')
    return redirect(url_for('drivers'))

# Delete Driver
@app.route('/delete-driver/<int:id>', methods=['POST'])
def delete_driver(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Drivers WHERE driverID = %s", (id,))
        mysql.connection.commit()
        flash('Driver deleted!', 'success')
    except Exception as e:
        print("Error deleting driver:", e)
        flash('Error deleting driver.', 'danger')
    return redirect(url_for('drivers'))

# RECIPIENTS CRUD METHODS
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

# Add Recipient
@app.route('/add-recipient', methods=['POST'])
def add_recipient():
    try:
        organization = request.form['organizationName']
        address = request.form['streetAddress']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        contact = request.form['contactName']
        email = request.form.get('email')
        phone = request.form.get('phone')
        description = request.form.get('description')
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Recipients
                (organizationName, streetAddress, city, state, zip, contactName, email, phone, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (organization, address, city, state, zip_code, contact, email, phone, description))
        mysql.connection.commit()
        flash('Recipient added!', 'success')
    except Exception as e:
        print("Error adding recipient:", e)
        flash('Error adding recipient.', 'danger')
    return redirect(url_for('recipients'))

# Route to Edit Recipient
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

# Update Recipient
@app.route('/update-recipient/<int:id>', methods=['POST'])
def update_recipient(id):
    try:
        organization = request.form['organizationName']
        address = request.form['streetAddress']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        contact = request.form['contactName']
        email = request.form.get('email')
        phone = request.form.get('phone')
        description = request.form.get('description')
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Recipients
            SET organizationName=%s, streetAddress=%s, city=%s, state=%s, zip=%s,
                contactName=%s, email=%s, phone=%s, description=%s
            WHERE recipientID=%s
        """, (organization, address, city, state, zip_code, contact, email, phone, description, id))
        mysql.connection.commit()
        flash('Recipient updated!', 'success')
    except Exception as e:
        print("Error updating recipient:", e)
        flash('Error updating recipient.', 'danger')
    return redirect(url_for('recipients'))

# Delete Recipient
@app.route('/delete-recipient/<int:id>', methods=['POST'])
def delete_recipient(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Recipients WHERE recipientID = %s", (id,))
        mysql.connection.commit()
        flash('Recipient deleted!', 'success')
    except Exception as e:
        print("Error deleting recipient:", e)
        flash('Error deleting recipient.', 'danger')
    return redirect(url_for('recipients'))

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

# Create Delivery
@app.route('/add-delivery', methods=['POST'])
def add_delivery():
    try:
        recipientID = request.form['recipientID']
        driverID = request.form['driverID']
        campaign = request.form.get('campaignName')
        date_time = request.form.get('deliveredDateTime')
        notes = request.form.get('notes')
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Deliveries (recipientID, driverID, campaignName, deliveredDateTime, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (recipientID, driverID, campaign, date_time, notes))
        mysql.connection.commit()
        flash('Delivery added!', 'success')
    except Exception as e:
        print("Error adding delivery:", e)
        flash('Error adding delivery.', 'danger')
    return redirect(url_for('deliveries'))

# Route to Edit Delivery
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

# Update Delivery 
@app.route('/update-delivery/<int:id>', methods=['POST'])
def update_delivery(id):
    try:
        recipientID = request.form['recipientID']
        driverID = request.form['driverID']
        campaign = request.form.get('campaignName')
        date_time = request.form.get('deliveredDateTime')
        notes = request.form.get('notes')
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Deliveries
            SET recipientID=%s, driverID=%s, campaignName=%s, deliveredDateTime=%s, notes=%s
            WHERE deliveryID=%s
        """, (recipientID, driverID, campaign, date_time, notes, id))
        mysql.connection.commit()
        flash('Delivery updated!', 'success')
    except Exception as e:
        print("Error updating delivery:", e)
        flash('Error updating delivery.', 'danger')
    return redirect(url_for('deliveries'))

# Delete Delivery
@app.route('/delete-delivery/<int:id>', methods=['POST'])
def delete_delivery(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Deliveries WHERE deliveryID = %s", (id,))
        mysql.connection.commit()
        flash('Delivery deleted!', 'success')
    except Exception as e:
        print("Error deleting delivery:", e)
        flash('Error deleting delivery.', 'danger')
    return redirect(url_for('deliveries'))

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
    cur.execute("SELECT deliveryID, campaignName FROM Deliveries;")
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
    cur.execute("SELECT deliveryID, campaignName FROM Deliveries")
    deliveries = cur.fetchall()

    # For supplies dropdowns
    cur.execute("SELECT supplyID, supplyBrand, supplyModel FROM Supplies")
    supplies = cur.fetchall()

    return render_template("edit_delivery_supply.html", ds=ds, deliveries=deliveries, supplies=supplies)

# Create Delivery Supply
@app.route('/add-delivery-supply', methods=['POST'])
def add_delivery_supply():
    try:
        deliveryID = request.form['deliveryID']
        supplyID = request.form['supplyID']
        supplyQuantity = request.form['supplyQuantity']
        cur = mysql.connection.cursor()
        cur.callproc('sp_add_delivery_supply', (deliveryID, supplyID, supplyQuantity))
        mysql.connection.commit()
        flash('Delivery supply added!', 'success')
    except Exception as e:
        print("Error adding delivery supply:", e)
        flash('Error adding delivery supply.', 'danger')
    return redirect(url_for('deliveries_supplies'))

# Update Delivery Supply
@app.route('/update-delivery-supply/<int:id>', methods=['POST'])
def update_delivery_supply(id):
    try:
        deliveryID = request.form['deliveryID']
        supplyID = request.form['supplyID']
        supplyQuantity = request.form['supplyQuantity']
        cur = mysql.connection.cursor()
        cur.callproc('sp_update_delivery_supply', (id, deliveryID, supplyID, supplyQuantity))
        mysql.connection.commit()
        flash('Delivery supply updated!', 'success')
    except Exception as e:
        print("Error updating delivery supply:", e)
        flash('Error updating delivery supply.', 'danger')
    return redirect(url_for('deliveries_supplies'))

# Delete Delivery Supply
@app.route('/delete-delivery-supply/<int:id>', methods=['POST'])
def delete_delivery_supply(id):
    try:
        cur = mysql.connection.cursor()
        cur.callproc('sp_delete_delivery_supply', (id,))
        mysql.connection.commit()
        flash('Delivery supply deleted!', 'success')
    except Exception as e:
        print("Error deleting delivery supply:", e)
        flash('Error deleting delivery supply.', 'danger')
    return redirect(url_for('deliveries_supplies'))

@app.route('/reset-database')
def reset_database():
    try:
        cur = mysql.connection.cursor()
        cur.execute("CALL sp_reset_database();")
        mysql.connection.commit()
        return index()
    except Exception as e:
        print("Error during RESET:", e)
        return "Database reset failed", 500

@app.route('/delete-latest-driver')
def delete_latest_driver():
    try:
        cur = mysql.connection.cursor()
        cur.execute("CALL sp_delete_latest_driver();")
        mysql.connection.commit()
        return drivers()
    except Exception as e:
        print("Error during DELETE:", e)
        return "Delete failed", 500


if __name__ == '__main__':
    app.run(port=4200, debug=True)