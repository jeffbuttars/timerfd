import timerfd.util as util


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

        self._cb = cb
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
    def last_deadline(self):
        return self._last_deadline

    @property
    def last_interval(self):
        return self._last_interval

    def start(self, deadline=None, interval=None, cb=None):
        """todo: Docstring for start

        :param deadline: arg description
        :type deadline: type description
        :param interval: arg description
        :type interval: type description
        :return:
        :rtype:
        """

        self._deadline = deadline or self._deadline
        self._interval = interval or self._interval
        self._cb = cb or self._cb

        self._last_deadline, self._last_interval = util.settime(
            self._fd,
            self._deadline,
            self._interval,
        )

        return (self._last_deadline, self._last_interval)
    #start()

    def stop(self):
        """todo: Docstring for stop
        :return:
        :rtype:
        """

        self._last_deadline, self._last_interval = util.settime(self._fd, 0, 0)
        return (self._last_deadline, self._last_interval)
    #stop()

    def expired(self):
        """todo: Docstring for expired
        :return:
        :rtype:
        """
        return False
    #expired()
#Timerfd
