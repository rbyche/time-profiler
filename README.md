# Simple time profiler for Python
## Usage example
```
from profiler import Profiler
from time import sleep


Profiler.start_range('global')

with Profiler('func1'):
	sleep(1)

with Profiler('func1'):
	sleep(1)

with Profiler('func2'):
    sleep(2)
    
    with Profiler('func3'):
        _ = list(range(100000))

Profiler.stop_range('global')

print(Profiler.summary())
{"data": {"global": {"count": 1, "accu": 4.010914325714111, "min": 4.010914325714111, "max": 4.010914325714111, "mean": 4.010914325714111}, "func1": {"count": 2, "accu": 2.0029799938201904, "min": 1.0012927055358887, "max": 1.0016872882843018, "mean": 1.0014899969100952}, "func2": {"count": 1, "accu": 2.007107973098755, "min": 2.007107973098755, "max": 2.007107973098755, "mean": 2.007107973098755}, "func3": {"count": 1, "accu": 0.004334211349487305, "min": 0.004334211349487305, "max": 0.004334211349487305, "mean": 0.004334211349487305}}}

Profiler.clear()

with Profiler('func1'):
	sleep(1)

print(Profiler.summary())
{"data": {"func1": {"count": 1, "accu": 1.0013227462768555, "min": 1.0013227462768555, "max": 1.0013227462768555, "mean": 1.0013227462768555}}}

print(Profiler.get_logs('func1'))
[('func1', [1.0013227462768555])]
```
