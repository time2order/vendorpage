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

def add_to_yettoapprove(username, password, email, mobile, shop_name, shop_owner_name, map_link, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO yettoapprove (username, password, email, mobile, shop_name, shop_owner_name, map_link, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (username, password, email, mobile, shop_name, shop_owner_name, map_link, category))
    conn.commit()
    conn.close()


def save_product(vendor_username, product_name, product_image, product_price, product_measure, availability):
    conn = get_connection()
    cursor = conn.cursor()



    insert_query = """
    INSERT INTO products (vendor_username, product_name, product_image, product_price, product_measure, availability)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (vendor_username, product_name, product_image, product_price, product_measure, availability)

    cursor.execute(insert_query, values)

    conn.commit()
    conn.close()


def get_products_by_vendor(vendor_username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE vendor_username = %s", (vendor_username,))
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