# This file cites and replicates similarly to:
# INTRODUCTION TO DATABASES (CS_340_400_S2025) Activity 2 Flask Starter Code

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

# Home Dashboard Route   
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("CALL sp_get_total_supplies()")
    total_supplies = cur.fetchone()['total_supplies']

    cur.execute("CALL sp_get_active_drivers()")
    active_drivers = cur.fetchone()['active_drivers']

    cur.execute("CALL sp_get_completed_deliveries()")
    completed_deliveries = cur.fetchone()['completed_deliveries']

    return render_template(
        'index.html',
        supplies_count=total_supplies,
        drivers_count=active_drivers,
        deliveries_count=completed_deliveries
    )

# SUPPLY CRUD METHODS
# Base Supply Route - SELECT all Supplies
@app.route('/supplies')
def supplies():
    cur = mysql.connection.cursor()
    cur.callproc('sp_get_supplies')
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
        cur.callproc('sp_add_supply', (brand, model, category, inventory, description))
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
    cur.callproc('sp_get_supply_by_id', (id,))
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
        cur.callproc('sp_update_supply', (id, brand, model, category, inventory, description))
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
        cur.callproc('sp_delete_supply', (id,))
        mysql.connection.commit()
        flash('Supply deleted!', 'success')
    except Exception as e:
        print("Error deleting supply:", e)
        flash('Error deleting supply.', 'danger')
    return redirect(url_for('supplies'))


# DRIVERS CRUD METHODS
# Base Driver Route - SELECT all Drivers
@app.route('/drivers')
def drivers():
    cur = mysql.connection.cursor()
    cur.callproc('sp_get_drivers')
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
        active = 1 if request.form.get('activeStatus') else 0
        details = request.form.get('driverDetails', '')
        cur = mysql.connection.cursor()
        cur.callproc('sp_add_driver', (first, last, phone, email, emergency_name, emergency_phone, active, details))
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
    cur.callproc('sp_get_driver_by_id', (id,))
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
        active = 1 if request.form.get('activeStatus') else 0
        details = request.form.get('driverDetails', '')
        cur = mysql.connection.cursor()
        cur.callproc('sp_update_driver', (id, first, last, phone, email, emergency_name, emergency_phone, active, details))
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
        cur.callproc('sp_delete_driver', (id,))
        mysql.connection.commit()
        flash('Driver deleted!', 'success')
    except Exception as e:
        print("Error deleting driver:", e)
        flash('Error deleting driver.', 'danger')
    return redirect(url_for('drivers'))

# RECIPIENTS CRUD METHODS
# Base Recipient Route - SELECT all Recipients
@app.route('/recipients')
def recipients():
    cur = mysql.connection.cursor()
    cur.callproc('sp_get_recipients')
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
        cur.callproc('sp_add_recipient', (organization, address, city, state, zip_code, contact, email, phone, description))
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
    cur.callproc('sp_get_recipient_by_id', (id,))
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
        cur.callproc('sp_update_recipient', (id, organization, address, city, state, zip_code, contact, email, phone, description))
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
        cur.callproc('sp_delete_recipient', (id,))
        mysql.connection.commit()
        flash('Recipient deleted!', 'success')
    except Exception as e:
        print("Error deleting recipient:", e)
        flash('Error deleting recipient.', 'danger')
    return redirect(url_for('recipients'))

# DELIVERIES CRUD METHODS
# Base Delivery Route - SELECT all Deliveries
@app.route('/deliveries')
def deliveries():
    cur1 = mysql.connection.cursor()
    cur1.callproc('sp_get_deliveries')
    deliveries_data = cur1.fetchall()
    cur1.close()

    cur2 = mysql.connection.cursor()
    cur2.callproc('sp_get_recipient_dropdown')
    recipients = cur2.fetchall()
    cur2.close()

    cur3 = mysql.connection.cursor()
    cur3.callproc('sp_get_active_driver_dropdown')
    drivers = cur3.fetchall()
    cur3.close()

    return render_template(
        "deliveries.html",
        deliveries=deliveries_data,
        recipients=recipients,
        drivers=drivers
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
        cur.callproc('sp_add_delivery', (recipientID, driverID, campaign, date_time, notes))
        mysql.connection.commit()
        flash('Delivery added!', 'success')
    except Exception as e:
        print("Error adding delivery:", e)
        flash('Error adding delivery.', 'danger')
    return redirect(url_for('deliveries'))

# Route to Edit Delivery
@app.route("/edit-delivery/<int:id>")
def edit_delivery(id):
    cur1 = mysql.connection.cursor()
    cur1.callproc('sp_get_delivery_by_id', (id,))
    delivery = cur1.fetchone()
    cur1.close()

    cur2 = mysql.connection.cursor()
    cur2.callproc('sp_get_recipient_dropdown')
    recipients = cur2.fetchall()
    cur2.close()

    cur3 = mysql.connection.cursor()
    cur3.callproc('sp_get_active_driver_dropdown')
    drivers = cur3.fetchall()
    cur3.close()

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
        cur.callproc('sp_update_delivery', (id, recipientID, driverID, campaign, date_time, notes))
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
        cur.callproc('sp_delete_delivery', (id,))
        mysql.connection.commit()
        flash('Delivery deleted!', 'success')
    except Exception as e:
        print("Error deleting delivery:", e)
        flash('Error deleting delivery.', 'danger')
    return redirect(url_for('deliveries'))

# DELIVERIESSUPPLIES CRUD METHODS
# Base Deliveries Supplies Route - SELECT all Deliveries Supplies
@app.route('/deliveries-supplies')
def deliveries_supplies():
    cur1 = mysql.connection.cursor()
    cur1.callproc('sp_get_deliveries_supplies')
    ds_data = cur1.fetchall()
    cur1.close()

    cur2 = mysql.connection.cursor()
    cur2.callproc('sp_get_delivery_dropdown')
    deliveries = cur2.fetchall()
    cur2.close()

    cur3 = mysql.connection.cursor()
    cur3.callproc('sp_get_supply_dropdown')
    supplies = cur3.fetchall()
    cur3.close()

    return render_template(
        "deliveries_supplies.html",
        deliveries_supplies=ds_data,
        deliveries=deliveries,
        supplies=supplies
    )

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

# Route to Edit Delivery Supply
@app.route("/edit-delivery-supply/<int:id>")
def edit_delivery_supply(id):
    cur1 = mysql.connection.cursor()
    cur1.callproc('sp_get_delivery_supply_by_id', (id,))
    ds = cur1.fetchone()
    cur1.close()

    cur2 = mysql.connection.cursor()
    cur2.callproc('sp_get_delivery_dropdown')
    deliveries = cur2.fetchall()
    cur2.close()

    cur3 = mysql.connection.cursor()
    cur3.callproc('sp_get_supply_dropdown')
    supplies = cur3.fetchall()
    cur3.close()

    return render_template("edit_delivery_supply.html", ds=ds, deliveries=deliveries, supplies=supplies)

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
        flash('Database reset!', 'success')
        return index()
    except Exception as e:
        print("Error during RESET:", e)
        flash('Error reseting database.', 'danger')
        return "Database reset failed", 500

if __name__ == '__main__':
    app.run(port=4200, debug=True)