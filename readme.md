# Verteilter Statusserver
## Vor dem ersten Starten:
### Docker einrichten:
Sofern nicht bereits vorhanden, muss Docker installiert werden. Siehe https://docker.com

Wenn Docker eingerichtet und gestartet ist, muss ein neues Netzwerk in Docker eingerichtet werden, in dem das verteilte Statusserversystem laufen wird.

    docker network create tevs-network 

Das Netzwerk **muss** die Netzadresse 172.18.0.0/16 haben, andernfalls werden die Servernodes nicht starten (die erlaubten Adressen der Serverinstanzen sind im config.json File eingestellt). Überprüfen der Netzadresse:

    docker network inspect tevs-network

## Starten der Anwendung

Die beiden Dockerfiles (Server & Client) können von folgendem Link heruntergeladen werden:

Server:
https://fhburgenlandat-my.sharepoint.com/:u:/g/personal/2110859009_fh-burgenland_at/ERl0b9aMSz5BjM5fCFMsTVwBAmIrXLr_qGY2d32JFPls7Q?e=akwUMg

Client:
https://fhburgenlandat-my.sharepoint.com/:u:/g/personal/2110859009_fh-burgenland_at/EVoQeCBf-qVMq7auS6_uuSoBfMw8iW_zwrNAUiELWnkz_A?e=pM6Q8d

Nun erstellen wir das Serverimage. Dazu öffnen wir eine Konsole und navigieren zum Ort der zwei Dockerfiles. Nun führen wir folgenden Befehl aus:

    docker build --no-cache -t tevs_server_node -f Dockerfile_server .

Anschließend erstellen wir das Image für den Client:

    docker build --no-cache -t tevs_client_node -f Dockerfile_client .

Container mit dem Serverimage können folgendermaßen gestartet werden:

    docker run --network tevs-network --name Node1 tevs_server_node

Node1 gibt hier den Namen des Containers an, muss für weitere Server abgeändert werden. Wichtig ist, dass die Server im zuvor erstellten Netzwerk eingebunden werden, dafür der Parameter *--network tevs-network*

Sollte zumindest ein Server im Betrieb sein, kann ein Client mittels

    docker run -ti --network  tesv-network --name Client1 tevs_client_node

gestartet werden. *-ti* gibt hier an, dass der Container "attached" gestartet werden soll, sprich Eingaben können über das Terminal getätig werden. Auch hier ist darauf zu Achten, dass der Client im tevs-network eingebunden wird. 