package sdk

const (
	PROPERTY_PROXY_ID                     = "__proxy_id"
	PROPERTY_PROXY_ENTRY                  = "__proxy_entry"
	PROPERTY_PROXY_CONSTRUCTOR            = "__proxy_constructor"
	PROPERTY_PROXY_PEER                   = "__proxy_peer"
	PROPERTY_PROXY_PROPERTIES             = "__proxy_props"
	PROPERTY_PROXY_ONEWAY_METHODS         = "__proxy_oneway_methods"
	PROPERTY_JSON_COPY_SERIALIZE_CHILDREN = "__json_copy_serialize_children"

	RPC_RESULT_ERROR_NAME = "RPCResultError"
)

type LocalProxiedEntry struct {
	id          string
	finalizerID string
}

type RPCProxy struct {
	dict map[string]interface{}
}

func NewRPCProxy(peer *RPCPeer, entry *LocalProxiedEntry, proxyConstructorName string, proxyProps interface{}, proxyOneWayMethods []string) *RPCProxy {
	return &RPCProxy{
		dict: map[string]interface{}{
			PROPERTY_PROXY_ID:             entry.id,
			PROPERTY_PROXY_ENTRY:          entry,
			PROPERTY_PROXY_CONSTRUCTOR:    proxyConstructorName,
			PROPERTY_PROXY_PEER:           peer,
			PROPERTY_PROXY_PROPERTIES:     proxyProps,
			PROPERTY_PROXY_ONEWAY_METHODS: proxyOneWayMethods,
		},
	}
}

type RPCPeer struct {
}
