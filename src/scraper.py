import imaplib
import email
import pandas as pd
import re
import json

from tqdm import tqdm


def get_all_email_IDs_from_sender(imap,sender):
    """
    Returns a list of all email ids in a gmail inbox

    Args:
        parameter (str): the email address you want to collect
        all emails from.

        imap (@TODO): @TODO

    Returns:
        List: a list of email IDs
    """

    imap.select('inbox')

    # Search for emails from the specific sender
    status, messages = imap.search(None, 'FROM "webalerts@uwcu.org"')

    # Convert the byte string to a list of email IDs
    return messages[0].split()



def get_email_from_ID(imap, ID):
    """
    Returns a json of the important info from an email

    Args:
        ID (str): the ID of the email you would like to get

        imap (@TODO): @TODO

    Returns:
        List: a list of jsons where each json contatins
        contains "from", "subject", "date" and "body"
    """
    # Fetch the email by ID
    status, msg_data = imap.fetch(ID, '(RFC822)')

    msgs_data = []
    
    # Parse the email content
    for response_part in msg_data:
        msg_data = {
                    "from":"",
                    "subject":"",
                    "date":"",
                    "body":""
                }

        if isinstance(response_part, tuple):
        
            # Parse the raw email
            msg = email.message_from_bytes(response_part[1])
            
            # Get email details
            msg_data["subject"] = msg['subject']
            msg_data["from"] = msg['from']
            msg_data['date'] = msg['date']

            # Extract the email body
            if msg.is_multipart():

                for part in msg.walk():

                    if part.get_content_type() == "text/plain"
                    
                        msg_data["body"] += part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

        msgs_data.append(msg_data)
        
    return msgs_data



def parse_email_html(msg_data):
    pass

def scrap():
    pass



""""
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

"""
