# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# STEP 0
print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))


# STEP 1
# Employees in Boston
df_boston = pd.read_sql("""
    SELECT employees.firstName,
           employees.jobTitle
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE offices.city = 'Boston'
""", conn)

print("\nSTEP 1")
print(df_boston)


# STEP 2
# Offices with zero employees
df_zero_emp = pd.read_sql("""
    SELECT offices.officeCode,
           offices.city
    FROM offices
    LEFT JOIN employees
        ON offices.officeCode = employees.officeCode
    GROUP BY offices.officeCode
    HAVING COUNT(employees.employeeNumber) = 0
""", conn)

print("\nSTEP 2")
print(df_zero_emp)


# STEP 3
# All employees and their office city/state if they have one
df_employee = pd.read_sql("""
    SELECT employees.firstName,
           employees.lastName,
           offices.city,
           offices.state
    FROM employees
    LEFT JOIN offices
        ON employees.officeCode = offices.officeCode
    ORDER BY employees.firstName,
             employees.lastName
""", conn)

print("\nSTEP 3")
print(df_employee)


# STEP 4
# Customers who have not placed an order
df_contacts = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           customers.phone,
           customers.salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        ON customers.customerNumber = orders.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY customers.contactLastName
""", conn)

print("\nSTEP 4")
print(df_contacts)


# STEP 5
# Customer contacts and payment information
df_payment = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           payments.amount,
           payments.paymentDate
    FROM customers
    JOIN payments
        ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)

print("\nSTEP 5")
print(df_payment)


# STEP 6
# Employees whose customers have an average credit limit over 90k
df_credit = pd.read_sql("""
    SELECT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           COUNT(customers.customerNumber) AS num_customers
    FROM employees
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

print("\nSTEP 6")
print(df_credit)


# STEP 7
# Products sold: number of orders and total units
df_product_sold = pd.read_sql("""
    SELECT products.productName,
           COUNT(orderdetails.orderNumber) AS numorders,
           SUM(orderdetails.quantityOrdered) AS totalunits
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    GROUP BY products.productCode
    ORDER BY totalunits DESC
""", conn)

print("\nSTEP 7")
print(df_product_sold)


# STEP 8
# Number of different customers who ordered each product
df_total_customers = pd.read_sql("""
    SELECT products.productName,
           products.productCode,
           COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    JOIN orders
        ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode
    ORDER BY numpurchasers DESC
""", conn)

print("\nSTEP 8")
print(df_total_customers)


# STEP 9
# Number of customers per office
df_customers = pd.read_sql("""
    SELECT offices.officeCode,
           offices.city,
           COUNT(customers.customerNumber) AS n_customers
    FROM offices
    JOIN employees
        ON offices.officeCode = employees.officeCode
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode
""", conn)

print("\nSTEP 9")
print(df_customers)


# STEP 10
# Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           offices.city,
           offices.officeCode
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    JOIN orders
        ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails
        ON orders.orderNumber = orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT orderdetails.productCode
        FROM orderdetails
        JOIN orders
            ON orderdetails.orderNumber = orders.orderNumber
        GROUP BY orderdetails.productCode
        HAVING COUNT(DISTINCT orders.customerNumber) < 20
    )
    ORDER BY employees.lastName
""", conn)

print("\nSTEP 10")
print(df_under_20)


# Close connection
conn.close()