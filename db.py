import mysql.connector
import random
import string
from datetime import datetime
mydb = mysql.connector.connect(
  host="sql6.freesqldatabase.com",
  user="sql6439270",
  password="v6nSCFAC8T",
  database="sql6439270"
)
def get_random_password():
    random_source = string.ascii_letters + string.digits
    # select 1 uppercase
    password = random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol

    # generate other characters
    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

trans_id = get_random_password()
mycursor = mydb.cursor()
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
#mycursor.execute("CREATE TABLE account_data (id INT AUTO_INCREMENT PRIMARY KEY, mobile VARCHAR(255), account_no VARCHAR(255), transaction_id INT(20), balance INT(20), credit INT(20), debit INT(20), date VARCHAR(255))")
#mycursor.execute("ALTER TABLE customers DROP COLUMN address")
#sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#val = ("8879166971", "ACLS7LCdkj", ac_no, 1000, 1000, None, formatted_date)
#mycursor.execute(sql,val)
#mydb.commit()
#print(mycursor.rowcount, "record inserted")
#number=(str(8879166971),)
#mycursor.execute("SELECT * FROM customers WHERE mobile = %s", (number))
#mycursor.execute("SELECT * FROM customers WHERE mobile = %s", (number))
#x = mycursor.fetchone()
#print(x)
#mycursor.execute("SELECT balance FROM account_data WHERE account_no='ACCQgnTF3z' ORDER BY id DESC LIMIT 1")
#x=mycursor.fetchone()
#print(x[0])
mycursor.execute("SELECT * FROM account_data")
x = mycursor.fetchall()
for y in x:
    print(y)
#mycursor.execute("SELECT balance FROM account_data WHERE mobile='8879166971' ORDER BY id DESC LIMIT 1")
#x = mycursor.fetchall()
#for y in x:
#    print(y)
#mycursor.execute("SELECT * FROM customers")
#x = mycursor.fetchall()
#for y in x:
#    print(y)
#mycursor.execute("SHOW TABLES")
#for x in mycursor:
#    print(x)
#mydb.close()
#mycursor.execute("DELETE FROM account_data WHERE id IN (6,7,8,9)")
#mydb.commit()
#print("Records Deleted")
#sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#val = ("8879166971","ACLS7LCdkj", None, 100, None, None, None)
#mycursor.execute(sql,val)
#mydb.commit()
#print(mycursor.rowcount, "record inserted")
#mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s", (number))
#x = mycursor.fetchall()
#for y in x:
#    print(y[0])
#print(x)
#print(type(x))
#mycursor.execute("CAST x AS unsigned")
#entered_am = '1000 rupees'
#entered_am = entered_am.split('r')
#entered_am = entered_am[0]
#print(int(entered_am))