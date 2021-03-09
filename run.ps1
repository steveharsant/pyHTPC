$configPath = "$PSscriptRoot/config.json"

if (Test-Path -Path $configPath) {
  Write-Output 'Loading config.json'
}
else {
  Write-Error 'json.config file not found. Failed to boot thea. exit 10'
  exit 10
}

$config = Get-Content -Path $configPath | ConvertFrom-Json

Set-Location $config.startup.install_directory

if ($config.startup.force_venv -eq 'true') {
  # Install venv if not already installed and activate
  pip install virtualenv
  virtualenv venv
  .\venv\Scripts\activate

  # Install dependencies
  $dependencies = 'flask'
  foreach ($dependency in $dependencies) {
    pip install $dependency
  }
}

if ($config.startup.kiosk_mode -eq 'true') {
  $kiosk = '--kiosk'
}

&"$($config.startup.browser)" $kiosk 127.0.0.1:5000
python.exe "$($config.startup.install_directory)\app.py"
