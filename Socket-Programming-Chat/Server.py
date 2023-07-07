
# Salih Kuloğlu 20010011061

import socket
import threading

connections = []
usernames = []
size = 2048
max_client = 2          # Sohbet odasına eklenebilecek max kullanıcı sayısı
HOST = '127.0.0.1'
PORT = 12345

def client_msg_yakala(connection: socket.socket, address: str):

    while True:
        username = connection.recv(size)                    # client'ın username girmesi bekleniyor
        if username in usernames:
            connection.send("Bu kullanıcı zaten kayıtlı".encode())      # username kayıtlıysa client'a response olarak gönderiliyor
            continue
        else:
            connection.send("username başarılı".encode())
            usernames.append(username)              # username'i usernames dizisine ekledik
            msg = "        ".encode() + username + " - Sohbete Katıldı ".encode()
            broadcast(msg.decode(), connection)         # mesajı yayınlamak için brodcast fonksiyonuna gönderdik
            break

    if(len(connections) > 1):
        connection.send("Odadaki Katılımcılara selam vermek istermisin ?".encode())
        res = connection.recv(size).decode()
        if(res == "evet"):
            otoMsg = connection.recv(size).decode()         # odada en az bir katılımcı varsa yeni client'a selam vermek istermisiniz sorduk
            broadcast(otoMsg,connection)                    # gelen cevap evet ise kullanıcı selamını yayınladık
    else:
        connection.send("Odada kimse yok".encode())


    while True:
        try:
            msg = connection.recv(size)   # client'ın mesaj girmesi bekleniyor
            if msg:

                msg = username + " - ".encode() + msg  # girilen mesajın önüne username bilgisi eklenerek yayınlama fonksiyonuna gönderildi
                broadcast(msg.decode(), connection)

            else:
                connection.close()                  # hatalı mesaj girilmesi durumunda bağlantıyı kapattık ve connections dizisinden sildik
                connections.remove(connection)
                break

        except Exception as e:
            msg ="        ".encode() + username + " - Sohbetten Ayrıldı".encode()  # client terminali kapatırsa sohbete ayrıldı mesajını yayınladık ve
            broadcast(msg.decode(), connection)                                   # bağlantısını kapatarak diziden sildik
            print(e)
            usernames.remove(username)
            connection.close()
            connections.remove(connection)
            break


def broadcast(message: str, connection: socket.socket):

    for client_conn in connections:                            # mesajı gönderen client haric bütün client'lara mesajı yayınladık
        if client_conn != connection:
            try:
                client_conn.send(message.encode())
            except Exception as e:
                print(e)                                       # mesaj göndermede sıkıntı olursa bağlantıyı kapattık ve diziden sildik
                client_conn.close()
                connections.remove(client_conn)


def server():


    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # soket nesnesi
        socket_instance.bind((HOST, PORT))                                   # server bağlantısı
        socket_instance.listen(max_client)                                   # client girişi bekleniyor

        print('Sunucu Çalışıyor...')


            #            Sohbet Odasına Katılabilecek Max kullanıcı Kontrolü


        while True:
            socket_connection, address = socket_instance.accept()       # client girişi yakalandığında
            if(len(connections) >= max_client):
                msg = "Üzgünüz. Bu sohbet odası " + str(max_client) + " adet kullanıcı ile sınırlandırılmıştır"
                socket_connection.send(msg.encode())       # max_client sayısına göre kontrol işlemi yapıldı ve giriş yapmak isteyen client'a bilgilendirme mesajı gönderildi
                socket_connection.close()
                print("Fazla bağlantı sayısı engellendi")
                continue
            socket_connection.send("Bağlantı Başarılı".encode())
            connections.append(socket_connection)
            print("Yeni Bağlantı Oluşturuldu... ")  # server ekranına bağlantı oluştu biligisini yazdırdık
            threading.Thread(target=client_msg_yakala, args=[socket_connection, address]).start() # client için mesaj dinleme threadi oluşturduk ve atadık

    except Exception as e:
        print(e)

server()
