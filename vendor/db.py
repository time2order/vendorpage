import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Vikas@5599',
        database='Time2order'
    )

def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def user_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM yettoapprove WHERE username=%s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
def isrejected(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rejectedlist WHERE username=%s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
def add_to_yettoapprove(username, password, email, mobile, shop_name, shop_owner_name, map_link, shop_address, pincode, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO yettoapprove (
            username, password, email, mobile_number,
            shop_name, shop_owner_name, map_link,
            shop_address, pincode, category
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        username, password, email, mobile,
        shop_name, shop_owner_name, map_link,
        shop_address, pincode, category
    ))
    conn.commit()
    conn.close()



def save_product(vendor_id, product_name, product_image, product_price, product_measure, availability):
    conn = get_connection()
    cursor = conn.cursor()



    insert_query = """
    INSERT INTO products (vendor_id, product_name, product_image, product_price, product_measure, availability)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (vendor_id, product_name, product_image, product_price, product_measure, availability)

    cursor.execute(insert_query, values)

    conn.commit()
    conn.close()


def get_products_by_vendor(vendor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE vendor_id = %s", (vendor_id,))
    products = cursor.fetchall()
    conn.close()
    
    # Convert fetched data into a list of dictionaries
    product_list = []
    for product in products:
        product_dict = {
            'id': product[0],  # Assuming the first column is the product ID
            'product_name': product[2],  # Assuming the second column is the product name
            'product_image': product[3],  # Assuming the third column is the product image
            'product_price': product[4],  # Assuming the fourth column is the product price
            'product_measure': product[5],  # Assuming the fifth column is the product measure
            'availability': product[6]  # Assuming the sixth column is the availability
        }
        product_list.append(product_dict)

    return product_list

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return {
            'id': product[0],
            'product_name': product[2],
            'product_image': product[3],
            'product_price': product[4],
            'product_measure': product[5],
            'availability': product[6]
        }
    return None

def update_product(product_id, product_name, product_image, product_price, product_measure, availability):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products 
        SET product_name = %s, product_image = %s, product_price = %s, product_measure = %s, availability = %s 
        WHERE id = %s
    """, (product_name, product_image, product_price, product_measure, availability, product_id))
    conn.commit()
    conn.close()
    
def get_vendor_id_by_username(username):
    try:
        connection = get_connection()  # Assuming you have a function that returns a DB connection
        cursor = connection.cursor(dictionary=True)  # Use `dictionary=True` for dict-style result access
        query = "SELECT id FROM vendors WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result['id'] if result else None
    except Exception as e:
        print("Error fetching vendor ID:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def update_vendor_status(username, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE vendors SET shop_status = %s WHERE username = %s", (status, username))
        conn.commit()
        print(status,username)
        return True
    except Exception as e:
        print("Error updating vendor status:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

