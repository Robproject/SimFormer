import math, cmath
import matplotlib.pyplot as plt

def arr(x, y, dx, dy):
    return plt.arrow(x, y, dx, dy, length_includes_head=True, head_width=.1, head_length=1, width=.05)
def oarr(a):
    return plt.arrow(0, 0, a.real, a.imag, length_includes_head=True, head_width=.1, head_length=1, width=.05)
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
    Pi = (V1 * I1).real
    n = Po/Pi
    return n
def SimForm(V_2, VA, Load, pf, LeadLag, a, Z_1, Z_2, Z_C, circ, ex):

    VA = VA * Load

    if pf == 1:
        I_2 = complex(VA / V_2, 0)
    else:
        ReI_2 = VA * pf / V_2
        if LeadLag == "lead":
            I_2 = complex(ReI_2, VA / V_2 * math.sin(math.acos(pf)))
        else:
            I_2 = complex(ReI_2, VA / V_2 * -math.sin(math.acos(pf)))

    V_2 = complex(V_2, 0)

    if circ == "ex":
        E_2 = I_2 * Z_2 + V_2
        E_1 = a * E_2
        I_C = get_I_C(Z_C, E_1)
        I_1 = I_C[0] + I_2/a
        V_1 = I_1 * Z_1 + E_1
        Z_L = V_2 / I_2

        E2 = oarr(E_2).set_color('violet')
        E1 = oarr(E_1).set_color('green')

        vds = get_vd_dxdy(I_2, Z_2)
        I2R2 = arr(V_2.real, V_2.imag, vds[0], vds[1]).set_color('black')
        I2X2 = arr(V_2.real + vds[0], V_2.imag + vds[1], vds[2], vds[3]).set_color('orange')
    else:
        Z_1 = Z_1 + Z_2
        V_1 = I_2 * Z_1 + V_2
        E_1 = V_1
        I_C = get_I_C(Z_C, V_1)
        I_1 = I_C[0] + I_2

    n = get_efficiency(V_1, V_2, I_1, I_2)
    print('n =', n * 100, "%")
    VR = (abs(V_1) - a*abs(V_2))/(a*abs(V_2))
    print('VR =', VR*100, "%")

    print('V_1 =', cmath.polar(V_1), 'I_1 =', cmath.polar(I_1))


    V2 = oarr(V_2).set_color('blue')
    V1 = oarr(V_1).set_color('red')


    vdp = get_vd_dxdy(I_1, Z_1)
    I1R1 = arr(E_1.real, E_1.imag, vdp[0], vdp[1]).set_color('black')
    I1X1 = arr(E_1.real+vdp[0], E_1.imag+vdp[1], vdp[2], vdp[3]).set_color('orange')

    I2 = oarr(I_2).set_color('orange')
    ICr = oarr(I_C[1]).set_color('violet')
    ICx = oarr(I_C[2]).set_color('pink')
    IC = oarr(I_C[0]).set_color('blue')
    I1 = oarr(I_1).set_color('red')

    plt.xlim(-5, V_1.real + 10)
    plt.ylim(- abs(I_2) , V_1.imag + 10)

    plt.show()

if __name__ == '__main__':

    SimForm(200, 1000, .60, 1, "lag", .25, .05 + .225j, 0 + 0j, 75 + 20j, "eq", "pri")
#      V2(V),  |S|(VA), Load(.%%), pf(.%%), lead/lag, a, Z1, Z2, ZC, 'eq' or 'ex', 'pri' or 'sec'