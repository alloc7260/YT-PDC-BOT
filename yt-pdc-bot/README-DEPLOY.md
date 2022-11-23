# Steps to deploy to Azure:

1) Create App Service & Azure Bot on Azure Portal
2) Open command.txt, copy that command
3) Goto Configuration Setting of App Service, General settings paste that command in Startup Command box and save
4) Goto Overview tab, copy URL
5) Goto Configuration Setting of Azure Bot and paste URL in Messaging endpoint and then add /api/messages to end (Enable Streaming Endpoint and Apply changes)
6) Open config.py file and add Azure Bot - Id & Password there
(you can get them from Configuration Setting of Azure Bot)
7) Open this folder in vscode
(make sure you have signed in with azure account in vscode and loged in to Azure Account extention and also enabled the Azure App Service extention)
8) From side bar goto Azure(Shift+Alt+A), expand your Subscription, expand App Services, right click on your App Service and select Deploy to Web App..
9) Select path of your folder and Deploy
10) For testing goto Test in Web Chat Setting of Azure Bot

## Enjoy with your BOT!

### YouTube Help Video - https://youtu.be/wUsQvRInYcw