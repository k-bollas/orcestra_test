from numpy import power, roots, min, array, isreal, log, sqrt, log10, polyval, ones, all, matmul
from numpy.linalg import inv
from numpy.random import rand
import warnings
import time

def power_law(x, a, b, c):
    return a*power(x, b) + c

def third_poly(x, a, b, c, d) -> float:
    return a*x**3 + b*x**2 + c*x + d

def poly_log(x, a, b, c, d) -> float:
    return a*x**2 + b*x + c*log(x) + d

def poly_integral(x1,x2, *args) -> float:
    n = len(args)
    I = 0
    for k in args:
        I = I + k*(x2**n/n - x1**n/n)
        n = n - 1
    return I

def poly_frac_integral(x1,x2, *args) -> float:
    n = len(args)
    I = 0
    for k in args:
        I = I + k*x2**(n-1)/(n-1) - k*x1**(n-1)/(n-1) if n - 1>0 else I + k*log(x2/x1)
        n = n - 1
    return I

def secant(a,b,f,tol):
    a_n = a; f_a_n = f(a)
    b_n = b; f_b_n = f(b)
    stepNum=0
    decims = -int(log10(tol))
    m_n = a_n - f_a_n*(b_n - a_n)/(f_b_n - f_a_n)
    f_m_n = f(m_n)
    while abs(b_n-a_n) > tol:
        stepNum=stepNum+1
        m_n = a_n - f_a_n*(b_n - a_n)/(f_b_n - f_a_n)
        f_m_n = f(m_n)
        # print(m_n, f_m_n, 50*' ')#, end='\r', flush=True)
        # print(a_n, b_n, m_n, f_m_n)
        if abs(f_m_n) < 1e-8:
            # print("Found exact solution." , end = '\r', flush=True)
            break
        if f_a_n*f_m_n < 0:
            a_n = a_n; f_a_n = f_a_n
            b_n = m_n; f_b_n = f_m_n
        elif f_b_n*f_m_n < 0:
            a_n = m_n; f_a_n = f_m_n
            b_n = b_n; f_b_n = f_b_n
        else:
            print("Secant method fails.")
            return None
    return m_n, f_m_n, stepNum

def alternative_secant(x1,x2,f,tol, *args):
    err = 1
    stepNum = 0
    while err > tol:
        stepNum=stepNum+1
        A = array([[1,1],[f(x1), f(x2)]])
        B = array([[1], [0]])
        p = matmul(inv(A), B)
        x_n = float(sum([k1*k2 for k1,k2 in zip(p, [x1,x2])]))
        err = abs(x2 - x_n)
        x1,x2 = x2, x_n
        # print(x1, x2)
    
    return x_n, f(x_n), stepNum


def general_secant(x1,x2,x3,F,tol, *args):
    err = array([1,1])
    stepNum=0
    while all(err > tol*ones(len(err))):
        stepNum=stepNum+1
        A = array([[1,1,1],[F(x1)[0],F(x2)[0],F(x3)[0]],[F(x1)[1],F(x2)[1],F(x3)[1]]])
        B = array([[1],[0],[0]])
        p = matmul(inv(A), B)
        x_n = p[0]*x1 + p[1]*x2 + p[2]*x3
        err = abs(x3 - x_n)
        if 'only_possitive' in args:
            if x_n[0] < 0: x_n[0] = rand(1)*(x1[0] + x3[0])/2
            if x_n[1] < 0: x_n[1] = rand(1)*(x1[1] + x3[1])/2
        x1, x2, x3 = x2, x3, x_n
        # print(x1, x2, x3)
    return x_n, F(x_n), stepNum

def goldenOpt(a,b,f,tol):
        r=(sqrt(5)-1)/2
        a1=b-r*(b-a)
        a2=a+r*(b-a)
        stepNum=0
        decims = -int(log10(tol))
        while abs(b-a) > tol:
            print(" a = {} , b = {} , b-a = {}".format(round(a,decims), 
round(b,decims), round(abs(b-a),decims)), end="\r", flush=True)
            stepNum=stepNum+1
            f1=f(a1)
            f2=f(a2)
            if f1<f2:
                a=a1
                f1=f2
                a1=a2
                a2=a+r*(b-a)
            else:
                b=a2
                a2=a1
                f2=f1
                a1=b-r*(b-a)
        x_opt=(a+b)/2
        f_opt=f(x_opt)
        return x_opt,f_opt,stepNum



def critical_pres(media) -> float:
    Data = {
        "IPENTANE": 3378000.0,
        "H2O": 22064000.0,
    }
    return Data[media]

def critical_temp(media) -> float:
    Data = {
        "IPENTANE": 460.35,
        "H2O": 647.096,
    }
    return Data[media]

def molar_mass(media) -> float:
    Data = {
        "CO": 28.0101,
        "CO2": 44.0098,
        "O2": 31.9988,
        "N2": 28.01348,
        "H2O": 18.015268,
        "H2":2.01588,
        "CH4": 16.0428,
        "IPENTANE": 72.14878,
    }
    return Data[media]

def reference_data(media, *args) -> float:
    # T_ref = 298.15, P_ref = 101325
    h_ref_Data = {
        "IPENTANE": -465.1999941068353
    }

    s_ref_Data = {
        "IPENTANE": -1.5529314296953771
    }

    P_min_Data = {
        "IPENTANE": 34548.97173350334
    }

    return_values = []
    indexs = ['H', 'S', 'Pmin']
    outputs = [h_ref_Data[media], s_ref_Data[media], P_min_Data[media]]
    for x in args:
        if x in indexs:
            return_values.append(outputs[indexs.index(x)])
    if len(return_values) == 1:
        return_values = return_values[0]

    return return_values

def T_satur(P0, media) -> float:

    if media == "WATER": media = "H2O"
    Data = {
        "IPENTANE": [8.586124683012057, 0.23344582416555298, 173.28132421262504],
        "H2O": [12.623762604570574, 0.2063015816255692, 233.52523352954742]

    }
    if media in Data.keys():
        popt = Data[media]
    else:
        raise ValueError(" Saturation Temperature can't be calculated. Fliud does not exist in database")
    T_sat = power_law(P0, *popt)
    return T_sat

def compressibility_factor(P,T,media) -> float:
    warnings.filterwarnings("ignore")
    R = 8314/molar_mass(media)
    Tc, Pc = critical_temp(media), critical_pres(media)
    a, b =  0.42747*R**2*Tc**2.5/Pc, 0.08664*R*Tc/Pc
    A, B = a*P/(R**2*T**2.5), b*P/(R*T)
    pfac = [1, -1, A-B-B**2, -A*B]
    Z_sol = roots(pfac)
    Z_real = [float(x) for x in Z_sol if isreal(x)]
    if len(Z_real) > 1:
        Z = [x for x in Z_real if 1-x == min(1 - array(Z_real))][0]
    else:
        Z = float(Z_real[0])
    return Z

def density(P,T,media) -> float:
    R = 8314/molar_mass(media)
    Z = compressibility_factor(P,T,media)
    v_ideal = R*T/P
    v_real = Z*v_ideal
    return 1/v_real

def density_liquid(base, media):
    rho_liquid_Data = {
        "IPENTANE": 8070.47,
    }

    rho_mass = rho_liquid_Data[media]
    rho_molar = rho_mass*molar_mass(media)
    if base == 'mass':
        rho = rho_mass
    else:
        rho = rho_molar
    return rho

def ideal_cpmolar(media) -> array:
    Data = {
        "CO": [-1.3982364970020488e-08, 3.0423379787590333e-05, -0.014388574717088994, 31.14707011324664],
        "CO2": [6.8764331139653785e-09, -3.257575850723297e-05, 0.05652160600574999, 23.590646827581068],
        "O2": [1.4852579479387224e-09, -8.0796268586121e-06, 0.016683941420406714, 24.74063266387961],
        "N2": [-2.4066123119904753e-09, 6.266618162196282e-06, 0.0004994948204013997, 28.224786433983716],
        "H2O": [-5.254044744302822e-09, 1.721705772021166e-05, -0.006049034275552882, 35.27045769381774],
        "H2": [-8.431231839239766e-10, 4.366173045776814e-06, -0.002900635063489882, 29.640992741512843],
        "CH4": [-8.769571029555713e-10, -1.506882696242349e-05, 0.07519532409238476, 13.294107482324739],
        "IPENTANE": [-1.4934667404845468e-07, 8.360089620292359e-05, 0.3106936893968899, 25.982404950331297]
    }
    return Data[media]

def ideal_cpmolar_liquid(base, media, T) -> float:
    cp_liquid_Data = {
        "IPENTANE": [1.6713590556391626e-06, -0.0007482589775293744, 0.37876360997836633, 73.3483038454218],
        "H2O": [4.6576157438791806e-07, -0.00033388117471674363, 0.07517927022343525, 70.18242280115233],
    }

    cp_liquid = cp_liquid_Data[media]
    cp_molar = polyval(cp_liquid, T)
    cp_mass = cp_molar/(molar_mass(media)*1e-3)
    if base == 'mass':
        cp = cp_mass
    else:
        cp = cp_molar
    return cp

def acentric_factor(media) -> float:
    Data = {
        "IPENTANE": 0.2274
    }
    return Data[media]

def enthalpy(base, P2, T2, P1, T1, media, *args) -> float:
    cp_molar = ideal_cpmolar(media)
    h_molar_i = poly_integral(T1, T2, *cp_molar)

    if not("ideal" in args):    
        Z2, Z1 = compressibility_factor(P2,T2,media), compressibility_factor(P1,T1,media)
        P_crit, T_crit = critical_pres(media), critical_temp(media)
        A2, B2 = 0.42748*(P2/P_crit)/(T2/T_crit)**2.5, 0.08664*(P2/P_crit)/(T2/T_crit)
        A1, B1 = 0.42748*(P1/P_crit)/(T1/T_crit)**2.5, 0.08664*(P1/P_crit)/(T1/T_crit)
        h_molar_dep = 8.314*T2*(Z2 - 1 - 3/2*A2/B2*log(1 + B2/Z2)) - 8.314*T1*(Z1 - 1 - 3/2*A1/B1*log(1 + B1/Z1))
    else:
        h_molar_dep = 0
    
    h_molar = h_molar_dep + h_molar_i
    h_mass = h_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        h = h_molar if base == "molar" else h_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return h

def enthalpy_vap(base, P, media) -> float:
    h_vap_Data = {
        "IPENTANE": [-9.201611431609613e-10, -0.0007290532117048507, -2062.5596407037456, 48644.5830038151]
    }

    h_vap_par = h_vap_Data[media]
    h_vap_molar = poly_log(P, *h_vap_par)
    h__vap_mass = h_vap_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        h_vap = h_vap_molar if base == "molar" else h__vap_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return h_vap

def enthalpy_mix(base, P2, T2, P1, T1, y, subs, *args) -> float:
    h_molar = 0
    mw = 0
    for subs_i in subs:
        h_i = enthalpy("molar", P2, T2, P1, T1, subs_i, *args)
        mw_i = molar_mass(subs_i)
        h_molar = h_molar + y[subs.index(subs_i)]*h_i
        mw = mw + y[subs.index(subs_i)]*mw_i
    h_mass = h_molar/(mw*1e-3)
    if base in ["mass", "molar"]:
        h_mix = h_molar if base == "molar" else h_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return h_mix

def pressure_correction_liquid(P, media) -> float:
    corr_Data = {
        'IPENTANE': [6.059901846101062e-30, -6.153791999886393e-23, 2.484038869332436e-16, -4.91497545350383e-10, 0.00047087171704051435, -48.935640004410814],
        'H2O': [-4.844897254626344e-28, 1.4729201536396005e-21, -1.6809664503181336e-15, 8.351239156566494e-10, -4.217208015945755e-05, -95.52309474728739],
    }

    p_min_lim_Data = {
        'IPENTANE': 0.45*1e5,
        'H2O': 0.8*1e5,
    }

    if P < p_min_lim_Data[media]:
        raise ValueError(' Input pressure is lower than pressure lower limit for this fluid : {}'.format(media))
    
    correction = polyval(corr_Data[media], P)
    return correction


def enthalpy_liquid(base, P2, T2, P1, T1, media) -> float:
    cp_liquid_Data = {
        "IPENTANE": [1.6713590556391626e-06, -0.0007482589775293744, 0.37876360997836633, 73.3483038454218],
        "H2O": [4.6576157438791806e-07, -0.00033388117471674363, 0.07517927022343525, 70.18242280115233],
    }

    beta_Data = {
        "IPENTANE": 1655.0909054141323*1e-6,
        "H2O": 257.62735420172146*1e-6,
    }

    rho_liquid_Data = {
        "IPENTANE": 8070.47,
        "H2O": 53324.19,
    }

    cp_liquid = cp_liquid_Data[media]
    c_avg = (polyval(cp_liquid, T2) + polyval(cp_liquid, T1))/2
    v_avg = (1/rho_liquid_Data[media])/molar_mass(media)
    T_avg = (T1 + T2)/2
    beta = beta_Data[media]
    h_molar = c_avg*(T2 - T1) + v_avg*(1 - beta*T_avg)*(P2 - P1)# - pressure_correction_liquid(P2, media)
    h_mass = h_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        h = h_molar if base == "molar" else h_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return h

def entropy(base, P2, T2, P1, T1, media, *args) -> float:
    if not("ideal" in args):
        Tc, Pc = critical_temp(media), critical_pres(media)
        a, b =  0.42747*8.314**2*Tc**2.5/Pc, 0.08664*8.314*Tc/Pc
        m = 0.48 + 1.574*acentric_factor(media) - 0.176*acentric_factor(media)**2
        da_dT1, da_dT2 = 2*(0.4275*8.314**2*Tc**2/Pc)*m/(2*sqrt(T1/Tc))*(1/Tc), 2*(0.4275*8.314**2*Tc**2/Pc)*m/(2*sqrt(T2/Tc))*(1/Tc)
        Z2, Z1 = compressibility_factor(P2,T2,media), compressibility_factor(P1,T1,media)
        v2, v1 = 1/(density(P2, T2, media)*molar_mass(media)*1e-3), 1/(density(P1, T1, media)*molar_mass(media)*1e-3)
        s_molar_dep = 8.314*log(Z2*(v2-b)/v2) + 1/b*da_dT2*log((v2+b)/v2) - 8.314*log(Z1*(v1-b)/v1) + 1/b*da_dT1*log((v1+b)/v1)
    else:
        s_molar_dep = 0

    cp_molar = ideal_cpmolar(media)
    s_molar_i = poly_frac_integral(T1, T2, *cp_molar) - 8.314*log(P2/P1)
    s_molar = s_molar_dep + s_molar_i
    s_mass = s_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        s = s_molar if base == "molar" else s_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return s

def entropy_liquid(base, P2, T2, P1, T1, media) -> float:
    cp_liquid_Data = {
        "IPENTANE": [1.6713590556391626e-06, -0.0007482589775293744, 0.37876360997836633, 73.3483038454218]
    }

    beta_Data = {
        "IPENTANE": 1655.0909054141323*1e-6
    }

    rho_avg = density_liquid('molar', media)

    beta = beta_Data[media]
    cp_liquid = cp_liquid_Data[media]
    c_avg = (polyval(cp_liquid, T2) + polyval(cp_liquid, T1))/2
    v_avg = 1/rho_avg
    s_molar_i = c_avg*log(T2/T1) - beta*v_avg*(P2 - P1)
    s_molar = s_molar_i
    s_mass = s_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        s = s_molar if base == "molar" else s_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return s

def entropy_mix(base, P2, T2, P1, T1, y, subs, *args) -> float:
    s_molar = 0
    mw = 0
    for subs_i in subs:
        s_i = entropy("molar", P2, T2, P1, T1, subs_i)
        mw_i = molar_mass(subs_i)
        s_molar = s_molar + y[subs.index(subs_i)]*s_i
        mw = mw + y[subs.index(subs_i)]*mw_i
    s_mass = s_molar/(mw*1e-3)
    if base in ["mass", "molar"]:
        s_mix = s_molar if base == "molar" else s_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return s_mix

def speed_of_sound(P, T, media) -> float:
    P_i, T_i = P, T
    rho_i = density(P_i, T_i, media)
    rho_i_plus_1 = rho_i + 1
    rho_i_minus_1 = rho_i - 1
    x1, x2, x3 = array([P_i,T_i]), array([P_i - 100,T_i - 1]), array([P_i + 200,T_i + 10])
    F_i_plus_1 = lambda x: [density(x[0], x[1], media) - rho_i_plus_1, entropy('molar', x[0],x[1],P_i,T_i,media)]
    P_i_plus_1,T_i_plus_1 = general_secant(x1, x2, x3, F_i_plus_1, 1e-5, 'only_possitive')[0]

    F_i_minus_1 = lambda x: [density(x[0], x[1], media) - rho_i_minus_1, entropy('molar', x[0],x[1],P_i,T_i,media)]
    P_i_minus_1,T_i_minus_1 = general_secant(x1, x2, x3, F_i_minus_1, 1e-5, 'only_possitive')[0]

    c = sqrt((P_i_plus_1 - P_i_minus_1)/(rho_i_plus_1 - rho_i_minus_1))
    return c

if __name__ == '__main__':
    fluid = "IPENTANE"
    h = enthalpy_liquid("molar", 14*101325, 275.15, fluid)
    print(h)