BOOTSTRAP_SERVERS = ("b-3-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com:9196,"
                     "b-1-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com:9196,"
                     "b-2-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com:9196")
AUTO_OFFSET_RESET = "earliest"
SECURITY_PROTOCOL = "SASL_SSL"
SASL_MECHANISMS = "SCRAM-SHA-512"

MSG_TYPE = "msg_type"
K8SGPT_TYPE = "k8sgpt"

SECRETS_FILE = ".env"

PORT_API_URL = 'https://api.getport.io/v1'

WORKLOAD_BLUEPRINT_ID = 'workload'

K8SGPT_URL = "http://localhost:8080/v1/analyze"
BACKEND_LLM = "ollama"

UNWANTED_TEXT = ["Kubernetes error message with delimiters written in ",
                 "Provide the most possible solution in a step-by-step style, as follows:"]
