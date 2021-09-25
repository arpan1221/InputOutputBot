from twilio.rest import Client
import random
import string
client = Client('AC2afd3bcf5d81ab07b23939997f6a4c73', 'c1c700fe06989ac152912f14bbd6665a')
verify = client.verify.services('VAf62b701da03f80654635296039794718')
verify.verifications.create(to='+918879166971', channel='sms')
#VAf62b701da03f80654635296039794718


#result = verify.verification_checks.create(to='+918879166971', code='123456')
#print(result.status)
#result = verify.verification_checks.create(to='+918879166971', code='116434')
#print(result.status)
#x='+91'
#y='8879166971'
#pl = '+91'
#y = 8879166971
#print(pl+str(y))
#initial='AC'
#def get_random_password():
#    random_source = string.ascii_letters + string.digits
    # select 1 uppercase
#    password = random.choice(string.ascii_uppercase)
    # select 1 digit
#    password += random.choice(string.digits)
    # select 1 special symbol

    # generate other characters
#    for i in range(6):
#        password += random.choice(random_source)

#    password_list = list(password)
    # shuffle all characters
#    random.SystemRandom().shuffle(password_list)
#    password = ''.join(password_list)
#    return password

#ac_no = get_random_password()
#print(initial+ac_no)