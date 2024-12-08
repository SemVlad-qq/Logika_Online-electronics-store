import sqlite3

db = sqlite3.connect('Shop.db')

cursor = db.cursor()

#cursor.execute("""CREATE TABLE products (
    #product_id INTEGER PRIMARY KEY,
    #name TEXT NOT NULL,
    #category TEXT NOT NULL,
    #price REAL NOT NULL
#)""")

#cursor.execute("""CREATE TABLE customers(
    #customer_id INTEGER PRIMARY KEY,
    #first_name TEXT NOT NULL,
    #last_name TEXT NOT NULL,
    #email REAL NOT NULL UNIQUE
#)""")

#cursor.execute("""CREATE TABLE orders(
    #order_id INTEGER PRIMARY KEY,
    #customer_id INTEGER NOT NULL,
    #product_id INTEGER NOT NULL,
    #quantity INTEGER NOT NULL,
    #order_date DATE NOT NULL,
    #FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    #FOREIGN KEY (product_id) REFERENCES products(product_id)
#)""")
choice = input('Оберіть дію')

#Додати продукт у БД
if choice == '1':
    id = input("id ¯\_(ツ)_/¯")
    name_p = input("Ім'я")
    category_p = input("Категорія")
    price_p = input("Ціна")
    #Збереження змін в базі даних
    yes_no = input("Ви хочете ви зберегти зміні в Бази Данних? (Так/Ні)")
    if yes_no == "Так":
        cursor.execute(
            "INSERT INTO products (product_id, name, category, price) "
            "VALUES (?, ?, ?, ?)",
            (id, name_p, category_p, price_p)
        )
    else:
        print("-")

#Список усіх продуктів
elif choice == '2':
    cursor.execute("SELECT * FROM products")
    print(cursor.fetchall())

#Додати кліента у БД
elif choice == '3':
    id = input("id ¯\_(ツ)_/¯")
    name_c = input("Ім'я")
    lastname_c = input("Фамілія")
    email_c = input("Емеїл")
    #Збереження змін в базі даних
    yes_no = input("Ви хочете ви зберегти зміні в Бази Данних? (Так/Ні)")
    if yes_no == "Так":
        cursor.execute(
            "INSERT INTO customers (customer_id, first_name, last_name, email) "
            "VALUES (?, ?, ?, ?)",
            (id, name_c, lastname_c, email_c))
    else:
        print("-")

#Список усіх кліентів
elif choice == '4':
    cursor.execute("SELECT * FROM customers")
    print(cursor.fetchall())

#Додати заказ у БД
elif choice == '5':
    o_id = input("id order ¯\_(ツ)_/¯")
    c_id = input("id customer ¯\_(ツ)_/¯")
    p_id = input("id product ¯\_(ツ)_/¯")
    c_quantity = input("Кількість")
    order_date = input("Дата заказу")
    #Збереження змін в базі даних
    yes_no = input("Ви хочете ви зберегти зміні в Бази Данних? (Так/Ні)")
    if yes_no == "Так":
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, product_id, quantity, order_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (o_id, c_id, p_id, c_quantity, order_date))
    else:
        print("-")

#Список усіх заказів
elif choice == '6':
    cursor.execute("SELECT * FROM orders")
    print(cursor.fetchall())



#Сумарний обсяг продажів:
elif choice == '10':
    cursor.execute("""
    SELECT SUM(products.price * orders.quantity) AS total_price
    FROM products
    JOIN orders ON products.product_id = orders.product_id; """)
    result = cursor.fetchone()
    if result and result[0] is not None:
        print(f"Сумарний обсяг продажів: {result[0]}")
    else:
        print("Немає заказів")

#Кількість замовлень на кожного клієнта
elif choice == '11':
    client = input("ID кліента, закази якого треба знайти ")
    cursor.execute("""
    SELECT COUNT(*) AS order_count
    FROM orders
    WHERE customer_id = ?; """, (client,))
    result = cursor.fetchone()
    if result and result[0] is not None:
        print(f"Пользователь с id {client} робив {result[0]} заказів")
    else:
        print("Немає такого пользователя")

#Середній чек замовлення
elif choice == "12":
    cursor.execute("""
    SELECT 
        COUNT(*) AS order_quantity,
        SUM(products.price * orders.quantity) AS total_price,
        SUM(products.price * orders.quantity) / COUNT(*) AS average_order_price
    FROM orders
    JOIN products ON products.product_id = orders.product_id; """)
    result = cursor.fetchone()
    if result:
        print(f"Середній чек замовлення: {result[2]}")
    else:
        print("Немає заказів або немає/не працює База Данних")

#Найбільш популярна категорія товарів: (У процессі)
elif choice == "13":
    cursor.execute("""
    SELECT 
        products.category, 
        COUNT(products.category) AS category_count
    FROM 
        orders
    JOIN 
        products 
    ON 
        orders.product_id = products.product_id
    GROUP BY 
        products.category
    ORDER BY 
        category_count DESC
    LIMIT 1;""")
    result = cursor.fetchone()
    if result:
        print(f"Сама популярна категорія це - {result[0]} (Усього {result[1]} заказів)")
    else:
        print("Немає заказів або немає/не працює База Данних")

#Загальна кількість товарів кожної категорії
elif choice == "14":
    cursor.execute("""
    SELECT category, COUNT(*) as category_quantity FROM products 
    GROUP BY category; """)
    result = cursor.fetchall()
    if result:
        print("Товари по категоріям:")
        for row in result:
            print(f"Категорія: {row[0]}, Кількість товарів: {row[1]}")
    else:
        print("Немає товарів у категоріях.")

#Оновлення цін (Оновіть ціни товарів в категорії "смартфони" на 10% збільшення.
elif choice == "15":
    cursor.execute("""
    UPDATE products
    SET price = price * 1.1
    WHERE category = 'Смартфони';""")
    result = cursor.fetchall()
    if result:
        print("+")
    else:
        print("-")





db.commit()

db.close()