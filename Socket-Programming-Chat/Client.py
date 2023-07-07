
# Salih Kuloğlu 20010011061

import socket
import threading

size = 2048
HOST = '127.0.0.1'
PORT = 12345

def msg_yakala(connection: socket.socket):                  #  Sunucudan gelen mesajları yakalamak için

    while True:
        try:
            msg = connection.recv(size)                     # soketten gelecek mesajı bekler
            if msg:
                print(msg.decode())
            else:
                print("Hatalı bir mesaj gönderdiniz")
                connection.close()                          # mesaj içeriğinde bir hata olursa soketi kapatır
                break

        except Exception as e:
            print(e)
            connection.close()                              # mesaj yakalama işleminde bir hata olursa soketi kapatır
            break


def client():

    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   # soket nesnesi oluşturduk
        socket_instance.connect((HOST, PORT))               # server ile olan porta bağlandık
        response = socket_instance.recv(size).decode()
        if(response != "Bağlantı Başarılı"):                # Sohbet Odası dolu ise socket'i kapattık ve bilgilendirmeyi ekrana yazdırdık
            print(response)
            socket_instance.close()
            return
        while True:
            name = input("\nKullanıcı Adı Girin : ")
            socket_instance.send(name.encode())
            response = socket_instance.recv(size).decode()  # girilen kullanıcı adını servera gönderdik

            if(response == "Bu kullanıcı zaten kayıtlı"):   # kullanıcı adı kayıtlıysa döngüyü başa döndürdük
                print(response)
                continue
            break


        print('Sohbete bağlandınız!')
        print('Hoşgeldiniz\n')

        otoMsg = socket_instance.recv(size).decode()
        if(otoMsg != "Odada kimse yok"):                # odada en az bir katılımcı varsa client'a selam vermek istermisiniz sorduk
            print(otoMsg)
            while True:
                print("evet / hayır")
                cevap = input()                        # girilen cevaba göre server'a cevabı gönderdik
                if(cevap == "evet"):
                    socket_instance.send("evet".encode())
                    msg = "Merhaba, benim adım " + name + ". Sohbet odasına yeni katıldım"
                    socket_instance.send(msg.encode())
                    print(msg)
                    break
                elif(cevap == "hayır"):
                    socket_instance.send("hayır".encode())
                    break
                else:
                    print("Hatalı seçim yaptınız")
                    continue

        threading.Thread(target=msg_yakala, args=[socket_instance]).start()  # kayıt yapılan client'a serverdan gelen mesajları dinlemek için thread atadık
        while True:
            msg = input()
            socket_instance.send(msg.encode())                               # kullanıcının girdiği mesajları server'a gönderdik
    except Exception as e:
        print("client fonksiyonu")
        print(e)
        socket_instance.close()                  # client oluşturmada bir hata olşursa ekrana yazdırıp soketi kapattık

client()
