import os
import smtplib
import socket
from io import BytesIO     # for handling byte strings
from io import StringIO    # for handling unicode strings
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def message(subject="Python Notification", text="", img=None, attachment=None):
    # build message contents
    msg = MIMEMultipart()
    msg['Subject'] = subject  # add in the subject
    msg.attach(MIMEText(text))  # add text contents

    # check if we have anything given in the img parameter
    if img is not None:
        # if we do, we want to iterate through the images, so let's check that
        # what we have is actually a list
        if type(img) is not list:
            img = [img]  # if it isn't a list, make it one
        # now iterate through our list
        for one_img in img:
            img_data = open(one_img, 'rb').read()  # read the image binary data
            # attach the image data to MIMEMultipart using MIMEImage, we add
            # the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    # we do the same for attachments as we did for images
    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]  # if it isn't a list, make it one

        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                # read in the attachment using MIMEApplication
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            # here we edit the attached file metadata
            file['Content-Disposition'] = f'attachment; filename="{os.path.basename(one_attachment)}"'
            msg.attach(file)  # finally, add the attachment to our message object
    return msg


def send(msg, toAddr=None, server='smtp.gmail.com', port='587'):
    # contain following in try-except in case of momentary network errors
    try:
        # initialise connection to email server, the default is Outlook
        smtp = smtplib.SMTP(server, port)
        # this is the 'Extended Hello' command, essentially greeting our SMTP or ESMTP server
        smtp.ehlo()
        # this is the 'Start Transport Layer Security' command, tells the server we will
        # be communicating with TLS encryption
        smtp.starttls()
        # Reading the credentials
        email = None
        pwd = None
        with open("username.txt", "r", encoding="utf-8") as username_file:
            email = username_file.read()
        with open("password.txt", "r", encoding="utf-8") as password_file:
            pwd = password_file.read()

        # login to outlook server
        smtp.login(email, pwd)
        # send notification to self
        if toAddr is None:
            smtp.sendmail(email, email, msg.as_string())
        else:
            smtp.sendmail(email, toAddr, msg.as_string())
        # disconnect from the server
        smtp.quit()
    except socket.gaierror:
        print("Network connection error, email not sent.")
