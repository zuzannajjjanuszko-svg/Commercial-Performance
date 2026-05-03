import socket
# try the pooler host that worked in the populate script
try:
    ip = socket.gethostbyname("aws-0-eu-west-1.pooler.supabase.com")
    print("IP:", ip)
except Exception as e:
    print("Error:", e)