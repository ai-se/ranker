from __future__ import division,print_function
import sys,random,time
sys.dont_write_bytecode = True

import housing,ranges
from rangesLib import *

# add in scorerd. abcd mre, lift

def g(x): return ('%g' % x)

def _rangeLib(seed=1):
  print("\n######################")
  pretty(The)
  print("\n#",time.strftime('%Y/%m/%d/ %H:%M:%S'))
  random.seed(seed)
  def show(n,rule):
    print(n,g(rule.score),rule)
    #print(n,sorted(map(lambda z:z.id,rule.rows)))  
  t=housing.housing() 
  b4=Counts(map(lambda l:l.score,t.data))
  print(b4.mu) 
  r=[]
  for i  in t.indep: 
    more=ranges.sdiv(t.data,attr=t.names[i],
              tiny=The.ranker.tiny,
              x=lambda z:z[i],
              y=lambda z:z.score,
              small=The.ranker.small)
    print(t.names[i],len(more) )
    if len(more) > 1:
        r += more 
  #r = sorted(r,key=lambda z : z.y.mu*-1)
  for one in r:
    if one.y.mu > b4.mu:   
      print(one,o(mu=g(one.y.mu),sd=g(one.y.sd)), '<==',o(b4=g(b4.mu),sd0=g(b4.sd())))
  #exit()   
  rules =map(lambda z:Rule([z],z.rows),r)
  most=b4.mu
  n=0 
  for _ in xrange(The.ranker.retries):
    rules = sorted(rules,key=lambda z: z.score)[-1*The.ranker.beam:]
    for i in xrange(The.ranker.repeats): 
      n+=1
      rule1  = random.choice(rules)
      rule2  = random.choice(rules) 
      rule3 = rule1+rule2
      if rule3 and The.ranker.enough(rule3.rows,t.data) and rule3.score > most:
        most = rule3.score 
        print("")
        print(n,most,int(100*most/b4.mu))
        show(1,rule1)
        show(2,rule2)
        show(3,rule3)
        rules += [rule3]
  print("\n",n,sorted(rules,key=lambda z: z.score)[-1])
  
if __name__ == "__main__":
    _rangeLib()