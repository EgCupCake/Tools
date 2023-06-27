import requests
import threading
import pyfiglet

author=pyfiglet.figlet_format("EG CUPCAKE")

print(author)
x = input("Which Domain address would you like to request?")
dosya_adi = input("With which Wordlist do you want to guess the subdomain?")
verbose = input("How many requests should be made at once?")
error = 0
timeout = 0
semaphore = threading.BoundedSemaphore(value=int(verbose))

def make_request(payload):
    global error, timeout  
    fullreq = "https://" + payload + "." + x
    try:
        resp = requests.get(fullreq, timeout=15)  
        print(payload, "=Subdomain", resp.status_code, "=Response")
    except requests.exceptions.Timeout:
        timeout += 1  
    except requests.exceptions.RequestException:
        error += 1  
    finally:
        semaphore.release()

try:
    with open(dosya_adi, 'r') as dosya:
        wordlist = dosya.readlines()

        threads = []
        for value in wordlist:
            payload = value.strip()
            semaphore.acquire()
            thread = threading.Thread(target=make_request, args=(payload,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

except FileNotFoundError:
    print("The specified file could not be found.")
    
print("Total", error, "Error encountered")
print("Total", timeout, "Timeout  Encountered")
