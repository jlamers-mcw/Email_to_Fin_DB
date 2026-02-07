import pytest
import pytz

from tqdm import tqdm
from datetime import datetime

from src.scraper import authenticate
from src.scraper import get_all_email_IDs_from_sender
from src.scraper import get_email_from_ID

def test_authenticate():
    """
    TODO
    """
    try:
        authenticate()
        assert True
    except Exception as e:
        print(e)
        assert False

def test_get_all_email_IDs_from_sender_normal_input():
    """
    TODO
    """
    list_of_normal_senders = [
                "webalerts@uwcu.org",
                "venmo@venmo.com",
                "noreply@reply.jsonline.com"
            ]
    
    imap = authenticate() 
    
    for sender in list_of_normal_senders:
        assert len(get_all_email_IDs_from_sender(imap,sender)) > 0

def test_get_email_from_ID_uwcu():
    """
    TODO
    """
    test_json = {
                "from":"UW Credit Union <webalerts@uwcu.org>",
                "subject":"Card Transaction Notification",
                "date":datetime.strptime(
                    "May 24 2022 3:53 PM",
                        "%b %d %Y %I:%M %p"
                    )
            }
    
    test_json["date"] = test_json["date"].astimezone(pytz.utc)


    imap = authenticate()

    email_ids = get_all_email_IDs_from_sender(imap,"webalerts@uwcu.org")

    emails_data = []

    for email_id in tqdm(email_ids):
        emails_data.append(get_email_from_ID(imap,email_id))

    emails_data_contains_test = False

    for emails_data in tqdm(emails_data):
        for msg_data in emails_data:

            if (
                    msg_data["from"] == test_json["from"] and
                    msg_data["subject"] == test_json["subject"] and
                    msg_data["date"].replace(second=0,microsecond=0) == test_json["date"].replace(second=0,microsecond=0)
                ):
                    emails_data_contains_test = True

    assert emails_data_contains_test

