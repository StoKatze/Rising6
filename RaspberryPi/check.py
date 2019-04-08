# -*- coding: utf-8 -*-
import sys
import pymysql
import subprocess
import time

print("Fase 2: Verifica del codice inserito")
nome = "Err" #Variabile inizializzata ad errore. Se avra successo la query verra cambiata nel nome della persona
db = pymysql.connect("localhost","Accesso","BONO","campusArcesso") #Dati di accesso al DB e connessione
print("Connessione al Database")
cursor = db.cursor() #Specifica un cursore per la lettura dei dati
try:
	cursor.execute("SELECT nome FROM studenti WHERE pin = %s;", sys.argv[1]) #esegue la query
	res = cursor.fetchall() #Prende tutti i risultati
	print("Verifica effettuata\n")
	for row in res: #Per ogni riga prende il nome (dovrebbe essercene solo una)
		nome = row[0] 
		#print(nome) #Debug
except:
	nome = "Err" #Vuole qualcosa qui...
	#Se c'è un errore di esecuzione la variabile nome sarà err (come impostata prima). Sarà riconosciuta da arduino come errore
	#print(nome) #Debug
else:
	#print(nome) # Debug
	time.sleep(5)
	processo = subprocess.check_output(['python3', 'send.py', nome]) #Apre il programma che pubblica sul topic di risposta
	print(processo.decode("utf-8")) #Dovrebbe stampare l'output del processo

db.close() #Chiude la connessione al DB
sys.exit() #Termina l'esecuzione di questo script
