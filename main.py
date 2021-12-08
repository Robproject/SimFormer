import math, cmath
import matplotlib.pyplot as plt

def oarr(a, c):
    scale = 1
    if c == 'c':
        scale = .2
    return plt.arrow(0, 0, a.real, a.imag, length_includes_head=True, head_width=.1 * scale , head_length=1 * scale, width=.05 * scale)

def zarr(i, vd):
    return plt.arrow(i.real, i.imag, vd[0], vd[1], length_includes_head=True, head_width=.1, head_length=1, width=.05, color='black'), \
           plt.arrow(i.real + vd[0], i.imag + vd[1], vd[2], vd[3], length_includes_head=True, head_width=.1, head_length=1, width=.05, color='orange')

def get_vd_dxdy(I, Z):
  vrdx = (I * Z.real).real
  vrdy = (I * Z.real).imag
  vxdx = (I * (Z.imag*1j)).real
  vxdy = (I * (Z.imag*1j)).imag
  return (vrdx, vrdy, vxdx, vxdy)

def get_I_C(Z, E):
    I_CR = E/complex(Z.real,0)
    I_CX = E/complex(0,Z.imag)
    I_C = I_CR + I_CX
    return (I_C, I_CR, I_CX)

def get_efficiency(V1, V2, I1, I2):
    Po = (V2 * I2).real
    Pi = abs(I1) * abs(V1) * math.cos(cmath.phase(V1) - cmath.phase(I1))
    n = Po/Pi
    return n

def print_phasor(name, unit, var):
    return print( f'{name} = %5.2f\u2220%4.2f{unit}' % (abs(var), cmath.phase(var) * 180 / cmath.pi))

def SimForm(V_2, VA, Load, pf, LeadLag, a, Z_1, Z_2, Z_C, pos):

    VA = VA * Load

    if pf == 1:
        I_2 = complex(VA / V_2, 0)
    else:
        ReI_2 = VA * pf / V_2
        ImI_2 = VA /V_2 * math.sin(math.acos(pf))
        if LeadLag == 'lead':
            I_2 = complex(ReI_2, ImI_2)
        else:
            I_2 = complex(ReI_2, -ImI_2)

    V_2 = complex(V_2, 0)
    E_2 = (I_2 * Z_2) + V_2
    E_1 = a * E_2

    if pos == 'before':
        V_1 = (I_2/a * Z_1) + E_1
        I_C = get_I_C(Z_C, V_1)
        I_1 = I_C[0] + I_2/a
    else:
        I_C = get_I_C(Z_C, E_1)
        I_1 = I_C[0] + I_2/a
        V_1 = I_1 * Z_1 + E_1

    n = get_efficiency(V_1, V_2, I_1, I_2)
    print('\u03B7 = %4.2f%%' % (n*100))
    VR = (abs(E_2) - abs(V_2))/(a*abs(E_2))
    print('VR = %4.4f%%' % (VR*100))
    print_phasor('V1', 'V', V_1)
    print_phasor('I1', 'A', I_1)
    print_phasor('E1', 'V', E_1)
    print_phasor('IC', 'A', I_C[0])
    print_phasor('E2', 'V', E_2)
    print_phasor('V2', 'V', V_2)
    print_phasor('I2', 'A', I_2)

    arrow = [E_2, E_1, V_2, V_1, I_2, I_1]
    color = ['violet', 'green', 'blue', 'red', 'orange', 'red']
    for ar, co in zip(arrow, color):
        oarr(ar, 'v').set_color(co)

    vds = get_vd_dxdy(I_2, Z_2)
    VZS = zarr(V_2, vds)

    vdp = get_vd_dxdy(I_1, Z_1)
    VZP = zarr(E_1, vdp)

    ICr = oarr(I_C[1], 'c').set_color('violet')
    ICx = oarr(I_C[2], 'c').set_color('pink')
    IC = oarr(I_C[0], 'c').set_color('blue')

    plt.xlim(-5, V_1.real + 10)
    plt.ylim(- abs(I_2) , V_1.imag + 10)

    plt.show()

if __name__ == '__main__':

    SimForm(240, 2400, .8, 1, 'lag', 10, 1.5 + 2.5j, .02 + .03j, 6000 + 8000j, 'center' )
#          V2(V), |S|(VA), Load(.%%), pf(.%%), lead/lag, a, Z1, Z2, ZC, 'before' or 'center'