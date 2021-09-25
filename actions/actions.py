from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from twilio.rest import Client
import string
import random
import mysql.connector
from datetime import datetime
#rasa run -m models --enable-api --cors "*" --debug
mydb = mysql.connector.connect(
  host="sql6.freesqldatabase.com",
  user="sql6439270",
  password="v6nSCFAC8T",
  database="sql6439270"
)
global balance
def get_random_password():
    random_source = string.ascii_letters + string.digits
    password = random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    for i in range(6):
        password += random.choice(random_source)
    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password
class ActionMobile(Action):
    def name(self) -> Text:
        return "action_mobile"
    
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global number
        number = tracker.get_slot('mobile')
        c_c = '+91'
        global main
        main = (c_c+str(number))
        number = (str(number),)
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM customers WHERE mobile = %s", (number))
        x = mycursor.fetchone()
        mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s ORDER BY id DESC LIMIT 0,1", (number))
        #mycursor.execute("SELECT account_no FROM account_data ORDER BY id DESC LIMIT 0,1")
        y = mycursor.fetchone()
        if x!=None and y==None:
            client = Client('AC2afd3bcf5d81ab07b23939997f6a4c73', 'c1c700fe06989ac152912f14bbd6665a')
            verify = client.verify.services('VAf62b701da03f80654635296039794718')
            verify.verifications.create(to=main, channel='sms')
            dispatcher.utter_message("Please enter the OTP sent to you in the format 'otp XXXXXX'")
        else:
            dispatcher.utter_message("Oops!, Looks like you haven't registered with us yet please head on to Login and Registration\nor you already have an A/C number")
        return []
class ActionOtp(Action):
    def name(self) -> Text:
        return "action_otp"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        otp = tracker.get_slot('otp')
        client = Client('AC2afd3bcf5d81ab07b23939997f6a4c73', 'c1c700fe06989ac152912f14bbd6665a')
        verify = client.verify.services('VAf62b701da03f80654635296039794718')
        result = verify.verification_checks.create(to=main, code=str(otp))
        if result.status=='approved':
            dispatcher.utter_message("Hurray! You have been authenticated")
            initial='AC'
            global ac_no
            ac_no = get_random_password()
            ac_no = initial+ac_no
            dispatcher.utter_message("Congratulations your A/C Number is:\n{}".format(ac_no))
            mycursor = mydb.cursor()
            sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (number[0],ac_no , None, None, None, None, None)
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted")
        elif result.status=='pending':
            dispatcher.utter_message("Oops, Authentication Failed Check if your Mobile Number is the one you used while registration or you can request for OTP resend by saying 'yes'")
        return []
class ActionACNumber(Action):
    def name(self) -> Text:
        return "action_ac_number"
    
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            account_no = tracker.get_slot('ac_number')
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("SELECT balance FROM account_data WHERE account_no=%s ORDER BY id DESC LIMIT 1",(account_no,))
            x = mycursor.fetchone()[0]
            if x!=None:
                response = "Great! continue your banking tasks!!!"
                dispatcher.utter_message(response)
            else:
                response = "Looks like you never created a new account start your banking journey by creating a new account"
                dispatcher.utter_message(response)
            return []
class ActionTransaction(Action):
    def name(self) -> Text:
        return "action_transaction"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_no = tracker.get_slot('ac_number')
        number=tracker.get_slot('mobile')
        number = str(number)
        mycursor = mydb.cursor(buffered=True)
        #mycursor.execute("SELECT TOP 1 balance FROM account_data WHERE mobile = %s ORDER BY id DESC LIMIT 0,1", (number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s", (number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile=%s ORDER BY id DESC LIMIT 1",(number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile=%s ORDER BY id DESC LIMIT 1",(number,))
        mycursor.execute("SELECT balance FROM account_data WHERE account_no=%s ORDER BY id DESC LIMIT 1",(account_no,))
        x = mycursor.fetchone()[0]
        if x!=None:
            response="Your A/C balance is {} rupees".format(x)
            dispatcher.utter_message(response)
        else:
            mycursor.execute("SELECT account_no FROM account_data WHERE mobile = %s", (number,))
            ac_no = mycursor.fetchone()[0]
            sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (number,ac_no , None, 0, None, None, None)
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted")
            response = "No balance available, hence setting it to default '0 rupees'"
            dispatcher.utter_message(response)
        return []
class ActionCredit(Action):
    def name(self) -> Text:
        return "action_credit"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_no = tracker.get_slot('ac_number')
        number = tracker.get_slot('mobile')
        number = str(number)
        entered_am = tracker.get_slot('amount')
        entered_am = entered_am.split(' r')
        entered_am = entered_am[0]
        entered_am = int(entered_am)
        mycursor = mydb.cursor(buffered=True)
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s ORDER BY id DESC LIMIT 0,1", (number))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s", (number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile=%s ORDER BY id DESC LIMIT 1",(number,))
        mycursor.execute("SELECT balance FROM account_data WHERE account_no=%s ORDER BY id DESC LIMIT 1",(account_no,))
        x = mycursor.fetchone()
        x = x[0]
        if x>=0:
            x = x + entered_am
            trans_id = get_random_password()
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            ac_no = account_no
            sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (number,ac_no , trans_id, x, entered_am, None,formatted_date )
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted")
            response = "{} rupees were credited to your account your current account balance is: {} rupees".format(entered_am,x)
            dispatcher.utter_message(response)
        return []

class ActionDebit(Action):
    def name(self) -> Text:
        return "action_debit"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_no = tracker.get_slot('ac_number')
        number = tracker.get_slot('mobile')
        number = str(number)
        entered_am = tracker.get_slot('amount')
        entered_am = entered_am.split(' r')
        entered_am = entered_am[0]
        entered_am = int(entered_am)
        mycursor = mydb.cursor(buffered=True)
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s ORDER BY id DESC LIMIT 0,1", (number))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s", (number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile=%s ORDER BY id DESC LIMIT 1",(number,))
        mycursor.execute("SELECT balance FROM account_data WHERE account_no=%s ORDER BY id DESC LIMIT 1",(account_no,))
        x = mycursor.fetchone()[0]
        if x>=0:
            x = x - entered_am
            trans_id = get_random_password()
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            #mycursor.execute("SELECT account_no FROM account_data WHERE mobile = %s", (number,))
            ac_no = account_no
            sql = "INSERT INTO account_data (mobile, account_no, transaction_id, balance, credit, debit, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (number,ac_no , trans_id, x, None, entered_am,formatted_date )
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted")
            response = "{} rupees were debited from your account, your current account balance is: {} rupees".format(entered_am,x)
            dispatcher.utter_message(response)
        else:
            response="You don't have enough funds for this transaction, sorry :("
            dispatcher.utter_message(response)
        return []

class ActionDisplayBalance(Action):
    def name(self) -> Text:
        return "action_display_balance"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        account_no = tracker.get_slot('ac_number')
        number = tracker.get_slot('mobile')
        number = str(number)
        entered_am = tracker.get_slot('amount')
        entered_am = entered_am.split(' r')
        entered_am = entered_am[0]
        entered_am = int(entered_am)
        mycursor = mydb.cursor(buffered=True)
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s ORDER BY id DESC LIMIT 0,1", (number))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile = %s", (number,))
        #mycursor.execute("SELECT balance FROM account_data WHERE mobile=%s ORDER BY id DESC LIMIT 1",(number,))
        mycursor.execute("SELECT balance FROM account_data WHERE account_no=%s ORDER BY id DESC LIMIT 1",(account_no,))
        x = mycursor.fetchone()[0]
        if x>=0:
            response = "Your Account balance is: {} rupees".format(x)
            dispatcher.utter_message(response)
        return []
class ActionMF(Action):
    def name(self) -> Text:
        return "action_mf"
    def run(self, dispatcher:CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent=='large_cap':
            response = """
Name : JM Large Cap Fund
Type : Large Cap
Returns 1 year" : 32.56%
Returns 3 year" : 12.37%
Returns 5 year" : 11.28%   

Name : Invesco India Largecap Fund
Type : Large Cap
Returns 1 year : 46.32%
Returns 3 year : 14.44%
Returns 5 year : 14.68%
"""
            dispatcher.utter_message(response)
        elif intent=='mid_cap':
            response = """
Name: SBI Focused Equity Fund-Reg(G)
Type : Equity - Midcap
Returns 1 year: 56.22%
Returns 3 years: 17.87%
Returns 5 years: 16.59%

Name: IIFL Focused Equity Fund-Reg(G)
Type : Equity - Midcap
Returns 1 year: 63.64%
Returns 3 years: 23.96%
Returns 5 years: 18.74%            
"""
            dispatcher.utter_message(response)
        elif intent=='small_cap':
            response="""
Name : ICICI Prudential Smallcap Fund
Type : Small Cap
Returns 1 year : 117.73%
Returns 3 year : 26.37%
Returns 5 year : 19.15%

Name : SBI Small Cap Fund Direct (G)
Type : Small Cap
Returns 1 year : 91.46%
Returns 3 year : 25.44%
Returns 5 year : 23.73%            
"""
            dispatcher.utter_message(response)
        elif intent=='multi_cap':
            response = """
Name : Quant Active Fund -Direct(G)
Type : Multi Cap
Returns 1 year : 98.13%
Returns 3 year : 30.31%
Returns 5 year : 23.84%            
"""
        return []