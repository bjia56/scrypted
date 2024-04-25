package sdk

type DeviceState struct {
	// This map contains all the internal properties of the device.
	// Since the public SDK interface may change, this map allows us
	// to accept new properties dynamically.
	X__scrypted_data map[string]interface{} `json:"-"`
}
