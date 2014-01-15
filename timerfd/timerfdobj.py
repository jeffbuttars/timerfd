import os
import struct
import errno
import timerfd.util as util


class TimerfdException(Exception):
    pass
#TimerfdException


class Timerfd(object):
    """A nice object to encapsulate and abstract the raw timerfd
    calls used in timerfd.util.

    If you need need to squeek out every last bit of performance, use the timerfd.util
    module. Otherwise, is this class.
    """

    CLOCK_REALTIME = util.CLOCK_REALTIME
    CLOCK_MONOTONIC = util.CLOCK_MONOTONIC
    TFD_NONBLOCK = util.TFD_NONBLOCK
    TFD_CLOEXEC = util.TFD_CLOEXEC

    def __init__(self,
                 deadline=None,
                 interval=None,
                 realtime=False,
                 monotonic=False,
                 async=False,
                 cloexec=False,
                 cb=None,
                 ):

        self._deadline = deadline
        self._interval = interval
        self._last_delta = None
        self._last_interval = None
        self._realtime = realtime
        self._monotonic = monotonic
        self._async = async
        self._cloexec = cloexec
        self._cflags = 0

        if async:
            self._cflags |= Timerfd.TFD_NONBLOCK
        if cloexec:
            self._cflags |= Timerfd.TFD_CLOEXEC

        if not self._realtime and not self._monotonic:
            self._monotonic = True
            self._clockid = Timerfd.CLOCK_MONOTONIC
        else:
            self._clockid = (self._realtime and Timerfd.CLOCK_REALTIME) or Timerfd.CLOCK_MONOTONIC

        self._callbacks = cb
        self._fd = util.create(self._clockid, self._cflags)
    #__init__()

    @property
    def fd(self):
        return self._fd

    @property
    def realtime(self):
        return self._realtime

    @property
    def monotonic(self):
        return self._monotonic

    @property
    def async(self):
        return self._async

    @property
    def cloexec(self):
        return self._cloexec

    @property
    def deadline(self):
        return self._deadline

    @property
    def interval(self):
        return self._interval

    @property
    def last_delta(self):
        return self._last_delta

    @property
    def last_interval(self):
        return self._last_interval

    def start(self, deadline=None, interval=None, cb=None):
        """todo: Docstring for start

        :param deadline: arg description
        :type deadline: type description
        :param interval: arg description
        :type interval: type description
        :return: (previous deadline value, previous interval value)
        :rtype: tuple
        """

        self._deadline = deadline or self._deadline
        self._interval = interval or self._interval

        if cb:
            self._callbacks.append(cb)

        self._last_delta, self._last_interval = util.settime(
            self._fd,
            self._deadline,
            self._interval,
        )

        return (self._last_delta, self._last_interval)
    #start()

    def stop(self):
        """Stop the timer without calling any configured callbacks.
        Returns the remaing time and the configured interval

        :return: (time left, interval)
        :rtype: tuple
        """

        self._last_delta, self._last_interval = util.settime(self._fd, 0, 0)
        return self._last_delta
    #stop()

    def restart(self, cb=None):
        """Restart a timer.
        If a timer is stopped before it expires, you can restart the timer and it will
        start the timer using the time left on the timer when it was stopped. The interval
        value will be preserved as well.

        If restart is called but stop() has not been called, then it will behave like start()
        If restart is called but there is time left on the timer, then it will behave like start()

        :return: (previous deadline value, previous interval value)
        :rtype: tuple
        """

        if cb:
            self._callbacks.append(cb)

        delta = self._last_delta or self._deadline
        inter = self._last_interval or self._interval or 0

        if not delta:
            raise TimerfdException("Unable to restart timer without a last delta or deadline")

        return self.start(deadline=delta, interval=inter)
    #restart()

    def expired(self):
        """
        By default, if the timer has not expired at least once, this will
        block until the next expiration.
        If the timer is created with async set to true, then this will always
        return immediately.

        If an expiration happens, then all callbacks will be called in the order
        they were added. The callback results will be returned in array of results
        in the same order as the callbacks were called.

        will return a tuple of callback results and how many times the timer
        has expired since the last read. In async mode, this will simply return 0,
        if the timer has not expired.

        :return: (callback results, Number of expirations)
        :rtype: tuple
        """

        res = 0
        try:
            res = struct.unpack("Q", os.read(self._fd, 8))[0]
        except IOError as e:
            if e[0] != errno.EAGAIN:
                raise
            return res

        cb_results = [x() for x in self._callbacks]

        return (cb_results, res)
    #expired()

    def delta(self):
        """
        Return a timedelta of the time remaining until the next
        timer expiration.

        :return: Time until next expiration
        :rtype: datetime.timedelta
        """

        return util.gettime(self._fd)[0]
    #delta()
#Timerfd
