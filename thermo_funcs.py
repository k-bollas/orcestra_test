from numpy import power, roots, min, array, isreal, log, sqrt, log10, polyval, ones, all, matmul
from numpy.linalg import inv
from numpy.random import rand
import warnings
import time

def power_law(x, a, b, c):
    return a*power(x, b) + c

def third_poly(x, a, b, c, d) -> float:
    return a*x**3 + b*x**2 + c*x + d

def fourth_poly(x, a, b, c, d, e) -> float:
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

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

def secant(a,b,f,tol, *args):
    a_n = a; f_a_n = f(a)
    b_n = b; f_b_n = f(b)
    stepNum=0
    decims = -int(log10(tol))
    m_n = a_n - f_a_n*(b_n - a_n)/(f_b_n - f_a_n)
    f_m_n = f(m_n)
    while abs(b_n-a_n) > tol:
        f_prev = f_m_n
        stepNum=stepNum+1
        m_n = a_n - f_a_n*(b_n - a_n)/(f_b_n - f_a_n)
        f_m_n = f(m_n)
        # print(m_n, f_m_n, 50*' ')#, end='\r', flush=True)
        if 'show' in args:
            print(a_n, b_n, m_n)
        if abs(f_m_n) < 1e-8:
            # print("Found exact solution." , end = '\r', flush=True)
            break
        if abs(f_m_n) < 1e-6 and abs(f_prev - f_m_n) < 1e-8:
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
        if stepNum > 500:
            raise ValueError("Secant method did not converge.")
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
        if 'show' in args:
            print(x_n, x1, x2)
        if x_n < 0 and 'only_possitive' in args:
            x_n = float(rand(1)*(x1 + x2)/2)
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
        if 'show' in args:
            print(x1, x2, x3)
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
        "MDM": 1410044.755816551,
        "ISOBUTAN": 3629000.0,
        "CYCLOHEX": 4082400.0,
        "TOLUENE": 4126000.0,
        "R245FA": 3651000.0,
        "ETHANOL": 6268000.0,
    }
    return Data[media]

def critical_temp(media) -> float:
    Data = {
        "IPENTANE": 460.35,
        "H2O": 647.096,
        "MDM": 564.09,
        "ISOBUTAN": 407.817,
        "CYCLOHEX": 553.6,
        "TOLUENE": 591.75,
        "R245FA": 427.01,
        "ETHANOL": 514.71,
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
        "MDM": 236.53146,
        "ISOBUTAN": 58.1222,
        "CYCLOHEX": 84.15948,
        "TOLUENE": 92.13842,
        "R245FA": 134.04794,
        "ETHANOL": 46.06844,
    }
    return Data[media]

def reference_data(media, *args) -> float:
    # T_ref = 298.15, P_ref = 101325
    h_ref_Data = {
        "IPENTANE": -465.1999941068353,
        "MDM": -58570.09383622628,
        "ISOBUTAN": 34758.775616486266,
        "CYCLOHEX": -9340.27904250502,
        "TOLUENE": -14572.886642192747,
        "R245FA": 57040.279662335124,
        "ETHANOL": -6572.404291526346,
    }

    s_ref_Data = {
        "IPENTANE": -21.52401509346904,
        "MDM": -687.9834445109129,
        "ISOBUTAN": 1206.3691080638048,
        "CYCLOHEX": -340.60680672773975,
        "TOLUENE": -464.74963440253316,
        "R245FA": 1115.5846904191837,
        "ETHANOL": -439.0314945587033,
    }

    P_min_Data = {
        "IPENTANE": 34548.97173350334,
        "MDM": 86.90387897550696,
        "ISOBUTAN": 162612.3001893673,
        "CYCLOHEX": 5431.367557558421,
        "TOLUENE": 1395.625885814431,
        "R245FA": 72598.85094149844,
        "ETHANOL": 2585.8919501261157,
    }

    P_sat298_Data = {
        "IPENTANE": 95589.83365239418,
        "MDM": 213.47254301663887,
        "ISOBUTAN": 352388.1004062365,
        "CYCLOHEX": 11832.999286471502,
        "TOLUENE": 2829.1165265611617,
        "R245FA": 150817.34224564815,
        "ETHANOL":5788.505598418044,
    }

    s_ref = entropy_vap('molar', P_sat298_Data[media], media)
    return_values = []
    indexs = ['H', 'S', 'Pmin']
    outputs = [h_ref_Data[media], s_ref, P_min_Data[media]]
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
        "H2O": [12.623762604570574, 0.2063015816255692, 233.52523352954742],
        "MDM": [12.096590742622269, 0.22854734568512008, 256.93759829373136],
        "ISOBUTAN": [5.7993049850386615, 0.24895770773331616, 158.72211480381426],
        "CYCLOHEX": [7.5807012375559895, 0.2486377080002356, 220.08895766397495],
        "TOLUENE": [9.730644960745698, 0.2366307544207094, 234.33711669869894],
        "R245FA": [7.360704186894217, 0.2323716048694507, 180.59410832712788],
        "ETHANOL": [9.70968895028273, 0.21446413819353646, 235.89978005774904],
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

def density_liquid(base, media, T):
    rho_liquid_Data = {
        "IPENTANE": [0, 0, 0, 0, 8070.47],
        "H2O": [0, 0, 0, 0, 53324.19],
        "MDM": [-1.2880595312062534e-07, 0.00019604226419838502, -0.11147135551056647, 26.94881311365969, -1485.019625114594],
        "ISOBUTAN": [-2.2038499472799376e-06, 0.002863923973998742, -1.3939804709350871, 299.8187521916941, -23405.90379196215],
        "CYCLOHEX": [-1.6598096763137473e-07, 0.00025370392986304884, -0.14491751016335225, 35.61049131566977, -2370.1043680203534],
        "TOLUENE": [-9.730167674413557e-08, 0.00015158548432554335, -0.0881642690939973, 21.659206045895896, -1002.5463195662455],
        "R245FA": [-2.43187265188239e-06, 0.003190596114244078, -1.5696413256881336, 340.1859064598278, -25890.498639009216],
        "ETHANOL": [-2.8619074656678294e-07, 0.0004125582592845447, -0.22301184704365895, 52.54644289407915, -3722.935286324642],
    }

    rho_mass = fourth_poly(T, *rho_liquid_Data[media])
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
        "IPENTANE": [-1.4934667404845468e-07, 8.360089620292359e-05, 0.3106936893968899, 25.982404950331297],
        "MDM": [6.173647655701377e-08, -0.000349049175782291, 0.7863488138725345, 147.0192216996996],
        "ISOBUTAN": [3.8542407810975426e-08, -0.00019964179268486173, 0.39147905560957064, -1.4612289950976314],
        "CYCLOHEX": [7.385041023155245e-08, -0.0003687354937708429, 0.676314748873086, -63.715250448043065],
        "TOLUENE": [6.302766275215257e-08, -0.0002893438958704359, 0.503361306228835, -15.388897588237763],
        "R245FA": [4.105235662808224e-08, -0.00020292075596997966, 0.35797529646942444, 27.542708974698378],
        "ETHANOL": [1.6420701061576366e-08, -9.401293140086021e-05, 0.20356003967086306, 16.750113393609226],
    }
    return Data[media]

def ideal_cpmolar_liquid(base, media, T) -> float:
    cp_liquid_Data = {
        "IPENTANE": [1.6713590556391626e-06, -0.0007482589775293744, 0.37876360997836633, 73.3483038454218],
        "H2O": [4.6576157438791806e-07, -0.00033388117471674363, 0.07517927022343525, 70.18242280115233],
        "MDM": [-2.1484892886470624e-06, 0.0027542558476381256, -0.5321224113372257, 392.5617299130509],
        "ISOBUTAN": [3.1026453533825644e-06, -0.001472808473318796, 0.42276100785573933, 63.86829202663845],
        "CYCLOHEX": [3.6134827986626795e-07, -0.00013494308947843288, 0.37843554613266217, 46.03630016583857],
        "TOLUENE": [-1.1938547384150377e-06, 0.0015421758154580837, -0.3082609541054791, 143.20345076468982],
        "R245FA": [3.1130516427357972e-06, -0.0016183726223522677, 0.4593719857441201, 100.92570367753852],
        "ETHANOL": [-2.1921431070111532e-06, 0.003319322085561455, -1.0327262719178865, 183.09559305961426],
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
        "IPENTANE": 0.2274,
        "MDM": 0.5280658490542447,
        "ISOBUTAN": 0.183,
        "CYCLOHEX": 0.212,
        "TOLUENE": 0.263,
        "R245FA": 0.3776,
        "ETHANOL": 0.644,
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
        "IPENTANE": [-9.201611431609613e-10, -0.0007290532117048507, -2062.5596407037456, 48644.5830038151],
        "MDM": [-4.706832346332244e-09, -0.009717918927239886, -2332.7072534523804, 63566.059786981],
        "ISOBUTAN": [-9.298155956227794e-10, 0.0010227062017887304, -2725.8902355477353, 53571.847735116055],
        "CYCLOHEX": [-6.903209114592468e-10, -0.0013377955659875978, -2042.1215781232622, 53303.13789278273],
        "TOLUENE": [-6.159919826250689e-10, -0.00234680517661459, -1933.3645102847584, 55158.13730494063],
        "R245FA": [-8.699612081155264e-10, -0.00024039387454405194, -2691.442925236896, 57848.44058610911],
        "ETHANOL": [-3.420530737556484e-10, -0.0013595383377909243, -2269.4120286694224, 64658.162563254424],
        "H2O": [-1.9910537531148716e-11, -0.0006564921003691679, -1598.0484117387098, 58331.079044394035],
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

    beta_Data = {
        "IPENTANE": 1655.0909054141323*1e-6,
        "H2O": 257.62735420172146*1e-6,
        "MDM": 1224.3463151083774*1e-6,
        "ISOBUTAN": 2334.400668538693*1e-6,
        "CYCLOHEX": 1220.336111363932*1e-6,
        "TOLUENE": 1080.7348553306667*1e-6,
        "R245FA": 2041.3841250204491*1e-6,
        "ETHANOL": 1095.4161042780302*1e-6,
    }

    rho_avg = (density_liquid('molar', media, T1) + density_liquid('molar', media, T2))/2

    c_avg = (ideal_cpmolar_liquid('molar', media, T2) + ideal_cpmolar_liquid('molar', media, T1))/2
    v_avg = 1/rho_avg
    T_avg = (T1 + T2)/2
    beta = beta_Data[media]
    h_molar = c_avg*(T2 - T1) + v_avg*(1 - beta*T_avg)*(P2 - P1)
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
    beta_Data = {
        "IPENTANE": 1655.0909054141323*1e-6,
        "H2O": 257.62735420172146*1e-6,
        "MDM": 1224.3463151083774*1e-6,
        "ISOBUTAN": 2334.400668538693*1e-6,
        "CYCLOHEX": 1220.336111363932*1e-6,
        "TOLUENE": 1080.7348553306667*1e-6,
        "R245FA": 2041.3841250204491*1e-6,
        "ETHANOL": 1095.4161042780302*1e-6,
    }

    beta = beta_Data[media]
    rho_avg = (density_liquid('molar', media, T1) + density_liquid('molar', media, T2))/2

    c_avg = (ideal_cpmolar_liquid('molar', media, T2) + ideal_cpmolar_liquid('molar', media, T1))/2
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

def entropy_vap(base, P, media) -> float:
    s_vap_Data = {
        "IPENTANE": [-2.3685622976725148e-12, 2.0653386974628845e-06, -15.18228407129838, 257.5409239712785],
        "MDM": [-1.0306565994784075e-11, -8.933823905025606e-06, -15.010139099322735, 257.88411884769897],
        "ISOBUTAN": [-2.7954903460025027e-12, 7.386665622224886e-06, -18.53539668442893, 298.51729044124096],
        "CYCLOHEX": [-1.3912863855779808e-12, -1.7666854732184042e-07, -13.934819501044316, 244.69013396392998],
        "TOLUENE": [-1.1623021293572008e-12, -1.816993218150737e-06, -13.442229961578644, 240.6327813375055],
        "R245FA": [-2.309200198209342e-12, 2.5464130864281816e-06, -16.983539772156274, 288.24310190971374],
        "ETHANOL": [-7.522533626954363e-13, -1.246449719250844e-06, -14.471529400967498, 276.4544465089006],
    }

    s_vap_par = s_vap_Data[media]
    s_vap_molar = poly_log(P, *s_vap_par)
    s_vap_mass = s_vap_molar/(molar_mass(media)*1e-3)
    if base in ["mass", "molar"]:
        s_vap = s_vap_molar if base == "molar" else s_vap_mass
    else:
        raise ValueError(' First parameter must be the specified base that enthalpy is calculated (must be string). The enthalpy must be calculated either in mass or molar based.')
    return s_vap

def entropy_gas_specified(base, P, media) -> float:
    return entropy_liquid(base, P, T_satur(P, media), 101325, 298, media) + entropy_vap(base, P, media)

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