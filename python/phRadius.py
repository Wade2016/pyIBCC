'''
Analysis of IBCC performance on  Planet Hunters, breaking the data down by radius.

Created on 12 May 2014

@author: edwin
'''

import numpy as np
import matplotlib.pyplot as plt
import ibccperformance as ip
import logging

def weightedVoteSchwamb(crowdLabels,goldAll,goldTypes,label):
    kIdxs = np.unique(crowdLabels[:,0])
    
    nCorrect = np.zeros(len(kIdxs))
    totalSeen = np.zeros(len(kIdxs))
    detection = np.zeros(len(goldAll))
    nClassifiers = np.zeros(len(goldAll))
    for l in range(crowdLabels.shape[0]):
        if l not in testIdxs:
            
            k = int(crowdLabels[l,0])
            i = int(crowdLabels[l,1])
                    
            if goldAll[i]==1:
                nCorrect[k] += crowdLabels[l,2]==0 
                totalSeen[k] += 1
                detection[i] += crowdLabels[l,2]==0 
                nClassifiers[i] += 1
        else:
            i = int(crowdLabels[l,1])
            nClassifiers[i] +=1
                
    print 'Fraction of candidates with >=5 classifications: ' + \
            str(float(np.sum(nClassifiers>=5))/float(len(goldAll)))
                
    detection = np.divide(detection, nClassifiers)
    errors = np.zeros(len(kIdxs)) 
    for l in range(crowdLabels.shape[0]):
        if l not in testIdxs:
            k = int(crowdLabels[l,0])
            i = int(crowdLabels[l,1])
            if goldAll[i]==1:  
                errors[k] += 0.2*detection[i]* (crowdLabels[l,2]==1)
    totalSeen[totalSeen==0] = 1
    weights = np.ones(len(kIdxs)) + nCorrect - errors 
    weights = weights+np.min(weights)
    weights = np.divide(weights, np.max(weights))
    
    pTVote = np.ones(pT.shape)
    for l in range(crowdLabels.shape[0]):
        i = int(crowdLabels[l,1])
        k = int(crowdLabels[l,0])
        v = crowdLabels[l,2]==0
        if v:
            pTVote[i,1]+=weights[k]
        else:
            pTVote[i,0]+=weights[k]
    pTVote = np.divide(pTVote, np.sum(pTVote,axis=1).reshape(pTVote.shape[0],1))
    plotRecallByRadius(pTVote, goldTypes, testIdxs, goldAll, label)

def plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label):

    tVals = [3, 4, 5, 6, 7, 10, 16]
    start = 2
    
    totalNs = np.zeros(len(tVals))
    recall = np.zeros(len(tVals))
    cumRecall = np.zeros(len(tVals))
    
    for i,t in enumerate(tVals):
        #find the boolean array of test indexes indicating this type
        thisType = np.bitwise_and(goldTypes<t, goldTypes>=start)
        thisType = thisType[testIdxs]
        #Find the test indexes of the current type 
        idxs = testIdxs[thisType]
        if len(idxs)==0:
            logging.warning("No test idxs found with radius between " + str(start) + ' and ' + str(t))
            continue
                
        if i+1<len(tVals) and tVals[i+1]>t:
            start = t
        
        pT_t = pT[idxs,:]
        greedyLabels = np.round(pT_t[:,1])
        gold_t = goldAll[idxs]
        pos_t = gold_t==1
        
        tp = float(np.sum(greedyLabels[pos_t]==1))
        fn = float(np.sum(greedyLabels[pos_t]<1))
        recall[i] = tp/(tp+fn)
        
        totalNs[i] = tp+fn
        
        print "Recall for type " + str(t) + " is " + str(recall[i])
        cumRecall[i] = np.sum(np.multiply(recall[0:i+1], totalNs[0:i+1]))/np.sum(totalNs[0:i+1])
        #print "Cum Recall for type " + str(t) + " is " + str(cumRecall[i])
                
    plt.figure(figure7)
    plt.plot(tVals, recall, label=label)
    plt.legend()
    plt.xlabel('Radius/Earth Radii')
    plt.ylabel('Recall')
    plt.title('Recall of Planet Transit Simulations by Radius')
    plt.hold(True)
    plt.grid(which="minor")
    
    ip.write_img("recallbyradius_" + label, 7)
    
    plt.figure(figure8)
    plt.xlabel('Radius/Earth Radii')
    plt.ylabel('Recall')
    plt.title('Recall of Planet Transit Simulations with Radius Greater than Indicated')
    plt.plot(tVals ,cumRecall, label=label)
    plt.legend()
    plt.grid(which="minor")
    
    ip.write_img("recallbyradiusgreater_" + label, 8)
    
def printMajorityVoteByType(pT, goldTypes, testIdxs, goldAll):
    tVals = [3, 4, 5, 6, 7, 10, 16]
    start = 2      
       
    for i,t in enumerate(tVals):
        
        thisType = np.bitwise_and(goldTypes<t, goldTypes>=start)
        idxs = testIdxs[thisType[testIdxs]]
        pT_t = pT[idxs,:]
        greedyLabels = np.round(pT_t[:,1])
        start = t
        hits = np.zeros(len(thisType))
        seenBy = np.zeros(len(thisType))
        for l in range(crowdLabels.shape[0]):
            idx = int(crowdLabels[l,1])
            if crowdLabels[l,2]==0:
                hits[idx] += float(1)
            seenBy[idx] += float(1)
            
        nThisType = float(len(hits[thisType]))
        nWithPos = np.sum(hits[thisType]>0) 
        print nWithPos
        print nThisType
        print nWithPos/nThisType    
        majorities = np.divide(hits[thisType], seenBy[thisType])>0.5
        nMajorities = np.sum(majorities)
        print nMajorities  
        print nMajorities / nThisType
        if i==5:
            bigPlanetIds = idxs[greedyLabels==0]
             
    return bigPlanetIds    
  
plt.close('all')

plt.figure()
plt.figure()
plt.figure()
ip.figure1 = 1
ip.figure2 = 2
ip.figure3 = 3

plt.figure(7)
figure7 = 7
plt.figure(8)
figure8 = 8

# #TEST SET 1: Q1 Real Data Performance -- put that in the title
# #only the real q1 data
#label = "unsup. learning on real"
#ip.testUnsupervised('./python/config/ph_q1_uns.py', label, "Confirmed Planets")

# #real data plus sims. Evaluate on real
#label = "unsup. learning with real+sim"
#ip.testUnsupervised('./python/config/ph_q1_uns_plussims.py', label, "Confirmed Planets")

# #real data plus sims. Eval on real. Sims as training.
label = "sims as training"
pT,goldTypes,testIdxs,goldAll,crowdLabels,origCandIds = ip.testSupervised(\
                      './python/config/ph_q1_supe_plussims.py', label, "Confirmed Planets")
plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)

#TEST SET 1+: Q1 Real Data Performance, IBCC divides peoples' reliability by radius group
  
# ADD IN ANOTHER METHOD FOR COMPARISON.
# REPEAT THE 50% SIMS METHOD MULTIPLE TIMES IF NOT DONE ALREADY?
  
label = "simulations as training, radius split"
pT,goldTypes,testIdxs,goldAll,crowdLabels,origCandIds = ip.testSupervised(\
                           './python/config/ph_q1_supe_plussims_rad.py', label, eval=False)
pTsum = np.concatenate( (pT[:,0].reshape(pT.shape[0],1),\
                          np.sum(pT[:,1:],1).reshape(pT.shape[0],1)), axis=1)
plotRecallByRadius(pTsum, goldTypes, testIdxs, goldAll, label)

#########################################################################

plt.figure()
plt.figure()
plt.figure()
ip.figure1 = 4
ip.figure2 = 5
ip.figure3 = 6
 
#TEST SET 2: Q1 Simulated Data Performance, all models learned using simulated and real crowd data.
#real data plus sims, evaluate only on sims 
label = "unsup. learning with real+sim"
pT,goldTypes,testIdxs,goldAll = ip.testUnsupervised(\
                                    './python/config/ph_q1_uns_sims.py', label)
plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)

#sims only
label = "unsup. learning with sims only"
pT,goldTypes,testIdxs,goldAll = ip.testUnsupervised(\
                                    './python/config/ph_q1_uns_simsonly.py', label)#sims only, evaluate on sims
plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)

#real data plus sims. Eval on half of sims, other half as training.
label = "real+sim, 50% sims as training"
pT,goldTypes,testIdxs,goldAll,_,_ = ip.testSupervised(\
                                './python/config/ph_q1_supe_sims.py', label)
plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)

#simulated data only, using 50% as training
label = "sims only, 50% sims as training"
pT,goldTypes,testIdxs,goldAll,crowdLabels,origCandIds = ip.testSupervised(\
                                './python/config/ph_q1_supe_simsonly.py', label)
plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)
  
#TEST SET 2+: Simulated Data Performance, IBCC divides reliability by radius
# #real data plus sims. Eval on half of sims, other half as training.
label = "real+sim, 50% sims as training, radius split"
pT,goldTypes,testIdxs,goldAll,crowdLabels,origCandIds = ip.testSupervised(\
                               './python/config/ph_q1_supe_sims_rad.py', label, eval=False)
pTsum = np.concatenate( (pT[:,0].reshape(pT.shape[0],1),\
                          np.sum(pT[:,1:],1).reshape(pT.shape[0],1)), axis=1)
plotRecallByRadius(pTsum, goldTypes, testIdxs, goldAll, label)

###########################################################################

#From test set 1+, removed because we don't test radius split in unsupervised mode 
#real data plus sims. Evaluate on real -- unsupervised doesn't make sense with radius split
# label = "unsup. learning with real+sim, radius split"
# ip.testUnsupervised('./python/config/ph_q1_uns_plussims_rad.py', label)

#real data plus sims. Eval on real. Sims as training.
  
#From test set 2+, see above 
#real data plus sims, evaluate only on sims 
# label = "unsup. learning with real+sim, radius split"
# pT,goldTypes,testIdxs,goldAll = ip.testUnsupervised(\
#                                     './python/config/ph_q1_uns_sims_rad.py', label)
# plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)  
  
#########################################################################    
  
# ip.plotCumDist(pTsum,2,testIdxsReal,goldAll, label)        
# acc,recall,spec,prec,auc,ap = \
#     ip.getAccMeasures(pTsum,goldAll,2,testIdxsReal)

#remove the real ones from the testIdxs
# goldAll[testIdxsReal]  = -1
#  
# testIdxs = np.setdiff1d(testIdxs, testIdxsReal, True)
#  
# goldAll[goldAll>1] = 1
# ip.plotCumDist(pTsum,2,testIdxs,goldAll, label)        
# acc,recall,spec,prec,auc,ap = \
#     ip.getAccMeasures(pTsum,goldAll,2,testIdxs)
# plotRecallByRadius(pT, goldTypes, testIdxs, goldAll, label)