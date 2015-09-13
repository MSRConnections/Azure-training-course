Import-Module Azure
Set-Location .\Images
$context = New-AzureStorageContext -ConnectionString "<Your Container Key Here>"
dir *.* | ForEach-Object { Set-AzureStorageBlobContent -Container "input" -Blob $_.Name -File $_.Name -Context $context -Force }
Set-Location ..\