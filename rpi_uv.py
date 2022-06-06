import spidev
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage



#bus and CE pin selection
bus = 0
device = 0

#initiate SPI
spi = spidev.SpiDev()
spi.open(bus, device)

#set transmit speed
spi.max_speed_hz = 1024

#uv index (0-11+)
uvi = 0
#nominal uv level i.e MODERATE
level = ''



#determine uv index nominal value
def get_level(uvi):
    if uvi < 0: lvl = ('Error: Negative input!')

    if uvi < 6: lvl = 'MODERATE'
    elif uvi < 8:   lvl = 'HIGH'
    elif uvi < 11:  lvl = 'VERY HIGH'
    else: lvl = 'EXTREME'

    return lvl



### DEFINE EMAIL SETTINGS ###
#desired email address
email = 'put@email.here'
#password of email account
password = 'password123'
#domain of provider smtp
domain = 'put.smtp.here'
#port of provider smtp
port = 587



#sent email alert
def alert(uvi, level):
    #get current time and format string to HH:MM
    now = datetime.now()
    now = now.strftime("%H:%M")

    #fstring email template for alert
    template = f'WARNING! UV exposure of {uvi} ({level}) recorded at {now}'

    #compile message and define fields
    msg = EmailMessage()
    msg.set_content(template)
    msg['Subject'] = 'UV Alert!'
    msg['From'] = email
    msg['To'] = email

    print(msg)

    #initiate smtp object
    server = smtplib.SMTP(domain, port)

    try:
        #begin smtp handshake and login
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
    except:
        ('SMTP connection failed!')
        server.quit()
        return

    #send alert to user inbox
    try:
        server.send_message(msg)
        print('Alert sent')
    except:
        print('Email sending failed!')

    #kill connection
    server.quit()



while True:
    #read uv index from Arduino via SPI
    uvi = spi.readbytes(0)
    uvi = uvi[0]

    print(uvi)

    #uv index of > 2 is considered potentially harmful, hence alerting if above 2
    if uvi > 2:
        alert(uvi, get_level(uvi))

    ### DEFINE TIME INTERVAL ###
    #Set time between readings in seconds, default 3600 (1 hour)
    time.sleep(3600)
