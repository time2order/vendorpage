import os
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
import db
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.validate_user(username, password):
            session['vendor_username'] = username
            return redirect(url_for('vendor_dashboard'))
        elif db.user_exists(username):
            error = 'Your account is pending approval.'
        elif  db.isrejected(username):
            error = 'Your account has been rejected.'  
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']
        mobile = request.form['mobile']
        shop_name = request.form['shop_name']
        shop_owner_name = request.form['shop_owner_name']
        map_link = request.form['map_link']
        shop_address = request.form['shop_address']
        pincode = request.form['pincode']
        category = request.form['category']

        if password != repassword:
            error = 'Passwords do not match.'
        elif db.user_exists(username):
            error = 'Username already exists.'
        else:
            db.add_to_yettoapprove(
                username, password, email, mobile,
                shop_name, shop_owner_name, map_link,
                shop_address, pincode, category
            )
            return "Registration submitted for approval!"

    return render_template('register.html', error=error)


@app.route('/vendor/dashboard')
def vendor_dashboard():
    if 'vendor_username' not in session:
        return redirect(url_for('login'))
    return render_template('vendor_dashboard.html', vendor_username=session['vendor_username'])

@app.route('/vendor/add-product', methods=['GET'])
def add_product():
    if 'vendor_username' not in session:
        return redirect(url_for('login'))
    return render_template('add_product.html', vendor_username=session['vendor_username'])
@app.route('/vendor/save-product', methods=['POST'])
def save_product():
    if 'vendor_username' not in session:
        return redirect(url_for('login'))

    vendor_username = session['vendor_username']
    vendor_id = db.get_vendor_id_by_username(vendor_username)  # You need to implement this DB function

    product_name = request.form['product_name']
    product_price = request.form['product_price']
    product_measure = request.form['product_measure']
    availability = 'Available' if 'availability' in request.form else 'Not Available'

    image_file = request.files['product_image']
    if image_file and image_file.filename:
        extension = os.path.splitext(image_file.filename)[1]
        new_filename = f"{vendor_id}_{product_name.replace(' ', '_')}{extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        image_file.save(filepath)
    else:
        filepath = None
        new_filename = None

    db.save_product(
        vendor_id=vendor_id,  # Store by ID
        product_name=product_name,
        product_image=new_filename,
        product_price=product_price,
        product_measure=product_measure,
        availability=availability
    )

    return {"message": "Product added successfully!"}, 200


@app.route('/vendor/products', methods=['GET'])
def list_products():
    if 'vendor_username' not in session:
        return redirect(url_for('login'))
    vendor_username = session['vendor_username']
    vendor_id = db.get_vendor_id_by_username(vendor_username)
    products = db.get_products_by_vendor(vendor_id)  # Fetch products from the database
    return render_template('list_products.html', products=products)

@app.route('/vendor/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'vendor_username' not in session:
        return redirect(url_for('login'))

    vendor_username = session['vendor_username']
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        product_measure = request.form['product_measure']
        availability = 'Available' if 'availability' in request.form else 'Not Available'

        # Handle image
        image_file = request.files['product_image']
        if image_file and image_file.filename:
            extension = os.path.splitext(image_file.filename)[1]
            new_filename = f"{vendor_username}_{product_name.replace(' ', '_')}{extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            image_file.save(filepath)
        else:
            # If no new image is uploaded, retain the existing image filename
            existing_product = db.get_product_by_id(product_id)
            new_filename = existing_product['product_image']

        # Update product in the database
        db.update_product(
            product_id=product_id,
            product_name=product_name,
            product_image=new_filename,
            product_price=product_price,
            product_measure=product_measure,
            availability=availability
        )

        flash("Product updated successfully!")
        return redirect(url_for('list_products'))

    # Fetch the existing product data to pre-fill the form
    product = db.get_product_by_id(product_id)
    return render_template('edit_product.html', product=product)

@app.route('/vendor/update-status', methods=['POST'])
def update_status():
    status = request.form.get('status')
    username = session.get('vendor_username')  # assuming session holds the logged-in vendor's username
    print(status,username)
    if not username:
        return "Unauthorized", 401

    if db.update_vendor_status(username, status):
        return redirect('/vendor/dashboard')
    else:
        return "Failed to update", 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
