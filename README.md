# Snapcast stream switch
[Snapcast][1] stream switch is a controller for auto stream select.

If some of the streams changes its status to "playing", controller sets this stream for all of the groups.

If some of the streams changes its status to "idle", controller sets one of the streams with status "playing" for all of the groups. If there is no streams with status "playing" then nothing will be changed.

## Install
The controller must be installed on the device where Snapcast is installed.

```shell script
git clone https://github.com/d-xtich/snapcast_stream_switch.git
cd snapcast_stream_switch
./install.sh
```

## Uninstall
```shell script
cd snapcast_stream_switch
./uninstall.sh
```

## Start/Stop
```shell script
systemctl start snapcontrol.service
systemctl stop snapcontrol.service
```

## TODO

- [X] Add configuration file with snapcast host/port
- [X] Add priority to the streams
- [ ] Add auto switch blacklist

[1]: https://github.com/badaix/snapcast