import logging
import time
from ochopod.bindings.generic.marathon import Pod
from ochopod.core.utils import shell
from ochopod.models.piped import Actor as Piped

logger = logging.getLogger('ochopod')

if __name__ == '__main__':

    class Strategy(Piped):

        cwd = '/opt/handler'
        pid = None
        since = 0.0

        # This method is optional for Ochopod to work, but we will always implement it and
        # return the uptime of the sub-process at least.

        def sanity_check(self, pid):
            #
            # - simply use the provided process ID to start counting time
            # - this is a cheap way to measure the sub-process up-time
            #
            now = time.time()
            if pid != self.pid:
                self.pid = pid
                self.since = now
            lapse = (now - self.since) / 3600.0
            return {'uptime': '%.2f hours (pid %s)' % (lapse, pid)}

        def configure(self, cluster):
            #
            # - simply pause for a minute and stop
            # - specify what you need to run below
            #
            return 'python /opt/flaskChatbot/run.py', {}


    Pod().boot(Strategy)