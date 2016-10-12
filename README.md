# Consulidator
Simple, dockerized way to backup and restore your Consul datastore

## Backup:
```sh
CONSUL_ADDRESS=10.0.1.2
CONSUL_PORT=8500
BACKUP_FILE=my_backup

docker run djenriquez/consulidator \
--backup \
--port $CONSUL_PORT $CONSUL_ADDRESS > $BACKUP_FILE
```

## Restore:
```sh
CONSUL_ADDRESS=10.0.1.2
CONSUL_PORT=8500
BACKUP_FILE=my_backup

docker run djenriquez/consulidator \
-v `pwd`:/restore \
--restore $BACKUP_FILE \
--port $CONSUL_PORT $CONSUL_ADDRESS
```