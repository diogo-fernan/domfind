from os.path import sep as SEP

DOMFIND_NAME = "domfind"
DOMFIND_VERSION = "v1.0"
DOMFIND_URL = "https://github.com/diogo-fernan/domfind"

DATA_PATH = "data" + SEP

IANA_TLD_FILE = "tlds-alpha-by-domain.txt"
IANA_TLD_URL = "https://data.iana.org/TLD/" + IANA_TLD_FILE
IANA_TLD_PATH = DATA_PATH + IANA_TLD_FILE

INTERNIC_ROOT_FILE = "named.root"
INTERNIC_ROOT_URL = "http://www.internic.net/domain/" + INTERNIC_ROOT_FILE
INTERNIC_ROOT_PATH = DATA_PATH + INTERNIC_ROOT_FILE

BAD_TLD_FILE = "known-bad-tld.txt"
BAD_TLD_PATH = DATA_PATH + BAD_TLD_FILE
