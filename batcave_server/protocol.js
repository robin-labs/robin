const DeviceStatus = {
	// Device is disconnected
	DISCONNECTED: "disconnected",
	// We're not sure what the device is doing
	UNKNOWN: "unknown",
	// The device server is running but doing busywork
	BUSY: "busy",
	// The device won't work because there's a hardware problem
	// Maybe a mic is unplugged or the emitter battery is dead
	HARDWARE_UNAVAILABLE: "hardware-unavailable",
	// Ready to go!
	READY: "ready",
};

const RemoteStatus = {
	NO_SOCKET: "no-socket",
	DISCONNECTED: "disconnected",
	CONNECTED: "connected",
};

const DirectMessage = {
	DEVICE_STATUS: "device-status",
	SET_RECORD_DURATION: "set-record-duration",
	TRIGGER_PULSE: "trigger-pulse",
	UPDATE_OVERRIDES: "update-overrides",
	UPDATE_CONFIG: "update-config",
	RESTART_DEVICE: "restart-device",
	AUDIO: "audio",
	HANDSHAKE_REMOTE: "handshake-remote",
	HANDSHAKE_DEVICE: "handshake-device",
	DEVICE_LOG: "device-log",
}

const ServerMessage = {
	CONNECT: "connect",
	DISCONNECT: "disconnect",
	DEVICE_LISTING: "device-listing",
	CHOOSE_DEVICE: "choose-device",
	DEVICE_REMOTE_CONNECT: "device-remote-connect",
	DEVICE_REMOTE_DISCONNECT: "device-remote-disconnect",
	DEVICE_CHOICE_SUCCESSFUL: "device-choice-successful",
}

const Message = { ...DirectMessage, ...ServerMessage };

module.exports = { DeviceStatus, RemoteStatus, DirectMessage, ServerMessage, Message };