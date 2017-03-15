from __future__ import division

import time
import datetime

from robin.audio import Audio
from robin.config import ULTRAMICS, DAC, IP, DEVICE_ID
from robin.config_secret import BATCAVE_HOST
from robin.echolocate import simple_loop
from robin.gpio import (emitter_enable, emitter_battery_low, device_battery_low,
                        power_led)
from robin.pulse import default_pulse, pulse_from_dict

from robin.util import app_running, kill_app
from robin.batcave.client import run_client
from robin.batcave.protocol import Message, DeviceStatus
from robin.batcave.debug_override import DebugOverride

AUDIO = Audio(ULTRAMICS, DAC)

connected_remotes = 0
last_pulse_dict = None
pulse = default_pulse()


def handle_override(overrides):
    emitter_enable.set(overrides.force_enable_emitters)


def on_connected():
    print "we're connected!"


def on_disconnect():
    print "we're disconnected."


def on_remote_connect():
    global connected_remotes
    connected_remotes += 1


def on_remote_disconnect():
    global connected_remotes
    connected_remotes -= 1
    if connected_remotes == 0:
        handle_override(DebugOverride())


def on_update_overrides(overrides):
    handle_override(DebugOverride.from_dict(overrides))


def on_update_pulse(pulse_dict):
    global pulse, last_pulse_dict
    if pulse != last_pulse_dict:
        last_pulse_dict = pulse_dict
        pulse = pulse_from_dict(pulse_dict)


def on_trigger_pulse():
    simple_loop(pulse, AUDIO)


def get_device_status():
    return DeviceStatus.READY


def get_device_info():
    return {
        'id': DEVICE_ID,
        'ip': IP,
        'deviceVoltageLow': power_led.read(),
        'deviceBatteryLow': device_battery_low.read(),
        'emitterBatteryLow': emitter_battery_low.read(),
        'bluetoothConnections': "Unknown",
        'lastSeen': str(datetime.datetime.now()),
        'pulse': last_pulse_dict,
    }


def main():
    run_client(BATCAVE_HOST,
               get_device_status,
               get_device_info,
               {
                   Message.CONNECT: on_connected,
                   Message.RECONNECT: on_connected,
                   Message.DISCONNECT: on_disconnect,
                   Message.TRIGGER_PULSE: on_trigger_pulse,
                   Message.UPDATE_PULSE: on_update_pulse,
                   Message.UPDATE_OVERRIDES: on_update_overrides,
                   Message.DEVICE_REMOTE_CONNECT: on_remote_connect,
                   Message.DEVICE_REMOTE_DISCONNECT: on_remote_disconnect,
               },
               app_running)

try:
    main()
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    kill_app()
