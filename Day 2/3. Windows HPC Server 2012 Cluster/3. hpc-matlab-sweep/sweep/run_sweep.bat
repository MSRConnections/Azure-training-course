

set delta=%1
set xmin=%2
set xmax=%3
set ymin=%4
set ymax=%5
set nTasks=%6
set taskID=%7

set outfile=banana%taskID%.mat

parallel_banana_sweep.exe %delta% %xmin% %xmax% %ymin% %ymax% %nTasks% %taskID%

AzureBlobCopy -Action Upload -BlobContainer output -LocalDir . -FileName %outfile%

