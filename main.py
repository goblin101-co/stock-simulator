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
credit_card=1000
stock_options=["APPLE","GOOGLE","NVIDIA"]
stock_options2=["NINTENDO","TESLA","LOGITECH"]
stock_options3=["SAMSUNG","MICROSOFT","FACEBOOK"]
print("WELCOME TO THE STOCK MARKET")
name=input(("enter your name: "))
print("welcome to the stock simulator!")
print(str(name)+": "+str(amount_money))
print("By Goblin101 and a special thanks to Gravityloops for testing this game you can find him on twitch under Gravityloops")
m=int(input("enter the amount of days that you want to spend on the market: "))
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
  print(player_menu) # menu created separately
  r=input("enter 'buy' if you want to buy some stocks, or 'shop' if you want to purchase other things: ")
  if r=='buy':
    print("great here are all of the amazing stock that you can buy")
    print(str(g)+" $"+str(a)+" "+str(h)+" $"+str(d)+" "+str(t)+" $"+str(f))
    print("enter the name of the stock that you want to buy: ")
    c=input()
    if c=="APPLE" or c=="GOOGLE" or c=="NVIDIA":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(a*p)
      buy_stock(c,p,a)
      total_num_of_stock=total_num_of_stock+p
      print("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    elif c=="NINTENDO" or c=="TESLA" or c=="LOGITECH":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(d*p)
      buy_stock(c,p,d)
      total_num_of_stock=total_num_of_stock+p
      print("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    elif c=="SAMSUNG" or c=="MICROSOFT" or c=="FACEBOOK":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(f*p)
      buy_stock(c,p,f)
      total_num_of_stock=total_num_of_stock+p
      print("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    x=input("do you want to sell any of your stock? write y, n: ")
    if x=='y':
      print("ok")
      z=str(input("which stock do you wish to sell?: "))
      if z=="APPLE" or z=="GOOGLE" or z=="NVIDIA":
        view_stock(z,p,round(a3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,a2)
        amount_money=amount_money+(y*a2)
      elif z=="NINTENDO" or z=="TESLA" or z=="LOGITECH":
        view_stock(z,p,round(d3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,d2)
        amount_money=amount_money+(y*d2)
      elif z=="SAMSUNG" or z=="MICROSOFT" or z=="FACEBOOK":
        view_stock(z,p,round(f3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(z,y,f2)
        amount_money=amount_money+(y*f2)
    if x=='n':
      print("ok")
      q=input(("ok the day is over press ENTER to go to the next day: "))
      if q=='':
        print("ok see you tommorrow")
        days=days-1
        clear_screen()
  if days==0:
    print("You have no more days left we hope to see you again soon")
    exit()
  if amount_money<=0 and total_num_of_stock>0:
    print("You are bankrupt sell your stock to buy more")
  if amount_money<=0 and total_num_of_stock==0:
    print("you are fully bankrupt, and your portfolio is completely empty, thank you for playing! GAME OVER :'(")
    exit()
  if r=='shop':
    print("1. Credit cards 2. ")
    # finish the API part first, and then add smaller features that are easy to add.