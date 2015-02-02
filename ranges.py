"""
sdiv: standard-division of numerics .
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved. 
      _____                                _______
    ,/_    ``-._                          /       \ 
   ,|:          `'-..__               ___|         |_
  ,|:_                 ``'''-----''''`_::~-.......-'~\ 
 ,|:_                                 _:    . ' .    :
 |:_                                  _:  .   '   .  |
 |:_                                  _:  '   .   '  |
 |:_                                  _:    ' . '    :
 |:_                    __,,...---...,,:_,.-'''''-.,_/
 |:_              _,.-``                 |         |
 |:_           ,-`                       |         |
 |:_         ,`                          |         |
 `|:_      ,'                            |         |
  |:_     /                              |         |
  `|:_   /                               |         |
   `|:_ :                                |         |
     \: |                                |         |
      \:|                                |         | cjr
       ~                                             

""" 

from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode = True
from rangesLib import *

def sdiv(lst, attr=None,tiny=3,cohen=0.3,small=None,
         x=lambda z:z[0], y=lambda z:z[-1],better=gt):
  "Divide lst of (x,y) using variance of y."
  #----------------------------------------------
  def divide(this,small): #Find best divide of 'this'
    lhs,rhs = Counts(), Counts(y(z) for z in this)
    n0, score, cut,mu = 1.0*rhs.n, rhs.sd(), None,rhs.mu
    for j,one  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
        if better(maybe,score) :  
          if abs(lhs.mu - rhs.mu) >= small:
            cut,score = j,maybe
      rhs - y(one)
      lhs + y(one)    
    return cut,mu,score,this
  #----------------------------------------------
  def recurse(this, small,cuts):
    cut,mu,sd,part0 = divide(this,small)
    if cut: 
      recurse(this[:cut], small, cuts)
      recurse(this[cut:], small, cuts)
    else:   
      cuts += [Range(attr = attr,
                     x    = o(lo=x(this[0]), hi=x(this[-1])),
                     y    = o(mu=mu, sd=sd),
                     rows = this)]
    return cuts
  #---| main |-----------------------------------
  small = small or Counts(y(z) for z in lst).sd()*cohen
  if lst: 
    return recurse(sorted(lst,key=x),small, [] )

def _sdiv():
  "Demo code to test the above."
  import random
  bell= random.gauss
  random.seed(1)
  def go(lst,cohen=0.3,
         x=lambda x:x[0],
         y=lambda x:x[1]):
    print("\n",sorted(lst)[:10],"...")
    for d in  sdiv(lst,cohen=cohen,num1=num1,num2=num2):
      print(d[1][0][0])
  l = [ (1,10), (2,11),  (3,12),  (4,13),
       (20,20),(21,21), (22,22), (23,23), (24,24),
       (30,30),(31,31), (32,32), (33,33),(34,34)]
  go(l,cohen=0.3)
  go(map(lambda x:(x[1],x[1]),l))
  ten     = lambda: bell(10,2)
  twenty  = lambda: bell(20,2)
  thirty  = lambda: bell(30,2)
  l=[]
  for _ in range(1000): 
    l += [(ten(),   ten()), 
          (twenty(),twenty()),
          (thirty(),thirty())]
  go(l,cohen=0.5)
  
if __name__ == '__main__': _sdiv()

"""
Output:

[ (1, 10),  (2, 11),  (3, 12),  (4, 13), 
 (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), 
 (30, 30)] ...
1
20
30

[(3.7000699679075257, 13.718816007599141), 
 (3.815015386011323, 7.222657539933019), 
 (4.207498112954239, 10.56596537668784), 
 (4.328418426639925, 9.920222370615866), 
 (4.715076966608875, 10.343126948569484), 
 (4.78790689427217, 8.306688616563584), 
 (5.013513775695802, 6.965741666232676), 
 (5.030668572838251, 8.546550180016057), ...] ...
3.70006996791
14.9850387857
25.6550191106

"""
