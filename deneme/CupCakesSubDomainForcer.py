import requests
import threading
import pyfiglet

author=pyfiglet.figlet_format("EG CUPCAKE")

print(author)
x = input("Hangi Domain adresine istekte bulunmak istersiniz?")
dosya_adi = input("Hangi Wordlist ile subdomain tahmininde bulunmak istiyorsunuz?")
verbose = input("Aynı anda kaç istek yapılmalı?")
error = 0
timeout = 0
semaphore = threading.BoundedSemaphore(value=int(verbose))

def make_request(payload):
    global error, timeout  
    fullreq = "https://" + payload + "." + x
    try:
        resp = requests.get(fullreq, timeout=15)  
        print(payload, "SubDomainine yapılan istek", resp.status_code, "yanıtı almıştır")
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
    print("Belirtilen dosya bulunamadı.")
    
print("Toplamda", error, "tane hatayla karşılaşıldı")
print("Toplamda", timeout, "tane zaman aşımıyla karşılaşıldı")
