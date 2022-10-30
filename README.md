# Booking
## Connect by SSH
Use `backend_server_key.pem` provided by one of the devs.

Set the lowest permission for it (**400** - read-only for owner):
```shell
chmod 400 backend_server_key.pem
```

To connect to the server use command below:
```shell
ssh -i backend_server_key.pem ubuntu@ec2-52-89-122-142.us-west-2.compute.amazonaws.com
```

### Caution!
Do not stop the ec2 instance, only reboot, otherwise hostname will be changed.
