# coding=utf8

"""
    A simple process pool

    Usage:

        pool = ProcessPool(size=4)  # size: how many processes in pool [default: 1]
        pool.start()  # start all processes to work
        pool.append_job(myjob, *args, **kwargs)  # add one job to queue
        pool.join()  # waiting all jobs done
        pool.stop()  # kill all processes in pool
"""


import multiprocessing
from multiprocessing import Process, JoinableQueue as Queue, Value
from Queue import Empty


# macros: process's states
RUNNING = 1
STOPPED = 0


class ProcessWorker(Process):

    def __init__(self, pool):
        super(ProcessWorker, self).__init__()
        self.pool = pool
        self.daemon = True  # When a process exits, it attempts to terminate all of its daemonic child processes
        self.state = Value('d', STOPPED)  # `worker.state` should be shared in `main process` and `worker process`

    def start(self):
        self.state.value = RUNNING
        super(ProcessWorker, self).start()

    def stop(self):
        self.state.value = STOPPED

    def run(self):

        while self.state.value == RUNNING:  # !import use `==` but not `is` here: `1.0` and `1` are different objects
            # dont use `Queue.empty` to check but use Exception `Empty`,
            # because another thread may put a job right after your checking
            try:
                job, args, kwargs = self.pool.jobs.get_nowait()
            except Empty:
                continue
            else:
                # do the job
                try:
                    result = job(*args, **kwargs)
                    self.pool.results.put(result)
                except Exception, e:
                    self.stop()
                    raise e  # error occurred, raise it and stop this thread
                finally:
                    self.pool.jobs.task_done()


class ProcessPool(object):

    def __init__(self, size=1):
        self.size = size
        self.jobs = Queue()
        self.results = Queue()
        self.processes = []

    def start(self):
        '''start all processes'''

        for i in range(self.size):
            self.processes.append(ProcessWorker(self))

        for process in self.processes:
            process.start()

    def append_job(self, job, *args, **kwargs):
        self.jobs.put((job, args, kwargs))

    def join(self):
        '''waiting all jobs done'''
        self.jobs.join()

    def stop(self):
        '''kill all processes'''
        for process in self.processes:
            process.stop()

        for process in self.processes:  # waiting processes completing
            if process.is_alive():
                process.join()

        del self.processes[:]  # reset processes to empty



if __name__ == '__main__':
    '''Time this test should get about 1s'''

    from time import sleep

    pool = ProcessPool(size=10)

    def foo(i):
        sleep(.1)
        print "hello world! %d" % i
        return 1

    pool.start()

    for x in range(100):
        pool.append_job(foo, x)

    pool.join()
    pool.stop()
