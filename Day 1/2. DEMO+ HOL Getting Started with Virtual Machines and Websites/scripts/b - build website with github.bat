:: Download azure publishsettings
azure account download
:: Import downloaded file
azure account import {path to .publishsettings file}
:: Set account (if different to account that is set by default
azure account set {account}

azure site create MySite --github --githubusername username --githubpassword password --githubrepository githubuser/reponame

:: To deploy branch
azure site repository branch <branch> <site>

