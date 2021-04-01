from numpy import array,dot
from os import listdir,chdir
from os.path import exists,getsize
from copy import deepcopy

#calculates trajectory of atoms in mep calculation
#trajectories by default are vectors relative to the initial position (ie the POSCAR in directory ./00/)
#by specifying reverse, the vectors are made relative to the final position, found in ./# of images/POSCAR
def mep_trajectory(filepath,**args):
    if 'reverse' in args:
        reverse=True
    else:
        reverse=False
        
    chdir(filepath)
    files=listdir(filepath)
    image_num=0
    for i in files:
        try:
            if int(i)>image_num:
                image_num=int(i)
        except ValueError:
            pass
    image_num+=1
    
    trajectory=[]
    for i in range(image_num):
        if exists('./'+str('{:02d}'.format(i))+'/CONTCAR'):
            if getsize('./'+str('{:02d}'.format(i))+'/CONTCAR')>0:
                filepath='./'+str('{:02d}'.format(i))+'/CONTCAR'
            else:
                filepath='./'+str('{:02d}'.format(i))+'/POSCAR'
        else:
            filepath='./'+str('{:02d}'.format(i))+'/POSCAR'
        coord=parse_poscar(filepath)[1]
        trajectory.append(coord)
    
    if reverse==True:
        ref=deepcopy(trajectory[-1])
    else:
        ref=deepcopy(trajectory[0])
    for i in range(image_num):
        trajectory[i]-=ref
        
    return trajectory
    
def parse_poscar(ifile):
    with open(ifile, 'r') as file:
        lines=file.readlines()
        sf=float(lines[1])
        latticevectors=[float(lines[i].split()[j])*sf for i in range(2,5) for j in range(3)]
        latticevectors=array(latticevectors).reshape(3,3)
        atomtypes=lines[5].split()
        atomnums=[int(i) for i in lines[6].split()]
        if 'Direct' in lines[7] or 'Cartesian' in lines[7]:
            start=8
            mode=lines[7].split()[0]
        else:
            mode=lines[8].split()[0]
            start=9
            seldyn=[''.join(lines[i].split()[-3:]) for i in range(start,sum(atomnums)+start)]
        coord=array([[float(lines[i].split()[j]) for j in range(3)] for i in range(start,sum(atomnums)+start)])
        if mode!='Cartesian':
            for i in range(sum(atomnums)):
                for j in range(3):
                    while coord[i][j]>1.0 or coord[i][j]<0.0:
                        if coord[i][j]>1.0:
                            coord[i][j]-=1.0
                        elif coord[i][j]<0.0:
                            coord[i][j]+=1.0
                coord[i]=dot(coord[i],latticevectors)
            
    #latticevectors formatted as a 3x3 array
    #coord holds the atomic coordinates with shape ()
    try:
        return latticevectors, coord, atomtypes, atomnums, seldyn
    except NameError:
        return latticevectors, coord, atomtypes, atomnums