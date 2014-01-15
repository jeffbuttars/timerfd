#!/usr/bin/env python
# encoding: utf-8
# edfcd9c1dda54c648ddf19005fdaad4d

import os
import datetime
import unittest

from timerfd import Timerfd
import timerfd.util


class TestTimerfdUtil(unittest.TestCase):
    """Docstring for TimerfdUtil """

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
        t = timerfd.util.create()
        self.assertIsInstance(t, int)
        self.tid = t
    #create()

    def test_create_realtime(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.util.create(clockid=timerfd.util.CLOCK_REALTIME)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime()

    def test_create_monotonic(self):
        """todo: Docstring for test_create_monotonic
        :return:
        :rtype:
        """
        self.tid = timerfd.util.create(clockid=timerfd.util.CLOCK_MONOTONIC)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic()

    def test_create_nonblock(self):
        """todo: Docstring for create_nonblock"""
        self.tid = timerfd.util.create(flags=timerfd.util.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_nonblock()

    def test_create_close_exec(self):
        """todo: Docstring for create_close_exec"""
        self.tid = timerfd.util.create(flags=timerfd.util.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_close_exec()

    def test_nonblock_cloexec(self):
        """todo: Docstring for nonblock_cloexec"""
        self.tid = timerfd.util.create(
            flags=(timerfd.util.TFD_CLOEXEC | timerfd.util.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_nonblock_cloexec()

    def test_create_realtime_nonblock(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_REALTIME,
            flags=timerfd.util.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_nonblock()

    def test_create_realtime_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_REALTIME,
            flags=timerfd.util.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_cloexec()

    def test_create_realtime_nonblock_cloexec(self):
        """todo: Docstring for create_realtime"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_REALTIME,
            flags=(timerfd.util.TFD_CLOEXEC | timerfd.util.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_create_realtime_nonblock_cloexec()

    def test_create_monotonic_nonblock(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_MONOTONIC,
            flags=timerfd.util.TFD_NONBLOCK)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_nonblock()

    def test_create_monotonic_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_MONOTONIC,
            flags=timerfd.util.TFD_CLOEXEC)
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_cloexec()

    def test_create_monotonic_nonblock_cloexec(self):
        """todo: Docstring for create_monotonic"""
        self.tid = timerfd.util.create(
            clockid=timerfd.util.CLOCK_MONOTONIC,
            flags=(timerfd.util.TFD_CLOEXEC | timerfd.util.TFD_NONBLOCK))
        self.assertIsInstance(self.tid, int)
    #test_create_monotonic_nonblock_cloexec()

    ###############################################
    ### test_settime ##############################
    ###############################################

    def _settime(self, dead, inter):
        print("\n_settime: deadline: %s, interval: %s" % (dead, inter))
        vi = timerfd.util.settime(self.tid, dead, inter)
        print("settime result ", vi)

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

        vi = self._settime(deadline_d, interval_d)
        # print("settime result ", vi)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

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
        vi = timerfd.util.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline, 0)
        vi = timerfd.util.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline, interval)
        vi = timerfd.util.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        self._settime(0, 0)
        vi = timerfd.util.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline_d, 0)
        vi = timerfd.util.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)

        self._settime(deadline_d, interval_d)
        vi = timerfd.util.gettime(self.tid)
        self.assertGreater(vi[0].microseconds, 0)
        self.assertGreater(vi[1].microseconds, 0)

        self._settime(0, 0)
        vi = timerfd.util.gettime(self.tid)
        self.assertEqual(vi[0].microseconds, 0)
        self.assertEqual(vi[1].microseconds, 0)
    #test_gettime()
#TestTimerfdUtil


class TestTimerfdObj(unittest.TestCase):
    """Docstring for TimerfdObj """

    def setUp(self):
        """todo: to be defined"""
        self.tfd = None
    #setUp()

    def test_class_props(self):
        """todo: Docstring for class_props"""
        # print(dir(Timerfd))
        self.assertEqual(timerfd.util.CLOCK_REALTIME, Timerfd.CLOCK_REALTIME)
        self.assertEqual(timerfd.util.CLOCK_MONOTONIC, Timerfd.CLOCK_MONOTONIC)
        self.assertEqual(timerfd.util.TFD_NONBLOCK, Timerfd.TFD_NONBLOCK)
        self.assertEqual(timerfd.util.TFD_CLOEXEC, Timerfd.TFD_CLOEXEC)
    #test_class_props()

    def test_init(self):
        self.tfd = Timerfd()
    #test_init()

#TestTimerfdObj


def main():
    unittest.main()
# main()

if __name__ == '__main__':
    main()

# To run with gdb:
#   gdb -ex r --args python ./test.py