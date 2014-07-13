
set nTasks=%1

for /L %%A IN (1,1,%nTasks%) DO (
  AzureBlobCopy -Action Download -BlobContainer output -LocalDir . -FileName banana%%A%.mat
)

postprocess_parallel_banana_sweep.exe %nTasks%

