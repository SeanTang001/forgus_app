import smtplib, imaplib, re, pprint, email, base64, time, html, json

#setup recieve sever
def rec_conn_init(email_cred):
    recieve_server = imaplib.IMAP4_SSL(email_cred["server"])
    recieve_server.login(email_cred["username"], email_cred["password"])
    return recieve_server

#check through mail box
def check_response(recieve_server, num):
    response = []
    num = str(num[0].decode('ascii')).split()
    for i in range(len(num)):
        typ, msg_data = recieve_server.fetch(num[i], 'RFC822')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = (email.message_from_bytes(response_part[1]))
                response.append(msg)
    return response

def sort_email(email, results):
    print(str(email))
    print(email.get_payload())
    if "@txt.voice.google.com" in email["From"]:
        text = email.get_payload()[0].get_payload()
        print(text)
        a,b,c = text.partition(r'.com>')
        a,b,c = c.partition('^>')
        print(a)
        try:
            payload = json.loads(html.unescape(a))
            a, b, c = email["From"].partition("<")
            payload["uid"] = a.replace('"', '').replace('(','').replace(')','').replace('-', '').replace(' ', '')
            results.append(payload)
        except:
            pass
    else:
        pass
    return results

def mail_checker(recieve_server):
    recieve_server.select('Inbox')
    typ, num = recieve_server.search(None, '(UNSEEN)')
    responses = check_response(recieve_server, num)
    print(responses)
    results = []
    for i in responses:
        results = sort_email(i, results)
    return results

def test():
    recieve_server = rec_conn_init({"server":"imap.gmail.com","username":"forgus003@gmail.com", "password":"password"})
    results = []
    while True:
        time.sleep(2)
        results = mail_checker(recieve_server)
        print(results)