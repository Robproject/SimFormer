import math, cmath
import matplotlib.pyplot as plt

def oarr(a, c):
    if c == 'c':
        scale = .2
    else:
        scale = 1
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
    print(cmath.phase(V1), cmath.phase(I1))
    print(Po, Pi)
    n = Po/Pi
    return n

def SimForm(V_2, VA, Load, pf, LeadLag, a, Z_1, Z_2, Z_C, pos):

    VA = VA * Load

    if pf == 1:
        I_2 = complex(VA / V_2, 0)
    else:
        ReI_2 = VA * pf / V_2
        ImI_2 = VA /V_2 * math.sin(math.acos(pf))
        if LeadLag == "lead":
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
    print('n =', n*100, "%")
    VR = (abs(V_1) - a*abs(V_2))/(a*abs(V_2))
    print('VR =', VR*100, "%")
    print('V_1 =', cmath.polar(V_1), 'I_1 =', cmath.polar(I_1) )
    print('V_2 =', cmath.polar(V_2), 'I_2 =', cmath.polar(I_2))

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

    SimForm(120, 540, .8, .85, "lag", 2, 1.5 + 1.5j, 1.12 + 1.13j, 60 + 80j, 'center' )
#          V2(V), |S|(VA), Load(.%%), pf(.%%), lead/lag, a, Z1, Z2, ZC, 'before' or 'center'