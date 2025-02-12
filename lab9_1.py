def send_email_smm(service, to, message): 
    print(f"Connecting to {service} service...") 
    print(f"Sending {service} to {to} with details: {message}...")
    print(f"{service} sent.") 

def send_email(to, subject, body): 
    send_email_smm("SMTP server", to, f"Subject: {subject}, Body: {body}")

def send_sms(to, message): 
    send_email_smm("SMS gateway", to, f"Message: {message}")

