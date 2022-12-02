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

Firstly, open project directory
```
cd booking-backend
```

To re-run containers use this command on server:
```shell
make run
```

To stop containers:
```shell
make stop
```

To show logs:
```shell
make logs
```

To show logs for specific service:
```shell
make logs service=<service_name>
```
