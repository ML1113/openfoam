import numpy as np
import matplotlib.pyplot as plt


def main():
    binWidth = 0.033
    cord = 0.034
    span = 0.05
    umean = 0.0974
    umeanExp = 0.1011
    ustarExp = 0.0840
    ustarExpsqr = ustarExp*ustarExp
    umeanExpsqr = umeanExp*umeanExp
    umeansqr = umean*umean
    scaleExp = ustarExpsqr/umeanExpsqr
    density = 1168
    StartAverage = 11.0
    Period = 2.0
    
    CdPhaseA =  np.zeros(int(round(Period/binWidth))+1)
    ClPhaseA =  np.zeros(int(round(Period/binWidth))+1)
    countCd  =  np.zeros(int(round(Period/binWidth))+1)
    countCl  =  np.zeros(int(round(Period/binWidth))+1)
    
    plottime = []
    time = 0.0 + binWidth/2.0
    while (time < Period):
        plottime.append(time)
        time += binWidth
        
    plottime.append(time)

    KrishnaCd = "Krishna2018Cd.csv"
    KrishnaCl = "Krishna2018Cl.csv"   
    Cdex = np.genfromtxt(KrishnaCd,comments="#",delimiter=",")
    Clex = np.genfromtxt(KrishnaCl,comments="#",delimiter=",")
    
    forceFile = "postProcessing/forces/force.dat" 
    forces = np.genfromtxt(forceFile,comments="#")
    times = forces[:,0]
    forceX = forces[:,1]
    forceY = forces[:,2]
    Cdrag  = np.divide(np.absolute(forceX),0.5*umeansqr*cord*span*density)
    Clift  = np.divide((forceY),0.5*umeansqr*cord*span*density)
    
    time = 0.0
    bins = []
    bins.append(time)
    
    while(time<times[-1]):
        time += binWidth
        bins.append(time)
        
    timeBins = np.digitize(times, bins, right=False)
    
    CdragSmoothed = np.zeros(len(bins))
    CliftSmoothed = np.zeros(len(bins))
    countLift = np.zeros(len(bins))
    countDrag = np.zeros(len(bins))
    
    for timeBin,Cd,Cl in zip(np.nditer(timeBins),np.nditer(Cdrag),np.nditer(Clift)):
        CdragSmoothed[timeBin]+=Cd
        CliftSmoothed[timeBin]+=Cl
        countLift[timeBin] += 1
        countDrag[timeBin] += 1
        
    countDrag = np.add(countDrag,0.0001)
    countLift = np.add(countLift,0.0001)
    CdragSmoothed = np.divide(CdragSmoothed,countDrag)
    CliftSmoothed = np.divide(CliftSmoothed,countLift)
        
    
    plt.plot(bins,CdragSmoothed,bins,CliftSmoothed)
    plt.ylabel('Cd,Cl [-]')
    plt.xlabel('time [s]')
    plt.savefig('ClCd.png')
    plt.close()
    
    PreviousBin = 0
    
    for time,Cd,Cl in zip(bins,CdragSmoothed,CliftSmoothed):
        if time < StartAverage: continue
        else:
            if time - StartAverage -  PreviousBin >= Period: PreviousBin += Period
            index = int ( (time - StartAverage -  PreviousBin) / binWidth )
            CdPhaseA[index] += Cd  
            ClPhaseA[index] += Cl 
            countCd[index]  += 1.0 
            countCl[index]  += 1.0 
            
    countCd = np.add(countCd,0.0001)
    countCl = np.add(countCl,0.0001)
    CdPhaseA = np.divide(CdPhaseA,countCd) 
    ClPhaseA = np.divide(ClPhaseA,countCl) 

    
    fig, ax = plt.subplots()
    
    plt.plot(plottime,CdPhaseA,plottime,ClPhaseA,Cdex[:,0]*4.,Cdex[:,1]*scaleExp,Clex[:,0]*4.0,Clex[:,1]*scaleExp)
    plt.legend(('Cd Sim','Cl Sim','Cd Exp','Cl Exp'))
    plt.ylabel('Cd,Cl [-]')
    plt.xlabel('time [s]')
    plt.savefig('ClCdPhaseA.png')
        
        
    
    
if __name__== "__main__":
  main()
