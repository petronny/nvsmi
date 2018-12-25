## Usage

```python
from nvsmi import NVLog

log = NVLog()

# Access attributes
print(log['version']))

# Print the original `nvidia-smi` table
print(log.as_table())

# Print the `nvidia-smi` table enhanced by me
log = NVLogPlus()
print(log.as_table())
```

## Known issues

* The power usages in the `nvidia-smi` table can not be found in `nvidia-smi -q`.  
So it uses the `Power Draw` in `Power Readings` instead.
* In some old versions, `nvidia-smi -q` doesn't have `CUDA Version`.  
So it will show `None` or `N/A`.
* I don't know which part in `nvidia-smi -q` is the `Volatile Uncorr. ECC` in the `nvidia-smi` table.  
So it will always show `N/A` for now.
