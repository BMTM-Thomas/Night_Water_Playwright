import socket
import dns.resolver
import requests
import ssl
import datetime
from datetime import datetime
import OpenSSL
import re
import time

# Clean Column
# Row - , Column |
# for row in ws['B2:F500']:
#   for cell in row:
#     cell.value = None

# # Save Excel
# wb.save("urls.xlsx")

# Check Cname Record
def Cname_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        for answer in answers:
            print(f"CNAME record: {answer}")

            jh03 = dns.resolver.resolve(str(answer), 'CNAME')
            for answer in jh03:
                print(f"CNAME record: {answer}")
    except:
        pass
    # except dns.resolver.NXDOMAIN:
    #     print(f"The domain {domain} does not exist")

# Check A Record
def A_record(domain):
    try:
        addresses = socket.getaddrinfo(domain, None, socket.AF_INET)
        unique_addresses = set()  # Store unique addresses
        for addr in addresses:
            unique_addresses.add(addr[4][0])  
        for unique_addr in unique_addresses:
            print(f"A record:     {unique_addr}")

        return(unique_addr)
       
    # except socket.gaierror as e:
    #     print(f"Error occurred: {e}")
    except:
        print("解析错误!!!")

# Check URL Status Code
def URL_Status_Code(url):
    try:
        response = requests.head(url)
        status_code = response.status_code
        print(f"Status code:  {status_code}")
        return status_code
    except:
        print(f"Status code:  400 Bad Request")
    # except:
    #     print("解析错误!!!")

# SSL Certificate
def SSL_Cert(domain):
    try:
        cert=ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        bytes=x509.get_notAfter()
        bytes2=x509.get_notBefore()
        issued = bytes.decode('utf-8')
        expired = bytes2.decode('utf-8')
        print ("Issued on:    " + datetime.strptime(issued, '%Y%m%d%H%M%S%z').date().isoformat())
        print ("Expired on:   " + datetime.strptime(expired, '%Y%m%d%H%M%S%z').date().isoformat())
    except:
        pass

# Make Word Bold
def make_bold(word):
    return f"\033[1m{word}\033[0m"

with open('url.txt', 'r') as f:
    url = f.read()

url = url.split()

X = 0
e = 2
f = 2
for item in url:
    # URL Address
    print("\n" + "[" + make_bold(url[X]) + "]")
    domain_name = url[X]
    # Cname Records
    Cname_record(domain_name)
    # A Records
    A = A_record(domain_name)
    # SSL Certification Date
    SSL_Cert(domain_name)
    # URL Status Code 200 or 400
    status = URL_Status_Code("https://"+domain_name)

    # 用来匹配dig 出来的ip address
    try:
        A = re.match(r'^(\d+\.\d+\.\d+)', A).group(1)
    except:
        pass
    
    # Write into Excel
    # B F J N R
    # 解析正确
    if status == 200 and A == "103.24.53" or A == "103.188.120" or A == "103.188.121":
        e += 1
    # 解析正确，但没绑定到
    elif status != 200 and A == "103.24.53" or A == "103.188.120" or A == "103.188.121":
        e += 1
    else:
    # 解析不正确
    # D H L P T
        f += 1

    X += 1


X = 0
for item in url:
    # URL Address
    domain_name = url[X]
    print(domain_name)
    X += 1

print('\n\n\n\n\n')

