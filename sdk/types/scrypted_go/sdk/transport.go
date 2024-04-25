package sdk

import (
	"encoding/binary"
	"fmt"
	"io"
	"os"
)

type RPCTransport interface {
	Prepare() error
	Read() (byte, []byte, error)
	Write([]byte) error
	Close() error
}

type RPCStreamTransport struct {
	read  io.ReadCloser
	write io.WriteCloser
}

func NewRPCStreamTransport(read io.ReadCloser, write io.WriteCloser) *RPCStreamTransport {
	return &RPCStreamTransport{
		read:  read,
		write: write,
	}
}

func (t *RPCStreamTransport) Prepare() error {
	return nil
}

func (t *RPCStreamTransport) Read() (_type byte, data []byte, err error) {
	lengthBytes := make([]byte, 4)
	typeBytes := make([]byte, 1)

	_, err = io.ReadFull(t.read, lengthBytes)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read message length: %w", err)
	}

	_, err = io.ReadFull(t.read, typeBytes)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read message type: %w", err)
	}

	_type = typeBytes[0]
	length := binary.BigEndian.Uint32(lengthBytes)

	data = make([]byte, length-1)
	_, err = io.ReadFull(t.read, data)
	if err != nil {
		return 0, nil, fmt.Errorf("failed to read message data: %w", err)
	}

	return _type, data, nil
}

func (t *RPCStreamTransport) Write(data []byte) error {
	_, err := t.write.Write(data)
	return err
}

func (t *RPCStreamTransport) Close() error {
	t.read.Close()
	t.write.Close()
	return nil
}

type RPCFileTransport struct {
	RPCStreamTransport
}

func NewRPCFileTransport(readFD int, writeFD int) (*RPCFileTransport, error) {
	read := os.NewFile(uintptr(readFD), "read")
	if read == nil {
		return nil, fmt.Errorf("invalid read file descriptor %d", readFD)
	}

	write := os.NewFile(uintptr(writeFD), "write")
	if write == nil {
		return nil, fmt.Errorf("invalid write file descriptor %d", writeFD)
	}

	return &RPCFileTransport{
		RPCStreamTransport: *NewRPCStreamTransport(read, write),
	}, nil
}
