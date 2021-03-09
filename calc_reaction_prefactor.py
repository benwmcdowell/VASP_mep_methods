def calc_reaction_prefactor(outcar):
    energies=[[],[]]
    with open(outcar,'r') as outcar:
        while True:
            line=outcar.readline()
            if not line:
                break
            if'THz' in line:
                if '/i' not in line:
                    energies[0].append(float(line.split()[9])/1000)
                else:
                    energies[1].append(float(line.split()[8])/1000)
    tempvar=1.0
    for i in energies[0]:
        tempvar*=i
    energies[0]=tempvar
    
    return energies

if __name__ == '__main__':
    outcar='./OUTCAR'
    energies=calc_reaction_prefactor(outcar)
    print('reaction prefactor:  {}'.format(energies[0]))
    print('imaginary modes:  {}'.format(energies[1]))