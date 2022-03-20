import thermo_funcs as tf
from numpy import array, linspace, isnan

class Thermodynamic_Cycle:
    def __init__(self) -> None:
        self.Th1, self.Ph1 = 450 + 273.15, 0.989*1e5
        self.mh_flow = 19.2
        self.fluid = "ETHANOL"
        self.Tw1, self.Pw1 = 15 + 273.15, 101325
        self.mw_flow = 10
        self.Pinch_evap_init, self.Pinch_cond__init = 5, 5
        self.DoSC_init, self.DoSH_init = 0, 0
        self.y_exh = [0.657, 0.158, 0.103, 0.072]
        self.subs_exh = ["N2", "CO2", "H2O", "O2"]
        self.WorkingFluidCoolProp = ["CYCLOHEX", "ETHANOL", "ISOBUTAN", "IPENTANE", "MDM", "R245FA", "TOLUENE"]
        self.WorkingFluidType = ["Dry", "Wet", "Dry","Dry", "Dry", "Dry", "Dry"]

    def working_fluid_selection(self) -> None:
        self.P_crit, self.T_crit = tf.critical_pres(self.fluid), tf.critical_temp(self.fluid)
        self.P_min = tf.reference_data(self.fluid, 'Pmin')
        self.P_max = tf.alternative_secant(self.P_min, self.P_crit*0.9, lambda x: tf.T_satur(x, self.fluid) - self.Th1, 1e-3)[0]
        if self.P_max > 0.9*self.P_crit or isnan(self.P_max) == True: self.P_max = 0.9*self.P_crit

    def Cycle_Dry_States(self,m_flow,**kwargs):
        self.working_fluid_selection()
        self.Pinch_evap, self.Pinch_cond = self.Pinch_evap_init, self.Pinch_cond__init
        self.DoSC, self.DoSH = self.DoSC_init, self.DoSH_init
        pinch_evap_fun = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(x, self.fluid) + self.Pinch_evap + self.DoSH, self.y_exh, self.subs_exh, "ideal") - m_flow*tf.enthalpy_vap("mass", x, self.fluid)
        
        if self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(self.P_crit*0.9, self.fluid) + self.Pinch_evap, self.y_exh, self.subs_exh, "ideal") > m_flow*tf.enthalpy_vap("mass", self.P_crit*0.9, self.fluid):
            self.P3 = 0.9*self.P_crit
            self.T_evap = tf.T_satur(self.P3, self.fluid)
            self.T3 = self.Th1 - self.Pinch_evap
            self.DoSH = self.T3 - self.T_evap
            thfpp_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", self.P3, self.fluid) + tf.enthalpy("mass", self.P3, self.T3, self.P3, self.T_evap, self.fluid))
            self.Thf_pp = tf.secant(self.Tw1, self.Th1, thfpp_function, 1e-3)[0]
            if self.Thf_pp < self.T_evap + self.Pinch_evap:
                self.Thf_pp = self.T_evap + self.Pinch_evap
                T3_fun = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, self.Thf_pp, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", self.P3, self.fluid) + tf.enthalpy("mass", self.P3, x, self.P3, self.T_evap, self.fluid))
                self.T3 = tf.secant(self.Tw1, self.Th1, T3_fun, 1e-3)[0]
                self.DoSH = self.T3 - self.T_evap
        else:        
            self.P3 = tf.secant(a = self.P_min, b = self.P_max, f = pinch_evap_fun, tol = 1e-3)[0]
            self.T3 = tf.T_satur(self.P3, self.fluid)
            self.T_evap = tf.T_satur(self.P3, self.fluid)
            thfpp_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", self.P3, self.fluid) + tf.enthalpy("mass", self.P3, self.T3, self.P3, self.T_evap, self.fluid))
            self.Thf_pp = tf.secant(self.Tw1, self.Th1, thfpp_function, 1e-3)[0]
        self.Z3 = tf.compressibility_factor(self.P3, self.T3, self.fluid)

        pinch_cond_fun = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, tf.T_satur(x, self.fluid) - self.Pinch_cond - self.DoSC, self.Pw1, self.Tw1, "H2O") - m_flow*tf.enthalpy_vap("mass", x, self.fluid)
        self.P1 = tf.secant(a = self.P_min, b = self.P_max, f = pinch_cond_fun, tol = 1e-3)[0]
        self.T1 = tf.T_satur(self.P1, self.fluid)
        self.T_cond = self.T1 + self.DoSC

        self.P4 = self.P1
        self.T4 = tf.secant(a = self.Tw1,b = self.Th1,f = lambda x: tf.entropy("mass",self.P4, x, self.P3, self.T3, self.fluid) ,tol = 1e-3)[0]
        self.Z4 = tf.compressibility_factor(self.P4, self.T4, self.fluid)
        self.Dh34 = tf.enthalpy("mass", self.P3, self.T3, self.P4, self.T4, self.fluid)
        self.wout = self.Dh34

        self.h_ref, self.s_ref = tf.reference_data(self.fluid, 'H'), tf.reference_data(self.fluid, 'S')
        self.h1 = tf.enthalpy_liquid("mass", self.P1, self.T1, 101325, 298.15, self.fluid) + self.h_ref
        self.s1 = tf.entropy_liquid("mass", self.P1, self.T1, 101325, 298.15, self.fluid) + self.s_ref
        self.P2 = self.P3
        self.T2 = tf.secant(self.T1,self.T3,lambda x: tf.entropy_liquid("molar",self.P2, x, self.P1, self.T1, self.fluid) ,1e-3)[0]
        self.Dh12 = tf.enthalpy_liquid("mass", self.P2, self.T2, self.P1, self.T1, self.fluid)
        self.h2 = self.h1 + self.Dh12
        self.s2 = self.s1
        self.win = self.Dh12
        self.Dh23 = tf.enthalpy_liquid("mass", self.P3, self.T3, self.P2, self.T2, self.fluid) + tf.enthalpy_vap("mass", self.P3, self.fluid)
        self.Ds23 = tf.entropy('mass', self.P2, self.T3, self.P2, self.T2, self.fluid)
        self.s3 = self.s2 + self.Ds23
        self.qin = self.Dh23
        self.h3 = self.h2 + self.Dh23
        self.h4 = self.h3 - self.Dh34
        self.s4 = self.s3
        self.Dh41 = tf.enthalpy("mass", self.P4, self.T4, self.P1, self.T1, self.fluid) + tf.enthalpy_vap("mass", self.P1, self.fluid)
        self.qout = self.Dh41

        th2_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*self.Dh23
        self.Th2 = tf.alternative_secant(self.Tw1, self.Th1, th2_function, 1e-3)[0]
        tw2_function = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, x, self.Pw1, self.Tw1, "H2O") - m_flow*self.Dh41
        self.Tw2, self.xw2 = tf.alternative_secant(self.Tw1, self.T4, tw2_function, 1e-3)[0], 0
        if self.Tw2 > tf.T_satur(self.Pw1, 'H2O'):
            self.Tw2 = tf.T_satur(self.Pw1, 'H2O')
            xw2_function = lambda x: self.mw_flow*(tf.enthalpy_liquid("mass", self.Pw1, self.Tw2, self.Pw1, self.Tw1, "H2O") + x*tf.enthalpy_vap('mass', self.Pw1, 'H2O')) - m_flow*self.Dh41
            self.xw2 = tf.alternative_secant(0, 1, xw2_function, 1e-5)[0]
        [self.W_in, self.W_out, self.Q_in, self.Q_out] = m_flow*array([self.win, self.wout, self.qin, self.qout])
        self.W_net = self.W_out - self.W_in
        self.PR = self.P3/self.P4
        self.nth = self.W_net/self.Q_in
        self.n_carnot = 1 - self.Tw1/self.Th1
        self.Ph2, self.Pw2 = self.Ph1, self.Pw1

        return self.W_net, self.Th2 - self.T2

    def Cycle_Wet_States(self,m_flow,**kwargs):
        self.working_fluid_selection()
        self.Pinch_evap, self.Pinch_cond = self.Pinch_evap_init, self.Pinch_cond__init
        self.DoSC, self.DoSH = self.DoSC_init, self.DoSH_init
        
        pinch_cond_fun = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, tf.T_satur(x, self.fluid) - self.Pinch_cond - self.DoSC, self.Pw1, self.Tw1, "H2O") - m_flow*tf.enthalpy_vap("mass", x, self.fluid)
        self.P1 = tf.secant(a = self.P_min, b = self.P_max, f = pinch_cond_fun, tol = 1e-3)[0]
        self.T1 = tf.T_satur(self.P1, self.fluid)
        self.T_cond = self.T1 + self.DoSC

        pinch_evap_fun = lambda x: [self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(x[0], self.fluid) + self.Pinch_evap, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", x[0], self.fluid) + tf.enthalpy("mass", x[0], tf.T_satur(x[0], self.fluid) + x[1], x[0], tf.T_satur(x[0], self.fluid), self.fluid)), 
        tf.entropy_gas_specified('mass', x[0], self.fluid) + tf.entropy('mass', x[0], tf.T_satur(x[0], self.fluid) + x[1], x[0], tf.T_satur(x[0], self.fluid), self.fluid) - tf.entropy_gas_specified('mass', self.P1, self.fluid)]
        [self.P3, self.DoSH] = tf.general_secant([self.P_min, 10], [(self.P_min + self.P_max)/3, 5], [(self.P_min + self.P_max)/2, 1], pinch_evap_fun, 1e-3, 'only_possitive')[0]
        self.T_evap = tf.T_satur(self.P3, self.fluid)
        self.T3 = tf.T_satur(self.P3, self.fluid) + self.DoSH

        if self.P3 > self.P_max:
            self.P3 = self.P_max
            self.T_evap = tf.T_satur(self.P3, self.fluid)
            dosh_fun = lambda x: tf.entropy_gas_specified('mass', self.P3, self.fluid) + tf.entropy('mass', self.P3, tf.T_satur(self.P3, self.fluid) + x, self.P3, tf.T_satur(self.P3, self.fluid), self.fluid) - tf.entropy_gas_specified('mass', self.P1, self.fluid)
            self.DoSH = tf.alternative_secant(0.5, 10, dosh_fun, 1e-3, 'only_possitive')[0]
            self.T3 = self.T_evap + self.DoSH
            thfpp_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", self.P3, self.fluid) + tf.enthalpy("mass", self.P3, self.T3, self.P3, self.T_evap, self.fluid))
            self.Thf_pp = tf.secant(a = self.Tw1, b = self.Th1, f = thfpp_function, tol = 1e-3)[0]
            self.Pinch_evap = self.Thf_pp - self.T_evap

        if self.T3 + self.Pinch_evap > self.Th1:
            self.T3 = self.Th1 - self.Pinch_evap
            p3wet_function = lambda x: tf.entropy_gas_specified('mass', x, self.fluid) + tf.entropy('mass', x, self.T3, x, tf.T_satur(x, self.fluid) , self.fluid) - tf.entropy_gas_specified('mass', self.P1, self.fluid)
            self.P3 = tf.alternative_secant(self.P_min, self.P_max, p3wet_function, 1e-3, 'only_possitive')[0]
            self.T_evap = tf.T_satur(self.P3, self.fluid)
            self.DoSH = self.T3 - self.T_evap
        thfpp_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*(tf.enthalpy_vap("mass", self.P3, self.fluid) + tf.enthalpy("mass", self.P3, self.T3, self.P3, self.T_evap, self.fluid))
        self.Thf_pp = tf.secant(a = self.Tw1, b = self.Th1, f = thfpp_function, tol = 1e-3)[0]
        
        self.Z3 = tf.compressibility_factor(self.P3, self.T3, self.fluid)

        self.P4 = self.P1
        self.T4 = tf.secant(a = self.Tw1,b = self.Th1,f = lambda x: tf.entropy("mass",self.P4, x, self.P3, self.T3, self.fluid) ,tol = 1e-3)[0]
        self.Z4 = tf.compressibility_factor(self.P4, self.T4, self.fluid)
        self.Dh34 = tf.enthalpy("mass", self.P3, self.T3, self.P4, self.T4, self.fluid)
        self.wout = self.Dh34

        self.h_ref, self.s_ref = tf.reference_data(self.fluid, 'H'), tf.reference_data(self.fluid, 'S')
        self.h1 = tf.enthalpy_liquid("mass", self.P1, self.T1, 101325, 298.15, self.fluid) + self.h_ref
        self.s1 = tf.entropy_liquid("mass", self.P1, self.T1, 101325, 298.15, self.fluid) + self.s_ref
        self.P2 = self.P3
        self.T2 = tf.secant(self.T1,self.T3,lambda x: tf.entropy_liquid("molar",self.P2, x, self.P1, self.T1, self.fluid) ,1e-3)[0]
        self.Dh12 = tf.enthalpy_liquid("mass", self.P2, self.T2, self.P1, self.T1, self.fluid)
        self.h2 = self.h1 + self.Dh12
        self.s2 = self.s1
        self.win = self.Dh12
        self.Dh23 = tf.enthalpy_liquid("mass", self.P3, self.T3, self.P2, self.T2, self.fluid) + tf.enthalpy_vap("mass", self.P3, self.fluid)
        self.Ds23 = tf.entropy('mass', self.P2, self.T3, self.P2, self.T2, self.fluid)
        self.s3 = self.s2 + self.Ds23
        self.qin = self.Dh23
        self.h3 = self.h2 + self.Dh23
        self.h4 = self.h3 - self.Dh34
        self.s4 = self.s3
        self.Dh41 = tf.enthalpy("mass", self.P4, self.T4, self.P1, self.T1, self.fluid) + tf.enthalpy_vap("mass", self.P1, self.fluid)
        self.qout = self.Dh41

        th2_function = lambda x: self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1, self.Ph1, x, self.y_exh, self.subs_exh, "ideal") - m_flow*self.Dh23
        self.Th2 = tf.secant(a = self.Tw1, b = self.Th1, f = th2_function, tol = 1e-3)[0]
        tw2_function = lambda x: self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, x, self.Pw1, self.Tw1, "H2O") - m_flow*self.Dh41
        self.Tw2 = tf.secant(a = self.Tw1, b = self.T4, f = tw2_function, tol = 1e-3)[0]
        [self.W_in, self.W_out, self.Q_in, self.Q_out] = m_flow*array([self.win, self.wout, self.qin, self.qout])
        self.W_net = self.W_out - self.W_in
        self.PR = self.P3/self.P4
        self.nth = self.W_net/self.Q_in
        self.n_carnot = 1 - self.Tw1/self.Th1
        self.Ph2, self.Pw2 = self.Ph1, self.Pw1

        return self.W_net, self.Th2 - self.T2

    def maximum_mass_flow(self):
        self.DoSC, self.DoSH = self.DoSC_init, self.DoSH_init
        self.working_fluid_selection()
        self.Pinch_evap, self.Pinch_cond = self.Pinch_evap_init, self.Pinch_cond__init
        F = lambda x: [self.mh_flow*tf.enthalpy_mix("mass", self.Ph1, self.Th1 , self.Ph1, tf.T_satur(x[1], self.fluid) + self.Pinch_evap + self.DoSH, self.y_exh, self.subs_exh, "ideal") - x[0]*tf.enthalpy_vap("mass", x[1], self.fluid),
        self.mw_flow*tf.enthalpy_liquid("mass", self.Pw1, tf.T_satur(x[1], self.fluid) - self.Pinch_cond - self.DoSC, self.Pw1, self.Tw1, "H2O") - x[0]*tf.enthalpy_vap("mass", x[1], self.fluid)]
        x1 = array([1, self.P_min + 1/3*(self.P_max - self.P_min)])
        x2 = array([2, self.P_min + 1/2*(self.P_max - self.P_min)])
        x3 = array([5, self.P_min + 2/3*(self.P_max - self.P_min)])
        x_n = tf.general_secant(x1,x2,x3,F, 1e-6, 'only_possitive')[0]
        m_flow_max1, P3 = x_n
        m_flow_max2 = tf.alternative_secant(0.1*m_flow_max1,0.2*m_flow_max1,lambda x: self.Cycle_Dry_States(x)[1] - self.Pinch_evap_init,1e-5)[0]
        if m_flow_max1 < 1 and m_flow_max1 < m_flow_max2:
            m_flow_max1 = m_flow_max2
        m_flow_max = min([m_flow_max1, m_flow_max2])

        print('PR constrain : m_max_1 = {:.3f} kg/s  ,  pinch point constrain : m_max_2 = {:.3f} kg/s'.format(m_flow_max1, m_flow_max2))

        return m_flow_max

    def mass_flow_optimisation(self):
        m_flow_max = self.maximum_mass_flow()
        if self.WorkingFluidType[self.WorkingFluidCoolProp.index(self.fluid)] == "Dry":
            opt_func = lambda x: self.Cycle_Dry_States(x)[0]
        elif self.WorkingFluidType[self.WorkingFluidCoolProp.index(self.fluid)] == "Wet":
            opt_func = lambda x: self.Cycle_Wet_States(x)[0]
        self.m_flow = tf.goldenOpt(a = 0.1*m_flow_max, b = 0.9*m_flow_max, f = opt_func, tol = 1e-6)[0]

        
if __name__ == '__main__':
    tc = Thermodynamic_Cycle()
    tc.m_flow = tc.maximum_mass_flow()
    # tc.mass_flow_sensitivity()
    tc.m_flow = 2
    tc.Cycle_Dry_States(tc.m_flow)
