# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 12:41:07 2020

@author: Ben
"""
from os import listdir
import matplotlib.pyplot as plt
import getopt
import sys
from numpy import array
from numpy.linalg import norm
from matplotlib.gridspec import GridSpec

def mep_forces(filepath):
    files=listdir(filepath)
    images=0
    for i in files:
        try:
            if int(i)>images:
                images=int(i)
        except ValueError:
            pass
    images+=1
    #avgf, maxf, and minf hold the average, maximum and minimum forces respectively
    #forces are stored as [[value for j in range(total_ionic_steps)] for each intermediate image being optimized]
    avgf=[[] for i in range(images-2)]
    maxf=[[] for i in range(images-2)]
    minf=[[] for i in range(images-2)]
    #rc stores the reaction coordinate for every image (not just the intermediate images)
    #rc structured as: [[]]
    rc=[[] for i in range(images)]
    time=[0.0]
    potim=0.0
    try:
        for i in range(1,images-1):
            with open('./'+str('{:02d}'.format(i))+'/OUTCAR','r') as file:
                counter = 0
                atomnum=0
                tol=0.0
                for line in file:
                    if 'EDIFFG' in line:
                        tol=abs(float(line.split()[line.split().index('EDIFFG')+2]))
                    elif 'POTIM' in line and i in range(1,images-2):
                        potim=float(line.split()[line.split().index('POTIM')+2])
                        if potim==0.0:
                            potim=-1.0
                    elif 'NIONS' in line:
                        atomnum=int(line.split()[line.split().index('NIONS')+2])
                        counter=atomnum+1
                    #in a standard VASP compilation the CHAIN + TOTAL force is plotted
                    #in a VASP compilation with VTST the tangent force is plotted
                    elif 'TOTAL-FORCE' in line:
                        counter=-2
                        tempavg=0.0
                        tempmax=0.0
                        tempmin=1000.0
                        if i==1 and len(avgf[0])!=0:
                            time.append(abs(potim)+time[-1])
                    #parses reaction coordinate output from a typical VASP compilation
                    elif 'left and right image' in line:
                        if i==1:
                            rc[0].append(0.0)
                        rc[i].append(float(line.split()[4])+rc[i-1][-1])
                        if i==images-2:
                            rc[i+1].append(float(line.split()[5])+rc[i][-1])
                    #parses reaction coordinate output from a VASP compilation with VTST
                    elif 'distance to prev, next image' in line:
                        if i==1:
                            rc[0].append(0.0)
                        rc[i].append(float(line.split()[8])+rc[i-1][-1])
                        if i==images-2:
                            rc[i+1].append(float(line.split()[9])+rc[i][-1])
                    elif counter<atomnum and atomnum!=0 and counter>=0 and i in range(1,images-1):
                        neb_force=norm(array([float(line.split()[j]) for j in range(3,6)]))
                        tempavg+=neb_force/atomnum
                        if neb_force>tempmax:
                            tempmax=neb_force
                        elif neb_force<tempmin:
                            tempmin=neb_force
                        if counter==atomnum-1 and i in range(1,images-1):
                            avgf[i-1].append(tempavg)
                            maxf[i-1].append(tempmax)
                            minf[i-1].append(tempmin)
                    counter+=1
    except IOError:
        print('something wrong with subdirectory OUTCAR files')
        sys.exit(1)
    
    for i in range(images):
        for j in range(len(rc[i])):
            rc[i][j]/=max([rc[k][j] for k in range(images)])
    
    #if the time step is 0, like is used to engage the VTST optimizers, the horizontal axis will be in units of ionic steps, not time
    if potim==-1.0:
        time_units='optimization steps'
    else:
        time_units='optimization time / fs'
    
    #plotting
    fig,axs=plt.subplots(images-2,2,gridspec_kw={'width_ratios': [3,1]},sharex=True)
    fig.tight_layout()
    #this sets the figure to an appropriate size for my screen
    fig.set_figheight(8)
    fig.set_figwidth(15)
    gs=GridSpec(images-2,2,width_ratios=(3,1))
    #checks for an exception in the structure of the axes, which occurs when only one mep image is used
    try:
        for ax,i in zip(axs[:,0],range(images-2)):
            ax.tick_params(axis='both',direction='in')
            ax.set(ylabel='image #'+str(i+1))
            if i==images-3:
                ax.set(xlabel=time_units)
            if i==0:
                ax.set(title='force evolution')
            for j,k in zip([maxf[i],minf[i],avgf[i]],['max force','min force','avg force']):
                ax.scatter(time,j,label=k)
            ax.plot([time[0],time[-1]],[tol,tol],linestyle='dashed',label='convergence')
        for ax in axs[:,1]:
            ax.remove()
        ax2=fig.add_subplot(gs[1:,1])
    except IndexError:
        axs[0].tick_params(axis='both',direction='in')
        axs[0].set(ylabel='image #'+str(i+1))
        axs[0].set(xlabel=time_units)
        for j,k in zip([maxf[0],minf[0],avgf[0]],['max force','min force','avg force']):
            axs[0].scatter(time,j,label=k)
        axs[0].plot([time[0],time[-1]],[tol,tol],linestyle='dashed',label='convergence')
        axs[1].remove()
        ax2=fig.add_subplot(gs[1])
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.tick_right()
    ax2.set(ylabel=time_units, xlabel='reaction coordinate',title='reaction coordinate evolution')
    for i in range(images-2):
        ax2.scatter(rc[i],time)
    fig.text(0.01,0.5,'forces / eV $\AA^{-1}$',ha='center',va='center',rotation='vertical')
    try:
        handles, labels = axs[0,0].get_legend_handles_labels()
    except IndexError:
        handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.show()


if __name__ == '__main__':
    inputfile = './'
    try:
        opts,args=getopt.getopt(sys.argv[1:],'hi:',['help','input='])
    except getopt.GetoptError:
        print('error in command line syntax')
        sys.exit(2)
    for i,j in opts:
        if i in ['-h','--help']:
            print('input options:\n\t-i, --input\t\tspecify an input path other than current directory\n\nhelp options:\n\t-h, --help\t\tdisplay this help message')
            sys.exit()
        if i in ['-i','--input']:
            inputfile=j
    mep_forces(inputfile)
