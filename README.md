# Consulidator
Simple, dockerized way to backup and restore your Consul datastore

## Backup:
```sh
CONSUL_ADDRESS=10.0.1.2
CONSUL_PORT=8500
BACKUP_FILE=my_backup

docker run --rm \
djenriquez/consulidator:v0.1.0 \
--backup \
--port $CONSUL_PORT $CONSUL_ADDRESS > $BACKUP_FILE
```

## Restore:
Assuming that you are running the restore in the working directory that contains `$BACKUP_FILE`
```sh
CONSUL_ADDRESS=10.0.1.2
CONSUL_PORT=8500
BACKUP_FILE=my_backup

docker run --rm \
-v `pwd`:/restore \
djenriquez/consulidator:v0.1.0 \
--restore $BACKUP_FILE \
--port $CONSUL_PORT $CONSUL_ADDRESS
```