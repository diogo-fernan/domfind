from traceback import format_exc

from domfind.common import out, rw, util
from domfind.core import dns, meta, tldroot, work

ina = []
pause = 0
tldf = meta.IANA_TLD_PATH
thread = work.DEFAULT


def run(arg, usage):
    def inarg():
        global ina, pause, tldf, thread
        if not arg["--update"] and not arg["<domain>"]:
            print(usage)
            exit(0)

        try:
            pause = int(arg["--pause"])
            if int(pause) < 0:
                pause = 0
        except ValueError:
            out.warn(f"invalid pause interval integer value \"{pause}\", "
                     f"defaulting to zero")

        if not arg["--thread"] == work.DEFAULT:
            try:
                thread = int(arg["--thread"])
                if int(thread) < 0:
                    raise ValueError
            except ValueError:
                out.warn(f"invalid thread integer value \"{thread}\", "
                         f"defaulting to {work.THREAD}")
                thread = work.THREAD
            work.THREAD = thread

        if arg["--bad"]:
            tldf = rw.readf(meta.BAD_TLD_PATH, mode='r')
        elif arg["--domain"]:
            tldf = rw.readf(arg["--domain"], mode='r')
        ina = arg["<domain>"]

    if arg["--verbose"] == 1:
        out.LEVEL = out.log.verb
    elif arg["--verbose"] > 1:
        out.LEVEL = out.log.debug
    out.debug("arg", obj=arg)

    inarg()

    from time import sleep, time

    if arg["--update"]:
        tldroot.update()
    else:
        tld = util.shuffle([d.strip().lower()
                            for d in tldf if
                            not d.strip().startswith('#')])
        # dns.parseroot()

        for i, j in enumerate(ina):
            start = time()

            summ = work.exec(j, tld)

            out.verb(f"{summ:4} hits out of {len(tld):4} for \"{j}\"")
            if i < len(ina) - 1 and time() - start < pause:
                nap = pause - (time() - start)
                out.verb(f"sleeping for {nap} seconds")
                sleep(nap)

    return
