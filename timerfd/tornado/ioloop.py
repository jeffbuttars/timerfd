from timerfd import Timerfd
from tornado.platform.epoll import EPollIOLoop
from tornado import stack_context


class EPollTimerfdIOLoop(EPollIOLoop, object):

   #  def initialize(self, **kwargs):
   #      """todo: Docstring for initialize

   #      :param **kwargs: arg description
   #      :type **kwargs: type description
   #      :return:
   #      :rtype:
   #      """
   #      super(UceemIOLoop, self).initialize(**kwargs)
   # #initialize()

    def add_timeout(self, deadline, callback):
        timeout = _Timeout(deadline, stack_context.wrap(callback), self)
        timeout.start()
        return timeout

    def remove_timeout(self, timeout):
        timeout.remove()
        self.revmove_handler(timeout.tfd.fd)
        self._cancellations += 1
#EPollTimerfdIOLoop


class _Timeout(object):
    """"""

    __slots__ = ['deadline', 'callback', 'tfd', 'io_loop']

    def __init__(self, deadline, callback, io_loop):
        self.callback = callback
        self.deadline = deadline
        self.io_loop = io_loop
        self.tfd = Timerfd(deadline=deadline)
    #__init__()

    def __call__(self, fd, events):
        self.callback()

        # Remove ourselves
        self.io_loop.remove_handler(self.tfd.fd)
    #__call__()

    def start(self):
        """todo: Docstring for start
        :return:
        :rtype:
        """
        return self.tfd.start()
        self.io_loop.add_handler(self.tfd.fd, self, self.READ)
    #start()

    def remove(self):
        """todo: Docstring for remove
        :return:
        :rtype:
        """
        self.tfd.stop()
        self.io_loop.remove_handler(self.tfd.fd)
        self.tfd = None
        self.callback = None
        self.deadline = None
        self.io_loop = None
    #remove()
