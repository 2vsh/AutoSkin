from PIL import Image
from random import randrange,choice
from time import sleep
import requests
import keyboard
import asyncio
from pyppeteer import launch

def promptUser():
    global email
    global password
    global ign
    print("Input your account's email")
    email = input(">")
    print()
    print("Input your account's password")
    password = input(">")
    print()
    print("Input your account's ign")
    ign = input(">")

    print("\nSetting up skinbot with email \""+email+"\" and password \""+password+"\"...\n")

def auth(email,password):
    try:
        authRequest = requests.post("https://authserver.mojang.com/authenticate", json={"agent": {"name": "Minecraft", "version": 1}, "username": email,"password": password}).json()
        bearer = authRequest['accessToken']
        return bearer
    except KeyError:	
        print("Invalid Account!\n")

def skinGen():
    im = Image.open("base.png")
    pixels = im.load()
    for x in range(128):
        for y in range(128):
            try:
                pixel = list(pixels[x,y])
                if pixel == [255, 255, 255, 255]:
                    pixels[x,y] = (randrange(50,255),randrange(10,50),randrange(50,100),randrange(0,255))
                if pixel == [255, 255, 255]:
                    pixels[x,y] = (randrange(50,100),randrange(10,50),randrange(50,100))
            except IndexError:
                pass
    im.save("current.png")
    print("Generated skin!")

def changeSkin():
    global bearer
    current_png = open('current.png', 'rb')
    files = {
        'variant': (None, choice(["slim","classic"])),
        'file': ('current.png', current_png),
    }
    headers = {"Authorization":"Bearer "+auth(email,password)}
    if requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins",headers=headers,files=files).status_code == 200:
        print("Skin Changed!")
    current_png.close()

async def main():
    while True:
        browser = await launch(headless=False) #launch a headed browser
        page = await browser.newPage() #make a new tab
        url = ("https://namemc.com/profile/"+ign).lower()
        await page.goto(url,waitUntil='domcontentloaded') #go to the url 
        await asyncio.sleep(5.5)
        skinGen()
        changeSkin()
        await browser.close() #close browser

promptUser()
asyncio.run(main())