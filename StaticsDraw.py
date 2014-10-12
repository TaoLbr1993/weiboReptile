from __future__ import division
import pylab as pl
import pickle
import os
import pylab as pl
def staticsDraw():
    if not os.path.exists('statics.data'):
        print 'Error!\nNo statics file found'
        raise IOError
    else:
        sfile=open('statics.data','r')
        statics=pickle.load(sfile)
        y_speed=[0]*48
        x_print=['']*48
        x_time=[0]*48
        for i in range(48):
            y_speed=statics['pages'][i]/statics['time'][i]
            x_time[i]=i
            if i%4==0:
                x_print[i]=str(i//4)
            else:
                x_print[i]=''
        
        pl.plot(x_time,y_speed)
        pl.xticks(x_time,x_print,color='red')
        pl.grid(True)
        pl.savefig('stiatics.png')
        pl.show()
        
def getSpeed():
    if not os.path.exists('statics.data'):
        print 'Error!\nNo statics file found'
        raise IOError
    else:
        sfile=open('statics.data','r')
        statics=pickle.load(sfile)
        y_speed=[0]*48  
        for i in range(48):
            y_speed[i]=statics['pages'][i]/statics['time'][i]
            print y_speed[i]
            
if __name__=="__main__":
    staticsDraw()