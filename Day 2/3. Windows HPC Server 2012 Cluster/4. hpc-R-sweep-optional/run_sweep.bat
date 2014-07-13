set sact=YOUR_ACCOUNT
set skey=YOUR_STORAGE_KEY

set taskId=%1
set python=C:\Python27\python.exe
set R="D:\Program Files\R\R-3.0.1\bin\Rscript.exe" --no-restore --no-save

%python% download_chunk.py %sact% %skey% bnames %taskId%
%R% top100.r %taskId%
%python% upload_chunk.py %sact% %skey% bnames %taskId%
