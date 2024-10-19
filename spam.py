import re
import json
import time
import ctypes
import string
import random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor


session = requests.Session()

url_base = (
    "https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?"
    "gsessionid={}&VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)"
    "&RID=rpc&SID={}&CI=0&AID=0&TYPE=xmlhttp&zx={}&t=1"
)

get_gsessionid_url = (
    "https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?"
    "VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)"
    "&RID={}&CVER=22&X-HTTP-Session-Id=gsessionid&zx={}&t=1"
)

payload_data = "count=1&ofs=2&req0___data__=%7B%22database%22%3A%22projects%2Ftasuketsu2%2Fdatabases%2F(default)%22%2C%22addTarget%22%3A%7B%22documents%22%3A%7B%22documents%22%3A%5B%22projects%2Ftasuketsu2%2Fdatabases%2F(default)%2Fdocuments%2Fpublic%2F{}%22%5D%7D%2C%22targetId%22%3A4%7D%7D"
payload_data2 = "count=1&ofs=3&req0___data__=%7B%22database%22%3A%22projects%2Ftasuketsu2%2Fdatabases%2F(default)%22%2C%22removeTarget%22%3A4%7D"
payload_data3 = "headers=X-Goog-Api-Client%3Agl-js%2F%20fire%2F9.15.0%0D%0AContent-Type%3Atext%2Fplain%0D%0AX-Firebase-GMPID%3A1%3A978100370888%3Aweb%3A006bc5c6eb78ae899854fd%0D%0A&count=1&ofs=0&req0___data__=%7B%22database%22%3A%22projects%2Ftasuketsu2%2Fdatabases%2F(default)%22%7D"

def random_string_lowercase(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._run = self.run
        self.run = self.set_id_and_run

    def set_id_and_run(self):
        self.id = threading.get_native_id()
        self._run()

    def get_id(self):
        return self.id
        
    def raise_exception(self):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.get_id()), 
            ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.get_id()), 
                0
            )
            print('Failure in raising exception')

def update_output():
    random_int = str(random.randrange(10**4, 10**5))
    
    
    headers = {
        "Content-Length": str(len(payload_data.format(target_id))),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    gsessionid_response = session.post(
        get_gsessionid_url.format(random_int, random_string_lowercase(5)),
        data=payload_data.format(target_id), headers=headers
    )
    
    if "X-HTTP-Session-Id" not in gsessionid_response.headers:
        print("X-HTTP-Session-Id not found in headers.")
        print(gsessionid_response.headers)
        exit()
    
    get_gsessionid = gsessionid_response.headers["X-HTTP-Session-Id"]
    lines = gsessionid_response.text.splitlines()
    
    try:
        json_data = json.loads(lines[1])
        get_sid = json_data[0][1][1]
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        print(lines)
        exit()
       
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ja;q=0.9",
        "Priority": "u=0, i",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0 Config/100.2.9281.82"
    }
    
    add_url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)&gsessionid={get_gsessionid}&SID={get_sid}&RID={str(random.randrange(10**4, 10**5))}&AID=5&zx={random_string_lowercase(12)}&t=1"
    sa = requests.post(add_url,data=payload_data.format(target_id),headers=headers)
    
    add_url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel?VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)&gsessionid={get_gsessionid}&SID={get_sid}&RID={str(random.randrange(10**4, 10**5))}&AID=5&zx={random_string_lowercase(12)}&t=1"
    sa = requests.post(add_url,data=payload_data2,headers=headers)
    
    add_url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Write/channel?VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)&RID={str(random.randrange(10**4, 10**5))}&CVER=22&X-HTTP-Session-Id=gsessionid&zx={random_string_lowercase(12)}&t=1"
    sa = requests.post(add_url,data=payload_data3,headers=headers)
    
    get_gsessionid = sa.headers["X-HTTP-Session-Id"]
    lines = sa.text.splitlines()
    
    try:
        json_data = json.loads(lines[1])
        get_sid = json_data[0][1][1]
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        print(lines)
        exit()
    
    add_url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Write/channel?gsessionid={get_gsessionid}&VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)&RID=rpc&SID={get_sid}&CI=0&AID=0&TYPE=xmlhttp&zx={random_string_lowercase(12)}&t=1"

    def temp_request():
        time.sleep(0.1)
        session.get(
            url=add_url,
            headers=headers,
            timeout=1
        )
    
    temp_thread = CustomThread(target=temp_request)
    temp_thread.start()
    
    sa = requests.get(add_url,headers=headers, timeout=100)
    temp_thread.raise_exception()
    match = re.search(r'"streamToken":\s*"([^"]+)"', sa.text)
    if match:
        stream_token = match.group(1)
        payload_data4 = f"count=1&ofs=1&req0___data__=%7B%22streamToken%22%3A%22{stream_token}%22%2C%22writes%22%3A%5B%7B%22update%22%3A%7B%22name%22%3A%22projects%2Ftasuketsu2%2Fdatabases%2F(default)%2Fdocuments%2Fpublic%2F{target_id}%22%7D%2C%22updateMask%22%3A%7B%22fieldPaths%22%3A%5B%5D%7D%2C%22updateTransforms%22%3A%5B%7B%22fieldPath%22%3A%22%60{sent_target}%60%22%2C%22increment%22%3A%7B%22integerValue%22%3A%221%22%7D%7D%5D%2C%22currentDocument%22%3A%7B%22exists%22%3Atrue%7D%7D%5D%7D"
        add_url = f"https://firestore.googleapis.com/google.firestore.v1.Firestore/Write/channel?VER=8&database=projects%2Ftasuketsu2%2Fdatabases%2F(default)&gsessionid={get_gsessionid}&SID={get_sid}&RID={str(random.randrange(10**4, 10**5))}&AID=1&zx={random_string_lowercase(12)}&t=1"
        sa = requests.post(add_url,data=payload_data4,headers=headers)
        if sa.status_code == 200:
            print("[+] success vote")

zoukaryou = "1" # 増加量 
sent_target = "z-0_{}".format(zoukaryou)
target_id = "" # XeauSxIclNV7ZFXq9zgx など

with ThreadPoolExecutor(max_workers=10) as executor:
    while True:
        executor.submit(update_output)
        time.sleep(0.1)