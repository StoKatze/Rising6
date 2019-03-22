# -*- coding: utf-8 -*-
import sys
import paho.mqtt.client as mqtt

print("Fase 3: Invio dell'esito della verifica")
nome = sys.argv[1] #Prende il nome dalla command line
#print(nome) #Debug
client = mqtt.Client() #Istanzia un nuovo client
client.connect("localhost",1883,60) #Si collega ad MQTT
print("Inviato")
client.publish("answer", nome) #Pubblica sul topic answer il nome dell'utente
client.disconnect() #Si disconnette de MQTT
print("Verifica terminata. Ritorno nella fase di attesa\n\n")
sys.exit() #Termina lo script
