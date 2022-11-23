# Booking
## Connect by SSH
Use `key` provided by one of the devs. Move it to .ssh folder.

Set the lowest permission for it (**400** - read-only for owner):
```shell
chmod 400 ~/.ssh/key
```

To connect to the server use command below:
```shell
ssh -i ~/.ssh/key superemail003@34.27.180.91 -o StrictHostKeyChecking=no
```

To re-run containers use these commands on server:
```shell
cd booking-backend/
./run-docker-local.sh --build -d
```

To stop contaners use:
```shell
cd booking-backend/
./stop-docker-local.sh
```
