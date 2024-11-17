#!/bin/bash

# start_app.sh

# Avvia i container Docker
echo "Avvio dei container Docker..."
docker-compose up --build -d

# Attendi che i container si avviino
echo "Attesa di 10 secondi per l'avvio dei container..."
sleep 10

# Verifica lo stato dei container
echo "Stato dei container Docker:"
docker-compose ps

# Mostra i log del backend
echo "Log del container backend:"
docker-compose logs backend

# Apri l'applicazione frontend nel browser (solo per macOS e Linux)
if which xdg-open > /dev/null
then
  xdg-open http://localhost:3000
elif which open > /dev/null
then
  open http://localhost:3000
else
  echo "Apri manualmente il browser all'indirizzo http://localhost:3000"
fi

