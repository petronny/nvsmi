# Usage

```python
import json
from nvsmi import NVLog

log = NVLog()
print(json.dumps(log, indent=2))
print(log.as_table())
```
