## Usage

* As a command line tool

```sh
$ python nvsmi.py
Thu Jan 24 15:41:40 2019
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.25       Driver Version: 390.25       CUDA Version: N/A      |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  TITAN X (Pascal)    Off  | 00000000:04:00.0 Off |                  N/A |
| 36%   60C    P2   120W / 250W |  11749MiB / 12196MiB |     31%      Default |
+-----------------------------------------------------------------------------+
|   1  TITAN X (Pascal)    Off  | 00000000:06:00.0 Off |                  N/A |
| 23%   39C    P0    57W / 250W |      0MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   2  TITAN X (Pascal)    Off  | 00000000:07:00.0 Off |                  N/A |
| 23%   36C    P0    56W / 250W |      0MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   3  TITAN X (Pascal)    Off  | 00000000:08:00.0 Off |                  N/A |
| 23%   38C    P0    57W / 250W |      0MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   4  TITAN X (Pascal)    Off  | 00000000:0C:00.0 Off |                  N/A |
| 23%   30C    P0    56W / 250W |      0MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   5  TITAN X (Pascal)    Off  | 00000000:0D:00.0 Off |                  N/A |
| 23%   32C    P0    57W / 250W |      0MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   6  TITAN X (Pascal)    Off  | 00000000:0E:00.0 Off |                  N/A |
| 23%   23C    P8     9W / 250W |    213MiB / 12196MiB |      0%      Default |
+-----------------------------------------------------------------------------+
|   7  TITAN X (Pascal)    Off  | 00000000:0F:00.0 Off |                  N/A |
| 54%   83C    P2   242W / 250W |   7695MiB / 12196MiB |     49%      Default |
+-----------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   User   Process name                             Usage      |
|=============================================================================|
|    0     36491  petron  python train.py                            11739MiB |
|    6     41239  petron  python /home/datadisk2/petron/anaconda3...   203MiB |
|    7     37694  petron  python train_student.py --model_name wa...  7685MiB |
+-----------------------------------------------------------------------------+
```

* As a python module

```python
from nvsmi import NVLog

log = NVLog()

# Access attributes
print(log['version']))
print(log['Attached GPUs']['GPU 00000000:04:00.0']['Processes'][0]['Used GPU Memory'])

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
