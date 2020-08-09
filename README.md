# Snapcast stream switch
[Snapcast][1] stream switch is a controller for auto stream select.

If some of the streams changes its status to "playing", controller sets this stream for all of the groups.

If some of the streams changes its status to "idle", controller sets the streams with the highest priority from a streams with status "playing" for all of the groups. If there are no streams with status "playing" then nothing will be changed.

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

## Configuration
The controller configuration is done in `snapcontrol.conf`

Snapserver host and port configured in the `snapcast` section

Streams priority configured in the `streams_priority` section, default priority is 0.

The controller will not set stream from `disabled_streams` section when it becomes 'playing'. In spite of this section, streams still may be enabled if it 'playing' and other streams 'idle'.

**NOTE:** All stream names in configuration file are _case insensitive_


[1]: https://github.com/badaix/snapcast