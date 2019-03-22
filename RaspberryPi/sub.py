# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import subprocess

def on_connect(client, userdata, flags, rc):  # Funzione di connessione ad MQTT
	if(format(str(rc)) == "0"): # Verifica la connessione
		print("Connesso.")
	else:
		print("Errore di connessione {0}".format(str(rc)))
	client.subscribe("code")  # Si iscrive al topic "code"

def on_message(client, userdata, msg):  # Funzione eseguita alla ricezione di un messaggio.
    msg.payload = msg.payload.decode("utf-8")
    print("Ricevuto -> " + str(msg.payload) + "\n")  # Stampa il messaggio ricevuto
    processo = subprocess.check_output(['python3', 'check.py', msg.payload.rstrip("\n")]) #Avvia la verifica
    print(processo.decode("utf-8")) # Stampa l'output del sottoprocesso

print("----- Sistema di verifica accessi -----")
print("\nFase 1: Ricezione del codice inserito")
client = mqtt.Client("test")  # Crea un'istanza del client mqtt
client.on_connect = on_connect  # Imposta la chiamata della funzione di connessione a seguito di un tentativo di collegamento
client.on_message = on_message  # Imposta la chiamata della funzione on_message a seguito della ricezione di un messaggio
client.connect('127.0.0.1', 1883) # Prova a collegarsi
client.loop_forever()  # Rimane in listening

