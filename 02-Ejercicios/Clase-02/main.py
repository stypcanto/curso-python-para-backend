from emailnotification import EmailNotification
from whatsapp_notifiaction import WhatsAppNotification

email = EmailNotification()
email.send("Juan","Hola ")

whatsapp = WhatsAppNotification()
whatsapp.send("Pedro","Hola ")
