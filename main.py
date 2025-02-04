import random
import stock_buy
from stock_buy import buy_stock
from stock_buy import sell_stock
from stock_buy import view_stock
import menu
from menu import amount_money
from menu import total_num_of_stock
from menu import days
from menu import player_menu
import text
from text import clear_screen
from text import typewriter_effect
from text import typewriter_input
credit_card=1000
stock_options=["APPLE","GOOGLE","NVIDIA"]
stock_options2=["NINTENDO","TESLA","LOGITECH"]
stock_options3=["SAMSUNG","MICROSOFT","FACEBOOK"]
typewriter_effect("WELCOME TO THE STOCK MARKET", 0.05)
name=typewriter_input(("enter your name: "))
typewriter_effect("welcome to the stock simulator!", 0.05)
typewriter_effect(str(name)+": "+str(amount_money))
typewriter_effect("By Goblin101 and a special thanks to Gravityloops for testing this game you can find him on twitch under Gravityloops", 0.05)
m=int(typewriter_input("enter the amount of days that you want to spend on the market: "))
days=days+m
while True:
  a=random.randrange(0,600) # stock option 1 price
  d=random.randrange(0,600) # stock option 2 price
  f=random.randrange(0,600) # stock option 3 price
  a2=random.randrange(0,600) # stock option 1 price new
  d2=random.randrange(0,600) # stock option 2 price new
  f2=random.randrange(0,600) # stock option 3 price new
  a3=((a2-a)/a)*100
  d3=((a2-a)/a)*100
  f3=((a2-a)/a)*100
  g=random.choices(stock_options)
  h=random.choices(stock_options2)
  t=random.choices(stock_options3)
  typewriter_effect(player_menu, 0.05) # menu created separately
  r=typewriter_input("enter 'buy' if you want to buy some stocks, or 'shop' if you want to purchase other things: ")
  if r=='buy':
    typewriter_effect("great here are all of the amazing stock that you can buy", 0.05)
    typewriter_effect(str(g)+" $"+str(a)+" "+str(h)+" $"+str(d)+" "+str(t)+" $"+str(f), 0.05)
    typewriter_effect("enter the name of the stock that you want to buy: ", 0.05)
    c=typewriter_input()
    if c=="APPLE" or c=="GOOGLE" or c=="NVIDIA":
      p=int(typewriter_input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(a*p)
      buy_stock(c,p,a)
      total_num_of_stock=total_num_of_stock+p
      typewriter_effect(player_menu, 0.05)
    elif c=="NINTENDO" or c=="TESLA" or c=="LOGITECH":
      p=int(typewriter_input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(d*p)
      buy_stock(c,p,d)
      total_num_of_stock=total_num_of_stock+p
      typewriter_effect(player_menu, 0.05)
    elif c=="SAMSUNG" or c=="MICROSOFT" or c=="FACEBOOK":
      p=int(typewriter_input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(f*p)
      buy_stock(c,p,f)
      total_num_of_stock=total_num_of_stock+p
      typewriter_effect(player_menu, 0.05)
    x=typewriter_input("do you want to sell any of your stock? write y, n: ")
    if x=='y':
      typewriter_effect("ok", 0.05)
      z=str(typewriter_input("which stock do you wish to sell?: "))
      if z=="APPLE" or z=="GOOGLE" or z=="NVIDIA":
        view_stock(z,p,round(a3,2))
        y=int(typewriter_input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,a2)
        amount_money=amount_money+(y*a2)
      elif z=="NINTENDO" or z=="TESLA" or z=="LOGITECH":
        view_stock(z,p,round(d3,2))
        y=int(typewriter_input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,d2)
        amount_money=amount_money+(y*d2)
      elif z=="SAMSUNG" or z=="MICROSOFT" or z=="FACEBOOK":
        view_stock(z,p,round(f3,2))
        y=int(typewriter_input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,f2)
        amount_money=amount_money+(y*f2)
    if x=='n':
      typewriter_effect("ok", 0.05)
      q=typewriter_input(("ok the day is over press ENTER to go to the next day: "))
      if q=='':
        typewriter_effect("ok see you tommorrow", 0.05)
        days=days-1
        clear_screen()
  if days==0:
    typewriter_effect("You have no more days left we hope to see you again soon", 0.05)
    exit()
  if amount_money<=0 and total_num_of_stock>0:
    typewriter_effect("You are bankrupt sell your stock to buy more", 0.05)
  if amount_money<=0 and total_num_of_stock==0:
    typewriter_effect("you are fully bankrupt, and your portfolio is completely empty, thank you for playing! GAME OVER :'(", 0.05)
    exit()
  if r=='shop':
    typewriter_effect("1. Credit cards 2. ", 0.05)

# Add documentation to this file