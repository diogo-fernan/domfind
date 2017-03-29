#!/usr/bin/env python3

"""
Usage: domfind [-h] [-p <sec>] [-r] [-t <thread>] [-u] [-v ...]
               [-b | -d <file>] 
               [<domain> ...]

Find identical domain names with SOA DNS records under different Top Level Domains (TLDs).

Options:
  -h, --help  show this help message and exit

  -b, --bad            use the known-bad TLD file at data/known-bad-tld.txt
  -d, --domain <file>  use the specified custom TLD file [default: data/tlds-alpha-by-domain.txt]
  -p, --pause <num>    wait an interval in seconds between each input domain [default: 0]
  -r, --raw            output raw hits (just the domain names)
  -t, --thread <num>   specify the size of the thread pool [default: number of CPU cores]
  -u, --update         update the local TLD list from IANA and the root name servers from InterNIC
  -v, --verbose        display verbose and debug messages

IANA online TLD list: https://data.iana.org/TLD/tlds-alpha-by-domain.txt
InterNIC online DNS root list: http://www.internic.net/domain/named.root

Examples:
  - Split the known-bad TLD list across two threads for checking the input 
    domain name:
$ python3 domfind.py -b -t 2 domain

  - Check two domain names across all TLDs listed by IANA, pause for 60 seconds
    between input domain names and be verbose:
$ python3 domfind.py -vp 60 sub2.sub1.domain1 sub.domain2

Copyright (c) 2017 Diogo Fernandes
https://github.com/diogo-fern/domfind
"""

from docopt import docopt, printable_usage

from domfind.core import main

exit(main.run(docopt(__doc__), printable_usage(__doc__)))


# wget -q -O - https://data.iana.org/TLD/tlds-alpha-by-domain.txt | tail -n +2 | \
# sed "s/^[0-9a-z]*-*[0-9a-z]*$/'\.&',/" | \
# awk 'BEGIN { FS="\n"; RS=""} \
# { for (i=1; i<=NF; i=i+3) printf "%30s %30s %30s\n", $i, $(i+1), $(i+2) }'
