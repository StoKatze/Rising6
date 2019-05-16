# Controllo accessi - Rising6
### Progetto di Alternanza Scuola-Lavoro 

## Descrizione
Abbiamo pensato ad un sistema di controllo accessi per un edificio scolastico: ad ogni entrata/uscita occorre passare il proprio tag RFID ed il proprio PIN. Il sistema registrerà gli ultimi accessi e consentirà (o meno) l'accesso o l'uscita.

## Componenti
Il sistema comprende un microcontrollore Arduino ed un server su un Raspberry. La comunicazione tra i due avviene tramite Mosquitto (MQTT).
##### Al microcontrollore sono collegati:
* Tastierino alfanumerico per inserimento PIN
* Ricevitore RFID/NFC
* Schermo per mostrare informazioni

##### Sul Raspberry sono installati:
* Broker MQTT
* MariaDB
* Python3 
* Libreria Python paho-mqtt
* Expect (per unbuffer): ```apt-get install expect ```
## Funzionamento
##### N. B. Arduino e Raspberry Pi si devono collegare alla stessa rete e devono avere (possibilmente) IP statici. Testato con Python 3
Prima di iniziare viene caricato il programma [sketck_oracle_v3.ino](Arduino/sketck_oracle_v3.ino) aggiornato con l'ip del Raspberry Pi sul microcontrollore Arduino, che viene acceso.
Viene eseguito lo script [sub.py](RaspberryPi/sub.py) che si iscrive al topic "code" e rimane in attesa di nuovi messaggi.
Alla ricezione di un messaggio verrà creato un sottoprocesso che eseguirà lo script [check.py](RaspberryPi/check.py).
[Check.py](RaspberryPi/check.py) si collegherà al DB MySQL ottenendo il nome della persona a cui è associato il PIN da verificare. Se non dovesse essere restituito alcun risultato sarà utilizzata una stringa ("Err") che indica un errore. [Check.py](RaspberryPi/check.py) provvederà ad avviare lo script [send.py](RaspberryPi/send.py).
[Send.py](RaspberryPi/send.py) invierà il nome ottenuto da [Check.py](RaspberryPi/check.py) nel topic "answer". Arduino Stamperà il nome ricevuto e farà illuminare di verde il LED. Se il nome ricevuto dovesse essere "Err", il led lampeggerà di rosso e sul display verrà stampato un messaggio di codice errato.

L'output di questi script viene salvato nel file ACS.log

## Portale Web
##### N. B. Occorre avere un webserver con il modulo PHP installato ed abilitato. Testato con PHP 7.2.
Il form della pagina [index.html](Web/index.html) chiamerà lo script php [actionAdd.php](Web/actionAdd.php) che provvederà ad aggiungere un nuovo utente nel DB.
##### ATTENZIONE: lo script non effettua la verifica di eventuali duplicati (non avevamo tempo per implementarlo).

## Database
##### N. B. L'utente qui seguente ha solo permessi di eliminazione, aggiunta e selezione righe. Il DB non è accessibile dall'esterno.
##### E sinceramente cambierei username e password di questo utente se si vuol fare qualcosa di serio.
* Nome DB: campusArcesso
* Utente: accesso
* Password: BONO
* Nome tabella: studenti

#### Campi tabella studenti:
* id - Auto increment primary key
* matricola - Matricola dello studente
* nome - Nome dello studente
* cognome - Cognome dello studente
* pin - Pin dello studente
* rfid - MAC Address del tag NFC utilizzato per l'accesso
* ultimoAccesso - Timestamp ultimo accesso

## Comandi esecuzione
Non dovrebbe essere necessario utilizzare nessuno di questi comandi in quanto lo script [autostart.sh](autostart.sh) viene eseguito automaticamente all'avvio mediante CRON.

#### Esecuzione diretta python
```shell
cd Desktop/
python3 sub.py
```
#### Esecuzione diretta python con LOG
```shell
cd Desktop/
unbuffer python3 sub.py 2>&1|tee -a ACS.log
```
#### Esecuzione mediante autostart
```shell
./autostart.sh
```

### Argomenti a riga di comando
Solo gli script [check.py](RaspberryPi/check.py) e [send.py](RaspberryPi/send.py) necessitano argomenti aggiuntivi.
Esempio
```shell
python3 check.py PIN
```
```shell
python3 send.py NOME
```
Dove al posto di PIN occorre inserire il PIN da verificare e al posto di NOME il nome dello studente da mostrare sul display collegato ad Arduino.

## [Video presentazione progetto finale](https://youtu.be/YnGyfyH0EmU)

## [Il Fermi nel percorso di ASL di Oracle Italia](https://www.itisfermi.edu.it/event/il-fermi-nel-percorso-di-asl-di-oracle-italia/)

### N.B. Il progetto va preso come "proof of concept", da non utilizzare in ambienti di produzione.
