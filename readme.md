To run the following chatbox you must have the following modules installed. 

- pip install customtkinter
- winget install --id Cloudflare.cloudflared
- pip install keyboard

To access the server you must use the following command in your terminal

For Host Side
- cloudflared tunnel --url tcp://localhost:65432
*Using the command above will generate you a temporary cloudflare link(url) which can make your localhost server exposed to public*

For client side
- cloudflared access tcp --hostname <YOUR-URL-HERE> --url tcp://127.0.0.1:65432
You have to remove the https:// from the url you acquired


----------------ChangeLogs----------------
3/3/2026
- Able to chat with other people
- Able to host server 
- Command logs
- You can now press ' to focus on chat window

2/18/2026 
- Chat window 

2/20/2026
- Automatic Transparency Chatwindow
- Transparent background
- Made the window smaller
- You can now use commands

2/21/2026
- can now send colored text using {color_name} text
