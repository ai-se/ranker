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

def sdiv(lst, attr=None,tiny=None,cohen=None,small=None,
         x=lambda z:z[0], y=lambda z:z[-1],better=gt):
  "Divide lst of (x,y) using variance of y."
  tiny = tiny or The.sdiv.tiny
  cohen= cohen or The.sdiv.cohen
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

