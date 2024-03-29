import socketio
import threading
import time
from typing import TYPE_CHECKING

from .protocol import Message
from robin.logger import log

sio = None

if TYPE_CHECKING:
    from robin.config import Config


def send_to_batcave_remote(*args, **kwargs):
    if sio and sio.connected:
        sio.emit(*args, **kwargs)


def client(config: "Config", get_device_status, get_device_info, callbacks):
    global sio
    connected = False
    attempts = 0
    sio = socketio.Client(reconnection=True)

    batcave_host = (
        "http://0.0.0.0:8000"
        if config.current.batcave.self_host
        else config.current.batcave.host
    )

    if not batcave_host:
        return

    log(f"Connecting to Batcave server at {batcave_host}")

    for event, handler in callbacks.items():
        sio.on(event, handler)

    def try_connect():
        nonlocal attempts, connected
        attempts = 0
        while not connected:
            try:
                time.sleep(max(5, min(2 ** (attempts // 4), 120)))
                sio.connect(batcave_host)
                connected = True
                run_connection()
            except Exception as ex:  # noqa: F841
                attempts += 1

    def run_connection():
        nonlocal connected
        log("Connected to Batcave server.", connected)
        sio.emit(Message.HANDSHAKE_DEVICE, get_device_info())
        while connected:
            device_status = get_device_status()
            device_info = get_device_info()
            send_to_batcave_remote(
                Message.DEVICE_STATUS,
                {
                    "status": device_status,
                    "info": device_info,
                    "config": config.current.model_dump(),
                },
            )
            sio.sleep(5)

    @sio.event
    def disconnect():
        nonlocal connected
        connected = False
        log("Disconnected from Batcave server.")
        try_connect()

    try_connect()


def run_batcave_client(*args):
    client_thread = threading.Thread(target=client, args=args, daemon=True)
    client_thread.start()
