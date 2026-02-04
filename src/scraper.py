import imaplib
import email
import pandas as pd
import re

from tqdm import tqdm

df = pd.DataFrame({
        "Date": [],
        "Card":[],
        "Amount":[],
        "Merchant":[],
        "Type":[]
    })

card_pattern = r'<strong>Card:</strong>\s*([^<]+)'
amount_pattern = r'<strong>Amount:</strong>\s*([^<]+)'
merchant_pattern = r'<strong>Merchant:</strong>\s*([^<]+)'

user = "jakelamers931@gmail.com"
pwd = "vpdw vggh mghr phqd"

m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
m.login(user, pwd)
m.select('inbox')

# Search for emails from the specific sender
status, messages = m.search(None, 'FROM "webalerts@uwcu.org"')

# Convert the byte string to a list of email IDs
email_ids = messages[0].split()

print(f"Found {len(email_ids)} emails\n")

# Loop through each email
for email_id in tqdm(email_ids):
    # Fetch the email by ID
    status, msg_data = m.fetch(email_id, '(RFC822)')
    
    # Parse the email content
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Parse the raw email
            msg = email.message_from_bytes(response_part[1])
            
            # Get email details
            subject = msg['subject']
            from_addr = msg['from']
            date = msg['date']
            
            # Extract the email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()

                        card = re.search(card_pattern, html).group(1).strip()
                        amount = re.search(amount_pattern, html).group(1).strip()
                        merchant = re.search(merchant_pattern, html).group(1).strip()
                        
                        df.loc[len(df)] = [
                                    msg['date'],
                                    card,
                                    amount,
                                    merchant,
                                    ''
                                ]
                        
                        break
            else:
                body = msg.get_payload(decode=True).decode()

                
                try:
                    card = re.search(card_pattern, body).group(1).strip()
                    amount = re.search(amount_pattern, body).group(1).strip()
                    merchant = re.search(merchant_pattern, body).group(1).strip()
                        
                    df.loc[len(df)] = [
                                msg['date'],
                                card,
                                amount,
                                merchant,
                                ''
                            ]
                except:
                    pass

df.to_csv('your_file_name.csv', index=False)

m.close()
m.logout()
