#!/usr/bin/env python
# encoding: utf-8
# edfcd9c1dda54c648ddf19005fdaad4d

import logging

# Set up the logger
logger = logging.getLogger('timerfd')
# Use a console handler, set it to debug by default
logger_ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(('%(asctime)s %(levelname)s:%(process)s'
                                   ' %(lineno)s:%(module)s:%(funcName)s()'
                                   ' %(message)s'))
logger_ch.setFormatter(log_formatter)
logger.addHandler(logger_ch)

import os
import datetime
import unittest
import time

from timerfd import Timerfd
import timerfd.lib


class TestTimerfdLib(unittest.TestCase):
    """Docstring for TimerfdLib """

    def setUp(self):
        """todo: to be defined"""
        self.tid = None
    #setUp()

    def tearDown(self):
        """todo: Docstring for tearDown
        :return:
        :rtype:
        """

        if self.tid:
            os.close(self.tid)
    #tearDown()

    ###############################################
    ### test_create ###############################
    ###############################################

    def test_create(self):
        t = timerfd.lib.create()
        self.assertIsInstance(t, int)
        self.tid = t
    #create()

    def test_create_realtime(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.lib.create(clockid=timerfd.lib.CLOCK_REALTIME)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime()

    def test_create_monotonic(self):
        """todo: Docstring for test_create_monotonic
        :return:
        :rtype:
        """
        self.tid = timerfd.lib.create(clockid=timerfd.lib.CLOCK_MONOTONIC)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic()

    def test_create_nonblock(self):
        """todo: Docstring for create_nonblock"""
        self.tid = timerfd.lib.create(flags=timerfd.lib.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_nonblock()

    def test_create_close_exec(self):
        """todo: Docstring for create_close_exec"""
        self.tid = timerfd.lib.create(flags=timerfd.lib.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_close_exec()

    def test_nonblock_cloexec(self):
        """todo: Docstring for nonblock_cloexec"""
        self.tid = timerfd.lib.create(
            flags=(timerfd.lib.TFD_CLOEXEC | timerfd.lib.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_nonblock_cloexec()

    def test_create_realtime_nonblock(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_REALTIME,
            flags=timerfd.lib.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_nonblock()

    def test_create_realtime_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_REALTIME,
            flags=timerfd.lib.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_cloexec()

    def test_create_realtime_nonblock_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_REALTIME,
            flags=(timerfd.lib.TFD_CLOEXEC | timerfd.lib.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_nonblock_cloexec()

    def test_create_monotonic_nonblock(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_MONOTONIC,
            flags=timerfd.lib.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_nonblock()

    def test_create_monotonic_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_MONOTONIC,
            flags=timerfd.lib.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_cloexec()

    def test_create_monotonic_nonblock_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.lib.create(
            clockid=timerfd.lib.CLOCK_MONOTONIC,
            flags=(timerfd.lib.TFD_CLOEXEC | timerfd.lib.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_nonblock_cloexec()

    ###############################################
    ### test_settime ##############################
    ###############################################

    def _settime(self, dead, inter):
        # print("\n_settime: deadline: %s, interval: %s" % (dead, inter))
        vi = timerfd.lib.settime(self.tid, dead, inter)
        # print("settime result ", vi)

        self.assertIsInstance(vi, tuple)
        self.assertIsInstance(vi[0], datetime.timedelta)
        self.assertIsInstance(vi[1], datetime.timedelta)

        return vi

    def test_settime(self):
        """todo: Docstring for settime"""
        deadline = 999999
        interval = 999999
        deadline_d = datetime.timedelta(microseconds=deadline)
        interval_d = datetime.timedelta(microseconds=interval)

        self.test_create()

        vi = self._settime(0, 0)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        vi = self._settime(deadline, 0)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)


        vi = self._settime(deadline, interval)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        vi = self._settime(0, 0)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        vi = self._settime(0, 0)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        vi = self._settime(deadline_d, 0)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        # Throw some absolute times in there.
        # now = datetime.datetime.now()
        # vi = self._settime(now + deadline_d, 0)
        # self.assertEqual(vi[0].microseconds, deadline)
        # self.assertEqual(vi[1].microseconds, 0)

        vi = self._settime(deadline_d, interval_d)
        # print("settime result ", vi)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        # vi = self._settime(datetime.datetime.now() + deadline_d, interval_d)
        # # print("settime result ", vi)
        # self.assertEqual(vi[0].microseconds, deadline)
        # self.assertEqual(vi[1].microseconds, 0)

        vi = self._settime(0, 0)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        vi = self._settime(0, 0)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)
    #test_settime()

    def test_gettime(self):
        """todo: Docstring for gettime"""
        deadline = 100
        interval = 100
        deadline_d = datetime.timedelta(microseconds=deadline)
        interval_d = datetime.timedelta(microseconds=interval)

        self.test_create()

        self._settime(0, 0)
        vi = timerfd.lib.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline, 0)
        vi = timerfd.lib.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline, interval)
        vi = timerfd.lib.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        self._settime(0, 0)
        vi = timerfd.lib.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline_d, 0)
        vi = timerfd.lib.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline_d, interval_d)
        vi = timerfd.lib.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        self._settime(0, 0)
        vi = timerfd.lib.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)
    #test_gettime()
#TestTimerfdLib


class TestTimerfdLibTime(unittest.TestCase):
    """Docstring for TimerfdLibTime """

    def setUp(self):
        """todo: to be defined"""
        self.deadline = 1000000
        self.interval = 1000000
        self.d_deadline = datetime.timedelta(microseconds=self.deadline)
        self.d_interval = datetime.timedelta(microseconds=self.interval)
        self.max_intervals = 5
    #setUp()

    def timer_sub_test(self, deadline, interval=None, *args, **kwargs):
        """todo: Docstring for timer_sub_test
        :return:
        :rtype:
        """

        self.test_create(*args, **kwargs)
        deadline = deadline or self.d_deadline
        interval = interval or 0

        print("\ntimer_sub_test settime ", deadline, interval)
        now = datetime.datetime.now()
        timerfd.lib.settime(self.tid, deadline, interval)

        print("timer_sub_test reading ", self.tid)
        expires = timerfd.lib.expired(self.tid)
        while expires == 0:
            expires = timerfd.lib.expired(self.tid)

        delta = datetime.datetime.now() - now
        # Throw in a little compensation for interval testing below.
        now = datetime.datetime.now() - datetime.timedelta(microseconds=100000)
        print("timer_sub_test read ", expires, " delta ", delta)

        # This is tricky, but the seconds of the delta 'should' be the same
        # as deadline seconds.
        self.assertEqual(self.d_deadline.seconds, delta.seconds)

        c_interval = 0
        if interval:
            print("Testing interval", interval)
            print("\ntimer_sub_test settime with interval ", deadline, interval)
            while c_interval < self.max_intervals:
                print("current interval", c_interval)
                print("timer_sub_test reading ", self.tid)
                expires = timerfd.lib.expired(self.tid)
                while expires == 0:
                    expires = timerfd.lib.expired(self.tid)
                c_interval += expires

                delta = datetime.datetime.now() - now
                print("timer_sub_test read interval ", expires, " delta ", delta)
                # Throw in a little compensation for interval testing below.
                now = datetime.datetime.now() - datetime.timedelta(microseconds=100000)

                # This is tricky, but the seconds of the delta 'should' be the same
                # as deadline seconds.
                self.assertEqual(self.d_interval.seconds, delta.seconds)

        timerfd.lib.settime(self.tid, 0, 0)
    #timer_sub_test()

    def timer_test(self, *args, **kwargs):
        """A generic timer test.

        :param *args: arg description
        :type *args: type description
        :param **kwargs: arg description
        :type **kwargs: type description
        :return:
        :rtype:
        """
        self.timer_sub_test(self.deadline, *args, **kwargs)
        self.timer_sub_test(self.deadline, self.interval, *args, **kwargs)
        self.timer_sub_test(datetime.datetime.now() + self.d_deadline,
                            *args, **kwargs)
        self.timer_sub_test(datetime.datetime.now() + self.d_deadline,
                            self.interval, *args, **kwargs)

        self.timer_sub_test(self.d_deadline, *args, **kwargs)
        self.timer_sub_test(self.d_deadline, self.d_interval, *args, **kwargs)
        self.timer_sub_test(datetime.datetime.now() + self.d_deadline,
                            *args, **kwargs)
        self.timer_sub_test(datetime.datetime.now() + self.d_deadline,
                            self.d_interval, *args, **kwargs)
    #timer_test()

    def test_default_timer(self):
        """todo: Basic tests for a blocking timer."""
        self.timer_test(clockid=timerfd.lib.CLOCK_MONOTONIC)
        self.timer_test(clockid=timerfd.lib.CLOCK_REALTIME)
    #test_default_timer()

    def test_async_timer(self):
        """todo: Basic tests for a non-blocking timer."""
        self.timer_test(
            clockid=timerfd.lib.CLOCK_MONOTONIC, flags=timerfd.lib.TFD_NONBLOCK)
        self.timer_test(
            clockid=timerfd.lib.CLOCK_REALTIME, flags=timerfd.lib.TFD_NONBLOCK)
    #test_async_timer()

    def test_create(self, *args, **kwargs):
        t = timerfd.lib.create(*args, **kwargs)
        self.assertIsInstance(t, int)
        self.tid = t
    #create()
#TestTimerfdLibTime


class TestTimerfdObj(unittest.TestCase):
    """Docstring for TimerfdObj """

    def setUp(self):
        """todo: to be defined"""
        self.tfd = None
    #setUp()

    def test_init(self):
        self.tfd = Timerfd()
    #test_init()

    def test_class_props(self):
        """todo: Docstring for class_props"""
        # print(dir(Timerfd))
        self.assertEqual(timerfd.lib.CLOCK_REALTIME, Timerfd.CLOCK_REALTIME)
        self.assertEqual(timerfd.lib.CLOCK_MONOTONIC, Timerfd.CLOCK_MONOTONIC)
        self.assertEqual(timerfd.lib.TFD_NONBLOCK, Timerfd.TFD_NONBLOCK)
        self.assertEqual(timerfd.lib.TFD_CLOEXEC, Timerfd.TFD_CLOEXEC)
    #test_class_props()

    def test_create_realtime(self):
        """todo: Docstring for create_realtime"""
        self.tfd = Timerfd(realtime=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_realtime()

    def test_create_monotonic(self):
        """todo: Docstring for test_create_monotonic
        :return:
        :rtype:
        """
        self.tfd = Timerfd(monotonic=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_monotonic()

    def test_create_nonblock(self):
        """todo: Docstring for create_nonblock"""
        self.tfd = Timerfd(async=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_nonblock()

    def test_create_close_exec(self):
        """todo: Docstring for create_close_exec"""
        self.tfd = Timerfd(cloexec=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_close_exec()

    def test_nonblock_cloexec(self):
        """todo: Docstring for nonblock_cloexec"""
        self.tfd = Timerfd(async=True, cloexec=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_nonblock_cloexec()

    def test_create_realtime_nonblock(self):
        """todo: Docstring for create_realtime"""
        self.tfd = Timerfd(async=True, realtime=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_realtime_nonblock()

    def test_create_realtime_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tfd = Timerfd(cloexec=True, realtime=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_realtime_cloexec()

    def test_create_realtime_nonblock_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tfd = Timerfd(async=True, cloexec=True, realtime=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_realtime_nonblock_cloexec()

    def test_create_monotonic_nonblock(self):
        """todo: Docstring for create_monotonic"""
        self.tfd = Timerfd(async=True, monotonic=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_monotonic_nonblock()

    def test_create_monotonic_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tfd = Timerfd(cloexec=True, monotonic=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_monotonic_cloexec()

    def test_create_monotonic_nonblock_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tfd = Timerfd(async=True, cloexec=True, monotonic=True)
        self.assertIsInstance(self.tfd, Timerfd)
    #test_create_monotonic_nonblock_cloexec()
#TestTimerfdObj


class TestTimerfdObjTime(unittest.TestCase):
    """Docstring for TimerfdObjTime """

    def setUp(self):
        """todo: to be defined"""

        self.deadline = 1000000
        self.interval = 1000000
        self.d_deadline = datetime.timedelta(microseconds=self.deadline)
        self.d_interval = datetime.timedelta(microseconds=self.interval)
        self.max_intervals = 5
        self.tfd = None
    #setUp()

    def timer_sub_test(self, deadline=None, interval=0, **kwargs):
        """todo: Docstring for timer_sub_test
        :return:
        :rtype:
        """

        deadline = deadline or self.d_deadline

        self.tfd = Timerfd(deadline=deadline, interval=interval, **kwargs)
        self.assertIsInstance(self.tfd, Timerfd)

        # now = datetime.datetime.now()
        # dline = now + self.d_deadline
        # print("test time: now %s" % now)
        # print("test time: later %s" % (dline))
        # self.tfd = Timerfd(
        #     deadline=(dline),
        #     interval=interval,
        #     **kwargs)
        # self.assertIsInstance(self.tfd, Timerfd)

        # print("\ntimer_sub_test settime ", dline, self.d_deadline, interval)
        # now = datetime.datetime.now()
        # self.tfd.start()

        print("timer_sub_test reading ", self.tfd.fd)
        expires, cbr = self.tfd.expired()
        self.assertIsInstance(expires, int)
        self.assertIsInstance(cbr, list)

        while expires == 0:
            expires, cbr = self.tfd.expired()

        delta = datetime.datetime.now() - now
        # Throw in a little compensation for interval testing below.
        now = datetime.datetime.now() - datetime.timedelta(microseconds=100000)
        print("timer_sub_test read ", expires, " delta ", delta)

        # This is tricky, but the seconds of the delta 'should' be the same
        # as deadline seconds.
        self.assertEqual(self.d_deadline.seconds, delta.seconds)

        c_interval = 0
        if interval:
            print("Testing interval", interval)
            print("\ntimer_sub_test settime with interval ", deadline, interval)
            while c_interval < self.max_intervals:
                print("current interval", c_interval)
                print("timer_sub_test reading ", self.tfd.fd)
                expires, cbr = self.tfd.expired()
                while expires == 0:
                    expires, cbr = self.tfd.expired()
                c_interval += expires

                delta = datetime.datetime.now() - now
                print("timer_sub_test read interval ", expires, " delta ", delta)
                # Throw in a little compensation for interval testing below.
                now = datetime.datetime.now() - datetime.timedelta(microseconds=100000)

                # This is tricky, but the seconds of the delta 'should' be the same
                # as deadline seconds.
                self.assertEqual(self.d_interval.seconds, delta.seconds)

        self.tfd.stop()
    #timer_sub_test()

    def timer_test(self, *args, **kwargs):
        """A generic timer test.

        :param *args: arg description
        :type *args: type description
        :param **kwargs: arg description
        :type **kwargs: type description
        :return:
        :rtype:
        """
        self.timer_sub_test(self.deadline, *args, **kwargs)
        self.timer_sub_test(self.deadline, self.interval, *args, **kwargs)

        self.timer_sub_test(self.d_deadline, *args, **kwargs)
        self.timer_sub_test(self.d_deadline, self.d_interval, *args, **kwargs)

        self.timer_sub_test(
            datetime.datetime.now() + self.d_deadline, *args, **kwargs)
        self.timer_sub_test(
            datetime.datetime.now() + self.d_deadline, self.d_interval, *args, **kwargs)
    #timer_test()

    def test_default_timer(self):
        """todo: Basic tests for a blocking timer."""
        self.timer_test(monotonic=True)
        self.timer_test(realtime=True)
    #test_default_timer()

    def test_async_timer(self):
        """todo: Basic tests for a non-blocking timer."""
        self.timer_test(monotonic=True, async=True)
        self.timer_test(realtime=True, async=True)
    #test_async_timer()
#TestTimerfdObjTime


class TestTimerfdObjRestart(unittest.TestCase):
    """Docstring for TimerfdObjRestart """

    def setUp(self):
        """todo: to be defined"""
        self.deadline = 1000000
        self.interval = 1000000
        self.d_deadline = datetime.timedelta(microseconds=self.deadline)
        self.d_interval = datetime.timedelta(microseconds=self.interval)
        self.max_intervals = 5
        self.tfd = None
    #setUp()

    def test_basic_restart(self):
        """Start a timer, stop it before it's done, then restart it."""

        # Set up a timer in a normal fashion and start it.

        self.tfd = Timerfd(
            deadline=self.deadline,
            interval=self.interval,
        )
        self.assertIsInstance(self.tfd, Timerfd)

        print("\ntest_basic_restart settime ", self.deadline, self.interval)
        self.tfd.start()

        # Sleep for a short spell
        time.sleep(0.300)

        # Stop the timer, there should be time left on it.
        ldelta, litv = self.tfd.stop()
        print("test_basic_restart stopped, ", ldelta.microseconds, litv)
        self.assertGreater(ldelta.microseconds, 0)

        # restart and run the timer until the end,
        print("test_basic_restart stopped, about to restart ", ldelta.microseconds, litv)
        self.tfd.restart()

        # it should stop at the remaining time interval.
        print("test_basic_restart waiting on expired ")
        exp, cb_res = self.tfd.expired()
        print("test_basic_restart expired ", exp, cb_res)

    #test_basic_restart()

#TestTimerfdObjRestart


def main():
    # unittest.main()
    # unittest.main(defaultTest='TestTimerfdObjRestart')
    unittest.main(defaultTest='TestTimerfdObjTime')
    
# main()

if __name__ == '__main__':
    main()

# To run with gdb:
#   gdb -ex r --args python ./test.py
