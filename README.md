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
 
### N.B. Il progetto va preso come "proof of concept", da non utilizzare in ambienti di produzione.
