#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 19:57:54 2019

@author: jmcleod
"""

import matplotlib.pyplot as plt
import Diffusion as df


class DOI_Model(object):
    def __init__(self,N=500,beta=0.09,gamma=0.01,max_time=250):
        self.potential_history=[]
        self.adoption_history=[]
        self.disposal_history=[]
        
        self.N=N
        self.beta=beta
        self.gamma=gamma
        self.max_time=max_time
        self.timespan=range(max_time)
        
        self.pop = df.Population(N,beta,gamma)
    
    def __str__(self):
        msg= 'DOI_Model: %d, %8.2f, %8.2f, %d' %(self.N,self.beta,self.gamma,self.max_time)
        return msg
    
    def run(self):
        for time in self.timespan:
            # tracking changes
            self.potential_history.append(self.pop.num_potentials)
            self.adoption_history.append(self.pop.num_adopters)
            self.disposal_history.append(self.pop.num_disposers)
            
            # model population actions
            self.pop.model_adoption()
            self.pop.model_disposal()
    def plot(self):
        #plot results
        plt.plot(self.timespan,self.potential_history,'-b',label='Potential')
        plt.plot(self.timespan,self.adoption_history,'-g',label='Adopters')
        plt.plot(self.timespan,self.disposal_history,'-r',label='Disposers')
        
        plt.title('Diffusion of Innovation with random mixing')
        plt.xlabel('Time')
        plt.ylabel('Adoption Rate')
        
        plt.ylim(0,self.pop.N) #potential error here
        plt.legend(title='key',loc='center right')
        plt.show()
        
def main():
    model = DOI_Model(N=10000,beta=0.003,gamma=0.008,max_time=1000)
    model.run()
    model.plot()

if __name__=='main':
    main()

main()
#%%