import random
import stock_dict
from stock_dict import buy_stock
from stock_dict import sell_stock
from stock_dict import stocks
from stock_dict import view_stock
import text
from text import clear_screen
from text import display_letter_by_letter
amount_money=100000
total_num_of_stock=0
days=0
stock_options=["APPLE","GOOGLE","NVIDIA"]
stock_options2=["NINTENDO","TESLA","LOGITECH"]
stock_options3=["SAMSUNG","MICROSOFT","FACEBOOK"]
display_letter_by_letter("WELCOME TO THE STOCK MARKET")
name=input("enter your name: ")
display_letter_by_letter("welcome to the betting simulator!")
display_letter_by_letter(str(name)+": "+str(amount_money))
display_letter_by_letter("By Goblin101 and a special thanks to Gravityloops for testing this game you can find him on twitch under Gravityloops")
m=int(input("enter the amount of days that you want to spend on the market: "))
days=days+m
while True:
  a=random.randrange(0,6000) # stock option 1 price
  d=random.randrange(0,6000) # stock option 2 price
  f=random.randrange(0,6000) # stock option 3 price
  a2=random.randrange(0,6000) # stock option 1 price new
  d2=random.randrange(0,6000) # stock option 2 price new
  f2=random.randrange(0,6000) # stock option 3 price new
  a3=((a2-a)/a)*100
  d3=((a2-a)/a)*100
  f3=((a2-a)/a)*100
  g=random.choices(stock_options)
  h=random.choices(stock_options2)
  t=random.choices(stock_options3)
  display_letter_by_letter("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
  r=input("enter buy if you want to buy stock or 'start hacking' for something crazy to happen but be ware you could lose everything: ")
  if r=='buy':
    display_letter_by_letter("great here are all of the amazing stock that you can buy")
    display_letter_by_letter(str(g)+" $"+str(a)+" "+str(h)+" $"+str(d)+" "+str(t)+" $"+str(f))
    display_letter_by_letter("enter the name of the stock that you want to buy: ")
    c=input()
    if c=="APPLE" or c=="GOOGLE" or c=="NVIDIA":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(a*p)
      buy_stock(c,p,a)
      total_num_of_stock=total_num_of_stock+p
      display_letter_by_letter("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    elif c=="NINTENDO" or c=="TESLA" or c=="LOGITECH":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(d*p)
      buy_stock(c,p,d)
      total_num_of_stock=total_num_of_stock+p
      display_letter_by_letter("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    elif c=="SAMSUNG" or c=="MICROSOFT" or c=="FACEBOOK":
      p=int(input("enter the number you want to buy of the stock: "))
      amount_money=amount_money-(f*p)
      buy_stock(c,p,f)
      total_num_of_stock=total_num_of_stock+p
      display_letter_by_letter("num of stocks: "+str(total_num_of_stock)+" amount of money: $"+str(amount_money)+" amount of days: "+str(days))
    x=input("do you want to sell any of your stock? write y, n or just press ENTER: ")
    if x=='y':
      display_letter_by_letter("ok")
      display_letter_by_letter(stocks)
      z=str(input("which stock do you wish to sell?: "))
      if z=="APPLE" or z=="GOOGLE" or z=="NVIDIA":
        view_stock(c,p,round(a3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(c,y,a2)
        amount_money=amount_money+(y*a2)
      elif z=="NINTENDO" or z=="TESLA" or z=="LOGITECH":
        view_stock(c,p,round(d3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(c,y,d2)
        amount_money=amount_money+(y*d2)
      elif z=="SAMSUNG" or z=="MICROSOFT" or z=="FACEBOOK":
        view_stock(c,p,round(f3,2))
        y=int(input("enter the number of shares that you want to sell: "))
        total_num_of_stock=total_num_of_stock-y
        sell_stock(c,y,f2)
        amount_money=amount_money+(y*f2)
    if x=='n':
      display_letter_by_letter("ok")
      q=input("ok the day is over press ENTER to go to the next day: ")
      if q=='':
        display_letter_by_letter("ok see you tommorrow")
        days=days-1
  if days==0:
    display_letter_by_letter("You have no more days left we hope to see you again soon")
    exit()
  if amount_money<=0 and total_num_of_stock>0:
    display_letter_by_letter("You are bankrupt sell your stock to buy more")
  if amount_money<=0 and total_num_of_stock==0:
    display_letter_by_letter("you are fully bankrupt thank you for playing GAME OVER :'(.....wait there is one more option, you could sell a few things")
    final=str(input("enter y or n: "))
    if final=='y':
      amount_money=amount_money+1000000
    if final=='n':
      exit()
  if r=='start hacking':
    hack=random.randrange(-2,2)
    amount_money=amount_money*hack
  yoink=random.randrange(1, days)
  if days==yoink:
    amount_money=amount_money-(amount_money/4)
    display_letter_by_letter("You lost a quarter of your money in a data leak :( I know this seems bad but this is the perfect time to get back and start trading again")
  clear_screen()