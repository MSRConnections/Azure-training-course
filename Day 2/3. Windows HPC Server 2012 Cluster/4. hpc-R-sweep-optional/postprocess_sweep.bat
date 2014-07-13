set sact=YOUR_ACCOUNT
set skey=YOUR_STORAGE_KEY

set nTasks=%1
set python=C:\Python27\python.exe
set R="C:\Program Files\R\R-3.0.1\bin\Rscript.exe" --no-restore --no-save

for /L %%A IN (1,1,%nTasks%) DO (
  %python% download_chunk.py %sact% %skey% bnames %%A%
)

%R% postprocess.r %nTasks%

