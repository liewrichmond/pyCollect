import imaplib
import smtplib
import cryptoFunctions

def connectSMTP():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    return server

def connectIMAP():
    master = input("Enter Master Password: ")
    server = imaplib.IMAP4_SSL('imap.gmail.com')
    credentials = cryptoFunctions.decrypt(master)
    server.login(credentials['username'], credentials['password'])
    server.list()
    server.select('inbox')
    result, data = server.uid('search', None, "ALL") # search and return uids instead
    latest_email_uid = data[0].split()[-1]
    result, data = server.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    print(raw_email)
    

if __name__ == "__main__":
    connectIMAP()


    