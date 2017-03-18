# *domfind*

*domfind* is a Python 3.6.x utility that tests for the existence of domain names under different Top Level Domains (TLDs). This is achieved by making a series of DNS requests for Start of Authority (SOA) records starting at the root servers and working down through the parent domains until the last parent replies with a `SOA` section or a `NXDOMAIN` response code indicating the nonexistence of the input domain name. Local or public DNS resolvers are purposefully not used in order to avoid cached records. It should be noted that the number of DNS queries performed grows linearly with the depth of the input domain and the number of TLDs to check for. For instance, `sub1.sub2.domain` needs a total of three queries per TLD. The first one is directed at a root server, the second one goes to a SOA server of `domain.tld`, and the third, final one to `sub2.domain.tld`.

This utility is useful to find malicious subdomains registered under multiple TLDs that might be used for phishing campaigns. Malicious actors often use the same domain name for related or subsequent campaigns for hosting web servers, which can be proactively found with *domfind* as a one-off, if a domain name is known, and acted upon accordingly afterwards.

The main purpose of *domfind* is to serve as an intelligence tool for incident responders and security investigators alike. It can, nevertheless, be used for other, similar goals where domain names need finding.

# Dependencies and Usage

*domfind* requires only a few modules that are specified in `requirements.txt`.

The supported options are the following:

```
Usage: domfind [-h] [-b] [-d <file>] [-p <sec>] [-t <thread>] [-u] [-v ...] [<domain> ...]

Find identical domain names with SOA DNS records under different Top Level Domains (TLDs).

Options:
  -h, --help  show this help message and exit

  -b, --bad            use the known-bad TLD file at data/known-bad-tld.txt
  -d, --domain <file>  use the specified custom TLD file [default: data/tlds-alpha-by-domain.txt]
  -p, --pause <num>    wait an interval in seconds between each input domain [default: 0]
  -t, --thread <num>   specify the size of the thread pool [default: number of CPU cores]
  -u, --update         update the local TLD list from IANA and the root name servers from InterNIC
  -v, --verbose        display verbose and debug messages
```

# Examples

* Split the pre-compiled known-bad TLD list across two threads for checking one input domain name:

```
$ python3 domfind.py -b -t 2 domain
```

* Check two domain names across all TLDs listed by IANA, pause for 60 seconds between input domain names and be verbose:

```
$ python3 domfind.py -vp 60 sub2.sub1.domain1 sub.domain2
```

# Future Work

* Documentation;
* Improve DNS querying performance, namely by building a list with the SOA servers for all TLDs and by implementing a local cache;
* Improve DNS and general error handling;
* Compile a list of known-bad hosting providers that allow the creation of subdomains under their own domain names.

# Change History

* *domfind* **20170318**: first release.
