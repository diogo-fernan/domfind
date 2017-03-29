from traceback import format_exc

import dns
import dns.name
import dns.resolver

from domfind.common import color, out

# A.ROOT-SERVERS.NET.      3600000      A     198.41.0.4
ROOT_A = "198.41.0.4"


class DNSException(Exception):
    def __init__(self, dom, msg):
        self.msg = f"{dom} -- DNS {msg} error"
        super(DNSException, self).__init__(self.msg)


# http://stackoverflow.com/questions/4066614/how-can-i-find-the-authoritative-dns-server-for-a-domain-using-dnspython
def __authns(dom, raw=False):
    depth = 2
    ns = ROOT_A
    timeout = 16
    dom = dns.name.from_text(dom)

    last = False
    while not last:
        d = dom.split(depth)

        last = d[0].to_unicode() == u"@"
        subdom = d[1]

        out.debug(f"\"{subdom}\" NS query to {ns}")
        query = dns.message.make_query(subdom, dns.rdatatype.NS)
        try:
            resp = dns.query.udp(query, ns, timeout=timeout)
        except dns.exception.Timeout:
            raise DNSException(subdom, "query timeout") from None

        rcode = resp.rcode()
        out.debug(
            f"\"{subdom}\" NS response {dns.rcode.to_text(rcode)} from {ns}")
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                out.verb(f"\"{subdom}\" does not exist")
                return 0
            else:
                raise DNSException(subdom, "unknown")

        if len(resp.authority) > 0:
            rrset = resp.authority
        elif len(resp.additional) > 0:
            rrset = resp.additional
        else:
            rrset = resp.answer

        prevns = ns
        for rr in rrset:
            flag = False
            for entry in rr:
                if entry.rdtype == dns.rdatatype.SOA:
                    out.debug(f"\"{subdom}\" SOA on {ns}")
                    flag = True
                    break
                elif entry.rdtype == dns.rdatatype.A:
                    ns = entry.items[0].address
                    flag = True
                    break
                elif entry.rdtype == dns.rdatatype.NS:
                    authority = entry.target

                    if len(resp.additional) > 0:
                        for i in resp.additional:
                            if i.rdtype == dns.rdatatype.A:
                                ns = i.items[0].address
                                flag = True
                                break
                    if not flag:
                        out.debug(f"\"{authority}\" NS query to {prevns}")
                        query = dns.message.make_query(authority,
                                                       dns.rdatatype.A)
                        try:
                            resp = dns.query.udp(query, prevns, timeout=timeout)
                        except dns.exception.Timeout:
                            raise DNSException(subdom, "timeout") from None
                        out.debug(f"\"{authority}\" NS response"
                                  f" {dns.rcode.to_text(resp.rcode())} from {prevns}")
                        for i in resp.additional:
                            if i.rdtype == dns.rdatatype.A:
                                ns = i.items[0].address
                                break
                        flag = True
                    break
                else:
                    # IPv6, ...
                    pass
            if flag:
                break

        depth += 1

    if raw:
        print(subdom)
    else:
        out.info(f"SOA hit for \"{subdom}\"\n{rr}")
    return 1


def query(dom, tld, raw=False):
    n = 0
    for t in tld:
        try:
            n += __authns(dom + "." + t, raw)
        except DNSException as e:
            out.warn(f"DNS error: {e}\n{color.red(format_exc())}")
    return n


def parseroot():
    pass
