Simple Pools
------------

Simple "Thread Pool" and "Process Pool" implement with standard library `threading` and `multiprocessing`.

What For
--------

Many cases we need our own pool implementation, this code tells where to start.

Usage
-----

Thread Pool:

```python
from threadpool import ThreadPool

pool = ThreadPool(size=10)
pool.start()
pool.append_job(myjob, *args, **kwargs)
pool.join()   # wait all jobs done
pool.stop()   # kill all threads in pool
```


Process Pool:

```python
from threadpool import ThreadPool

pool = ProcessPool(size=4)
pool.start()
pool.append_job(myjob, *args, **kwargs)  # add one job to queue
pool.join()  # waiting all jobs done
pool.stop()  # kill all processes in pool
```

License
-------

No license. It can be used in any purpose.
