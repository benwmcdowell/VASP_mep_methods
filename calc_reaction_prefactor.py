from os.path import exists

def calc_reaction_prefactor(outcar):
    energies=[[],[]]
    with open(outcar,'r') as outcar:
        while True:
            line=outcar.readline()
            if not line:
                break
            if'THz' in line:
                if '/i' not in line:
                    energies[0].append(float(line.split()[3]))
                else:
                    energies[1].append(float(line.split()[2]))
    for j in range(2):
        tempvar=1.0
        for i in energies[j]:
            tempvar*=i
        energies[j]=tempvar
    
    return energies

if __name__ == '__main__':
    outcar='./OUTCAR'
    if exists(outcar):
        energies=calc_reaction_prefactor(outcar)
        print('reaction prefactor:  {}'.format(energies[0]))
        print('imaginary modes:  {}'.format(energies[1]))
        print('units in THz')
