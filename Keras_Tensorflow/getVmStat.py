# import os

# os.system(vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f Mi\n", "$1:", $2 * $size / 1048576)')

import psutil

print('The CPU usage is: ', psutil.cpu_percent(4))
