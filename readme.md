## Usage

```python
import json
from nvsmi import NVLog

log = NVLog()
print(json.dumps(log, indent=2))
print(log.as_table())
```

## Known issues

* The power usages in the table of `nvidia-smi` can not be found in the output in `nvidia-smi -q`.  
So it uses the `Power Draw` in `Power Readings` instead.
