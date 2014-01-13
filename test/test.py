#!/usr/bin/env python
# encoding: utf-8
# edfcd9c1dda54c648ddf19005fdaad4d

import timerfd
import timerfd.util


def main():

    timerfd.Timerfd()

    print(dir(timerfd.util))

    t = timerfd.util.create()
    print(t)

    timeleft = timerfd.util.settime(t, deadline=1000)
    print("timeleft: ", timeleft)

    timeleft = timerfd.util.settime(t, deadline=1000)
    print("timeleft: ", timeleft)

    gt = timerfd.util.gettime(t)
    print("got time", gt)

    gt = timerfd.util.gettime(t)
    print("got time", gt)

    timeleft = timerfd.util.settime(t, deadline=0)
    print("last timeleft: ", timeleft)

    gt = timerfd.util.gettime(t)
    print("last got time", gt)

    print("Start class test.")
    tf = timerfd.Timerfd()
# main()

if __name__ == '__main__':
    main()

# To run with gdb:
#   gdb -ex r --args python ./test.py
