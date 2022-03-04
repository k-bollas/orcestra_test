import thermo_funcs as tf
from numpy import array, linspace

class Thermodynamic_Cycle:
    def __init__(self) -> None:
        self.Th1, self.Ph1 = 150 + 273.15, 0.989*1e5
        self.mh_flow = 19.2
        self.fluid = "IPENTANE"
        self.Tw1, self.Pw1 = 15 + 273.15, 101325
        self.mw_flow = 10
        self.Pinch_evap_init, self.Pinch_cond__init = 5, 5
        self.P_crit, self.T_crit = tf.critical_pres(self.fluid), tf.critical_temp(self.fluid)
        self.DoSC, self.DoSH = 0, 0
        self.y_exh = [0.657, 0.158, 0.103, 0.072]
        self.subs_exh = ["N2", "CO2", "H2O", "O2"]
        self.P_min = tf.reference_data(self.fluid, 'Pmin')
        self.P_max = tf.secant(a = self.P_min, b = self.P_crit*0.99, f = lambda x: tf.T_satur(x, self.fluid) - self.Th1, tol = 1e-3)[0] if self.Th1 < self.T_crit else self.P_crit*0.99

    def Cycle_Dry_States(self,m_flow,**kwargs):
        self.Pinch_evap, self.Pinch_cond = self.Pinch_evap_init, self.Pinch_cond__init
        pinch_evap_fun = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(x, self.fluid) + self.Pinch_evap + self.DoSH, self.y_exh, self.subs_exh, "ideal") - m_flow*tf.enthalpy_vap("mass", x, self.fluid)
        
        if self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(self.P_crit*0.99, self.fluid) + self.Pinch_evap + self.DoSH, self.y_exh, self.subs_exh, "ideal") > m_flow*tf.enthalpy_vap("mass", self.P_crit*0.99, self.fluid):
            self.P3 = 0.99*self.P_crit
            thfpp_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*tf.enthalpy_vap("mass", self.P3, self.fluid)
            self.Thf_pp = tf.secant(a = self.Tw1, b = self.Th1, f = thfpp_function, tol = 1e-3)[0]
            self.Pinch_evap = self.Thf_pp - tf.T_satur(self.P3, self.fluid)
        else:        
            self.P3 = tf.secant(a = self.P_min, b = self.P_max, f = pinch_evap_fun, tol = 1e-3)[0]
        self.T3 = tf.T_satur(self.P3, self.fluid) + self.DoSH
        self.Z3 = tf.compressibility_factor(self.P3, self.T3, self.fluid)

        pinch_cond_fun = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, tf.T_satur(x, self.fluid) - self.Pinch_cond - self.DoSC, self.Pw1, self.Tw1, "H2O") - m_flow*tf.enthalpy_vap("mass", x, self.fluid)
        
        # print('Max : {:.3f}  ,  Crit : {:.3f},  P3 : {:.3f}'.format(self.P_max/1e5, self.P_crit/1e5, self.P3/1e5))
        self.P1 = tf.secant(a = self.P_min, b = self.P_max, f = pinch_cond_fun, tol = 1e-3)[0]
        self.T1 = tf.T_satur(self.P1, self.fluid)
        self.T_cond = self.T1 + self.DoSC

        self.P4 = self.P1
        self.T4 = tf.secant(a = self.Tw1,b = self.Th1,f = lambda x: tf.entropy("mass",self.P4, x, self.P3, self.T3, self.fluid) ,tol = 1e-3)[0]
        self.Z4 = tf.compressibility_factor(self.P4, self.T4, self.fluid)
        self.Dh34 = tf.enthalpy("mass", self.P3, self.T3, self.P4, self.T4, self.fluid)
        self.wout = self.Dh34

        self.h_ref = tf.reference_data(self.fluid, 'H')
        self.h1 = tf.enthalpy_liquid("mass", self.P1, self.T1, 101325, 298.15, self.fluid) + self.h_ref
        self.P2 = self.P3
        self.T2 = tf.secant(a = self.T1,b = self.T3,f = lambda x: tf.entropy_liquid("molar",self.P2, x, self.P1, self.T1, self.fluid) ,tol = 1e-3)[0]
        self.Dh12 = tf.enthalpy_liquid("mass", self.P2, self.T2, self.P1, self.T1, self.fluid)
        self.h2 = self.h1 + self.Dh12
        self.win = self.Dh12
        self.Dh23 = tf.enthalpy_liquid("mass", self.P3, self.T3, self.P2, self.T2, self.fluid) + tf.enthalpy_vap("mass", self.P3, self.fluid)
        self.qin = self.Dh23
        self.h3 = self.h2 + self.Dh23
        self.h4 = self.h3 - self.Dh34
        self.Dh41 = tf.enthalpy("mass", self.P4, self.T4, self.P1, self.T1, self.fluid) + tf.enthalpy_vap("mass", self.P1, self.fluid)
        self.qout = self.Dh41

        th2_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*self.Dh23
        self.Th2 = tf.secant(a = self.Tw1, b = self.Th1, f = th2_function, tol = 1e-3)[0]
        self.Ph2 = self.Ph1
        tw2_function = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, x, self.Pw1, self.Tw1, "H2O") - m_flow*self.Dh41
        self.Tw2 = tf.secant(a = self.Tw1, b = self.T4, f = tw2_function, tol = 1e-3)[0]
        self.Pw2 = self.Pw1
        [self.W_in, self.W_out, self.Q_in, self.Q_out] = m_flow*array([self.win, self.wout, self.qin, self.qout])
        self.W_net = self.W_out - self.W_in
        self.PR = self.P3/self.P4
        self.nth = self.W_net/self.Q_in
        self.n_carnot = 1 - self.Tw1/self.Th1

        return self.W_net, self.Th2 - self.T2


    def maximum_mass_flow(self):
        self.Pinch_evap, self.Pinch_cond = self.Pinch_evap_init, self.Pinch_cond__init
        F = lambda x: [self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(x[1], self.fluid) + self.Pinch_evap + self.DoSH, self.y_exh, self.subs_exh, "ideal") - x[0]*tf.enthalpy_vap("mass", x[1], self.fluid),
        self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, tf.T_satur(x[1], self.fluid) - self.Pinch_cond - self.DoSC, self.Pw1, self.Tw1, "H2O") - x[0]*tf.enthalpy_vap("mass", x[1], self.fluid)]
        x1 = array([1, self.P_min + 1/3*(self.P_max - self.P_min)])
        x2 = array([2, self.P_min + 1/2*(self.P_max - self.P_min)])
        x3 = array([5, self.P_min + 2/3*(self.P_max - self.P_min)])
        x_n = tf.general_secant(x1,x2,x3,F, 1e-6, 'only_possitive')[0]
        m_flow_max1, P3 = x_n
        try: 
            m_flow_max2 = tf.alternative_secant(0.1*m_flow_max1,0.2*m_flow_max1,lambda x: self.Cycle_Dry_States(x)[1] - self.Pinch_evap_init,1e-5, 'below_max')[0]
        except:
            m_flow_max2 = m_flow_max1
        m_flow_max = min([m_flow_max1, m_flow_max2])

        # print('PR constrain : m_max_1 = {:.3f} kg/s  ,  pinch point constrain : m_max_2 = {:.3f} kg/s'.format(m_flow_max1, m_flow_max2))

        return m_flow_max

    def mass_flow_optimisation(self):
        m_flow_max = self.maximum_mass_flow()
        self.m_flow = tf.goldenOpt(a = 0.1*m_flow_max, b = 0.99*m_flow_max, f = lambda x: self.Cycle_Dry_States(x)[0], tol = 1e-6)[0]


if __name__ == '__main__':
    tc = Thermodynamic_Cycle()