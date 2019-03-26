# -*- coding: utf-8 -*-
import sys
import pymysql
import subprocess
import time

print("Fase 2: Verifica del codice inserito")
nome = "Err" #Variabile inizializzata ad errore. Se avra successo la query verra cambiata nel nome della persona
db = pymysql.connect("localhost","Accesso","BONO","campusArcesso") #Dati di accesso al DB e connessione
print("Connessione al Database")
cursor = db.cursor() #Specifica un cursore per la lettura e la scrittura dei dati

try:
	cursor.execute("SELECT nome FROM studenti WHERE pin ='" + sys.argv[1] + "';") #Esegue la query
	res = cursor.fetchall() #Prende tutti i risultati
	print("Verifica effettuata\n")
	if cursor.rowcount > 0: #Controlla se sono stati prodotti risultati
		for row in res: #Per ogni riga prende il nome (dovrebbe essercene solo una)
			nome = row[0]
			#print(nome) #Debug
		cursor.execute("UPDATE studenti SET ultimoAccesso=current_timestamp WHERE pin='" + sys.argv[1] + "';") #Aggiorna l'ultimo login
		#print("Debuggg") #Debug
		db.commit() #Applica i cambiamenti al DB
	else: #Altrimenti lascia il nome come "Err"
		nome = "Err"
except:
	nome = "Err" #Vuole qualcosa qui...
	#Se c'è un errore di esecuzione la variabile nome sarà err (come impostata prima). Sarà riconosciuta da arduino come errore
	#print(nome) #Debug
else:
	#print(nome) # Debug
	time.sleep(0.5)
	processo = subprocess.check_output(['python3', 'send.py', nome]) #Apre il programma che pubblica sul topic di risposta
	print(processo.decode("utf-8")) #Dovrebbe stampare l'output del processo

db.close() #Chiude la connessione al DB
sys.exit() #Termina l'esecuzione di questo script