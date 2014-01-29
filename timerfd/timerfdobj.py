import logging
logger = logging.getLogger('timerfd')

import timerfd.lib as lib


class TimerfdException(Exception):
    pass
#TimerfdException


class Timerfd(object):
    """A nice object to encapsulate and abstract the raw timerfd
    calls used in timerfd.lib.

    If you need need to squeek out every last bit of performance, use the timerfd.lib
    module. Otherwise, is this class.
    """

    CLOCK_REALTIME = lib.CLOCK_REALTIME
    CLOCK_MONOTONIC = lib.CLOCK_MONOTONIC
    TFD_NONBLOCK = lib.TFD_NONBLOCK
    TFD_CLOEXEC = lib.TFD_CLOEXEC

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
        self._last_deadline = None
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

        self._callbacks = cb or []
        self._fd = lib.create(self._clockid, self._cflags)
    #__init__()

    @property
    def fd(self):
        """
        Get the file descriptor for this timer instance.
        """
        return self._fd

    @property
    def realtime(self):
        """
        Get if this instance is using a realtime timer or not
        """
        return self._realtime

    @property
    def monotonic(self):
        """
        Get if this instance is using a monotonic timer or not
        """
        return self._monotonic

    @property
    def async(self):
        """
        Get if this instance is asynchronous or not
        """
        return self._async

    @property
    def cloexec(self):
        """
        Get if this instance is configured with closexec or not
        """
        return self._cloexec

    @property
    def deadline(self):
        """
        Get the deadline value this instance will use to start the timer.
        """
        return self._deadline

    @property
    def interval(self):
        """
        Get the interval value this instance will use to start the timer.
        """
        return self._interval

    @property
    def last_deadline(self):
        """
        Get the last/previous deadline value this instance used to start the timer.
        """
        return self._last_deadline

    @property
    def last_interval(self):
        """
        Get the last/previous interval value this instance used to start the timer.
        """
        return self._last_interval

    @property
    def delta(self):
        """
        Return a timedelta of the time remaining until the next
        timer expiration.

        :return: Time until next expiration
        :rtype: datetime.timedelta
        """

        return lib.gettime(self._fd)[0]
    #delta()

    def start(self, deadline=None, interval=None, cb=None):
        """By default, use the deadline and interval
        set at instantiation. If deadline or interval parameters
        are used, then they will be used for that call only, and will
        _not_ be used again. For a persistent deadline and interval value
        set them on instantiation.

        :param deadline: arg description
        :type deadline: type description
        :param interval: arg description
        :type interval: type description
        :return: (previous deadline value, previous interval value)
        :rtype: tuple
        """

        dl = deadline or self._deadline
        itvl = interval or self._interval

        if cb:
            self._callbacks.append(cb)

        logger.debug("using settime, fd:%s, deadline:%s, interval:%s",
                     self._fd, dl, itvl)
        self._last_deadline, self._last_interval = lib.settime(
            self._fd,
            dl,
            itvl,
        )

        return (self._last_deadline, self._last_interval)
    #start()

    def stop(self):
        """Stop the timer without calling any configured callbacks.
        Returns the remaing time and the configured interval

        :return: (time left, interval)
        :rtype: tuple
        """

        self._last_deadline, self._last_interval = lib.settime(self._fd, 0, 0)

        logger.debug("stopped, last_deadline: %s, last_interval: %s",
                     self._last_deadline, self._last_interval)
        return (self._last_deadline, self._last_interval)
    #stop()

    def restart(self, cb=None):
        """Restart a timer.
        If a timer is stopped before it expires, you can restart the timer and it will
        start the timer using the time left on the timer when it was stopped. The interval
        value will be preserved as well.

        If restart is called but stop() has not been called, then it will behave like start()
        If restart is called but there is time left on the timer, then it will behave like start()

        You can also add a callback when calling restart.

        :return: (previous deadline value, previous interval value)
        :rtype: tuple
        """

        delta = self._last_deadline or self._deadline
        inter = self._last_interval or self._interval or 0

        if not delta:
            raise TimerfdException("Unable to restart timer without a last delta or deadline")

        logger.debug("restarting, deadline:%s, interval:%s", delta, inter)
        return self.start(deadline=delta, interval=inter, cb=cb)
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
        exp = lib.expired(self._fd)
        cb_res = []
        if exp > 0:
            cb_res += [x() for x in self._callbacks]

        return (exp, cb_res)
    #expired()
#Timerfd
