from kivymd.app import MDApp
from kivy.clock import mainthread, Clock
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, NoTransition, SlideTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd import images_path
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
import time
import threading
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
import config as cf
import os
from numpy import sqrt, polyval
from thermo_cycle import Thermodynamic_Cycle
import thermo_funcs as tf
import cProfile
from kivy.metrics import dp
from functools import partial

os.environ["KIVY_NO_CONFIG"] = "1"

Window.fullscreen = True
# Window.size = (350, 650)

class Content(MDBoxLayout):
    pass

class ContentCustomSheet(MDBoxLayout):
    divider = None
    title = StringProperty()
    text = StringProperty()
    
class EvaporatorPropCustomSheet(MDBoxLayout):
    divider = None
    title = StringProperty()
    text = StringProperty()
    image = StringProperty()

class WorkingFluidInfoSheet(MDBoxLayout):
    pass
    
class RotorCustomSheet(MDBoxLayout):
    divider = None
    title = StringProperty()
    text = StringProperty()

    
class NozzleCustomSheet(MDBoxLayout):
    pass

class StatorBladeCustomSheet(MDBoxLayout):
    pass

class StatorSectionAbCustomSheet(MDBoxLayout):
    pass

class StatorR2R1CustomSheet(MDBoxLayout):
    pass

class PolytropicIndexCustomSheet(MDBoxLayout):
    pass
        

    
class Thermotab1(BoxLayout, MDTabsBase):
    
    workingfluidbutton = ObjectProperty(None)
    WorkingFluid = ObjectProperty(None)
    thermotab2 = ObjectProperty(None)
    thermotab3 = ObjectProperty(None)
    fluidtypetext = ObjectProperty(None)
    fluidtypeimage = ObjectProperty(None)
    mflowsldr = ObjectProperty(None)
    mflowplus = ObjectProperty(None)
    mflowminus = ObjectProperty(None)
    mflowreset = ObjectProperty(None)
    mflowround = ObjectProperty(None)

    def callback_for_workingfluid_items(self, *args):
        app = App.get_running_app()
        self.WorkingFluid = self.WorkingFluidCoolProp[self.WorkingFluidData.index(args[0])]
        self.workingfluidbutton.text = "Working Fluid : {}".format(args[0])
        self.fluidtypetext.text = " Fluid Type : {}".format(self.WorkingFluidType[self.WorkingFluidData.index(args[0])])
        self.fluidtypeimage.source = "Ts_{}.png".format(self.WorkingFluidType[self.WorkingFluidData.index(args[0])])
        self.ashrae34field.text = "    None"
        self.gwp100field.text = "    None"
        self.odpfield.text = "None"
        cf.WFLUID = "Working Fluid : {}".format(args[0])
        cf.WorkingFluid = self.WorkingFluid

    def show_workingfluidinfo_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.WorkingFluidInfoSheet())
        self.custom_sheet.open()
        
    def WorkingFluid_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet()
        self.WorkingFluidData = ["Cyclohexane", "Ethanol", "Isobutane", "Isopentane", "MDM", "R245fa", "Toluene"]
        self.WorkingFluidCoolProp = ["CYCLOHEX", "ETHANOL", "ISOBUTAN", "IPENTANE", "MDM", "R245FA", "TOLUENE"]
        self.WorkingFluidType = ["Dry", "Wet", "Dry","Dry", "Dry", "Dry", "Dry"]
                
        for i in range(0, len(self.WorkingFluidData)):
            bottom_sheet_menu.add_item(
                self.WorkingFluidData[i],
                lambda x, y=i: self.callback_for_workingfluid_items(self.WorkingFluidData[y]))
        bottom_sheet_menu.open()
        
    def OptActivate(self):
        if self.massflowopt.active == True:
            self.mflow.disabled = True
            self.mflowsldr.disabled = True
            self.mflowminus.disabled = True
            self.mflowplus.disabled = True
            self.mflowreset.disabled = True
            self.mflowround.disabled = True
            self.mflowtext.text_color = [128/255,128/255,128/255, 1]
        else:
            self.mflow.disabled = False
            self.mflowsldr.disabled = False
            self.mflowminus.disabled = False
            self.mflowplus.disabled = False
            self.mflowreset.disabled = False
            self.mflowround.disabled = False
            self.mflowtext.text_color = [0.28, 0.39, 0.63, 1]


class Thermotab2(BoxLayout, MDTabsBase):
    app = App.get_running_app()
    th1 = ObjectProperty(None)
    th1sldr = ObjectProperty(None)
    itemhotinlettemp = ObjectProperty(None)
    itemhotinletpres = ObjectProperty(None)
    itemhotmflow = ObjectProperty(None)
    ph1sldr = ObjectProperty(None)
    mhflowsldr = ObjectProperty(None)
    ph1 = ObjectProperty(None)
    mhflow = ObjectProperty(None)
    th2 = ObjectProperty(None)
    ph2 = ObjectProperty(None)
    tw1= ObjectProperty(None)
    pw1 = ObjectProperty(None)
    mwflow = ObjectProperty(None)
    tw2 = ObjectProperty(None)
    pw2 = ObjectProperty(None)
    t1 = ObjectProperty(None)
    p1 = ObjectProperty(None)
    t2 = ObjectProperty(None)
    p2 = ObjectProperty(None)
    t21 = ObjectProperty(None)
    p21 = ObjectProperty(None)
    t3 = ObjectProperty(None)
    p3 = ObjectProperty(None)
    t4 = ObjectProperty(None)
    t4s = ObjectProperty(None)
    p4 = ObjectProperty(None)
    pinchevap = ObjectProperty(None)
    dosh = ObjectProperty(None)
    pinchcond = ObjectProperty(None)
    dosc = ObjectProperty(None)
    nn2 = ObjectProperty(None)
    nco2 = ObjectProperty(None)
    nh2o = ObjectProperty(None)
    no2 = ObjectProperty(None)
    npump = ObjectProperty(None)
    thermotab1 = ObjectProperty(None)
    thermotab3 = ObjectProperty(None)
    HeatSource = ObjectProperty(None)
    pinchevapsldr = ObjectProperty(None)
    doshsldr = ObjectProperty(None)
    resetpinchcond = ObjectProperty(None)
    pinchcond = ObjectProperty(None)
    pinchcondsldr = ObjectProperty(None)
    resetdosc = ObjectProperty(None)
    dosc = ObjectProperty(None)
    doscsldr = ObjectProperty(None)
    tw1sldr = ObjectProperty(None)
    pw1sldr = ObjectProperty(None)
    mwflowsldr = ObjectProperty(None)
    npumpsldr = ObjectProperty(None)
    nturb = ObjectProperty(None)
    nturbsldr = ObjectProperty(None)

    
    def show_evap_custom_bottom_sheet(self, choice):
        def get_title(i):
            switcher={
                "pinchpoint":"Pinch Point",
                "dosh":"Degrees of superheat"}
            return str(switcher.get(i))
        
        def get_text(i):
            switcher={
                "pinchpoint":"Select the pinch point of the cycle. The pinch point is in fact the minimum temperature in the evaporator between the cold side (Working Fluid) and the hot side (Heat Source). In our case the pinch point is the difference between the evaporation temperature and the outlet temperature of the heat source. The pinch point value is fixed when it's necessary, in order to ensure that the evaporation temperature is lower than the critical temperature",
                "dosh": "Selete the degrees of superheat in the thermodynamic cycle. The degrees of superheat is the temperature increase in the superheated vapor region, from the evaporation temperature for the given pressure. The degrees of superheat value is fixed when it's necessary, in order to ensure that the expansion happens in the vapor region"}
            return str(switcher.get(i))
        
        def get_image(i):
            switcher={
                "pinchpoint":"ThermPinchPoint.JPG",
                "dosh": "ThermDosh.JPG"}
            return str(switcher.get(i))
        
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.EvaporatorPropCustomSheet(title = get_title(choice), text = get_text(choice), image = get_image(choice)))
        self.custom_sheet.open()
    
    def callback_for_heatsource_items(self, *args):
        app = App.get_running_app()
        self.HeatSource = self.HeatSourceCoolProp[self.HeatSourceData.index(args[0])]
        self.heatsourcebutton.text = "Heat Source : {}".format(args[0])
        if args[0] == "Exhaust Gases":
            self.dialog = MDDialog(
                title="[color={}][b] Composition [/b][/color]".format("#4863A0"),
                type="confirmation",
                items=[
                    ItemIndDialog(var="nN2",value="0.657"),
                    ItemIndDialog(var="nCO2",value="0.168"),
                    ItemIndDialog(var="nH2O",value="0.103"),
                    ItemIndDialog(var="nO2",value="0.072")],
                buttons=[
                    MDRaisedButton(text="OK", text_color=(1,1,1,1), on_release=self.close_and_save_ind),
                    MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog),
                ],size_hint=(0.75,1))
            cf.comp_dialog = self.dialog
            self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()
        
    def close_and_save_ind(self,obj):
        [self.nN2, self.nCO2, self.nH2O, self.nO2] = [float(self.dialog.items[x].comptext.text) for x in range(0,len(self.dialog.items))]
        print(self.nN2, self.nCO2, self.nH2O, self.nO2)
        self.dialog.dismiss()
        
    def HeatSource_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet()
        self.HeatSourceData = ["Exhaust Gases","Water/Steam"]
        self.HeatSourceCoolProp = ["NITROGEN&CO2&WATER&OXYGEN","WATER"]
        for i in range(0, len(self.HeatSourceData)):
            bottom_sheet_menu.add_item(
                self.HeatSourceData[i],
                lambda x, y=i: self.callback_for_heatsource_items(self.HeatSourceData[y]))
        bottom_sheet_menu.open()

                
class Thermotab3(BoxLayout, MDTabsBase):
    app = App.get_running_app()
    pr = ObjectProperty(None)
    qin = ObjectProperty(None)
    wout = ObjectProperty(None)
    win = ObjectProperty(None)
    wnet = ObjectProperty(None)
    nth = ObjectProperty(None)
    ncar = ObjectProperty(None)
    mflowres = ObjectProperty(None)
    presscalculate = ObjectProperty(None)
    ThermCalcCompleted = ObjectProperty(None)
    thermotab1 = ObjectProperty(None)
    thermotab2 = ObjectProperty(None)
    thermspinner = ObjectProperty(None)
    dosh_change = False


    @mainthread
    def spinner_toggle(self):
        if self.thermspinner.active == False:
            self.thermspinner.active = True
        else:
            self.thermspinner.active = False
     
    @mainthread
    def ThermFinish(self):
        if self.Error_Type == 1:
            if self.thermotab1.WorkingFluid == None and self.thermotab2.HeatSource != None: textmsg = "Please select Working Fluid"
            elif self.thermotab1.WorkingFluid != None and self.thermotab2.HeatSource == None: textmsg = "Please select Heat Source"
            else: textmsg = "Please select Working Fluid and type of Heat Source"
            self.dialog = MDDialog(
            title="[color={}][b] Not Enough Inputs [/b][/color]".format("#4863A0"),
            text=textmsg,
            buttons=[MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog),],size_hint=(0.75,1))
            self.dialog.open()
        elif self.Error_Type == 2:
            self.dialog = MDDialog(
            title="[color={}][b] Calculation Error [/b][/color]".format("#4863A0"),
            text="Too high mass flow. For the given inlet conditions mass flow can not be higher than {:.3f} kg/s".format(self.m_flow_max),
            buttons=[MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog),],size_hint=(0.75,1))
            self.dialog.open()
        elif self.Error_Type == 0:
            self.unexpected_error(self.exc)
        else:
            self.snackbar = Snackbar(text="Calculations completed!",snackbar_x=dp(0),snackbar_y=dp(10), duration=0.2)
            self.snackbar.open()
            if self.dosh_change == True:

                Clock.schedule_once(partial(self.my_callback), 1.5)

    def my_callback(self, obj):
        self.snackbar_dosh = Snackbar(text="Deg. of Superheating value changed",snackbar_x=dp(0),snackbar_y=dp(10))
        self.snackbar_dosh.open()

    def ThermCalculations(self):
        Error = False
        self.Error_Type = None
        self.dosh_change = False
        try:
            if self.thermotab1.WorkingFluid == None or self.thermotab2.HeatSource == None:
                self.Error_Type = 1   
                Error = True

            if Error == False:
                self.tc = Thermodynamic_Cycle()
                self.tc.Th1, self.tc.Ph1 = float(self.thermotab2.th1.text) + 273.15, float(self.thermotab2.ph1.text)*1e5
                self.tc.mh_flow = float(self.thermotab2.mhflow.text)
                self.tc.fluid = self.thermotab1.WorkingFluid
                self.tc.Tw1, self.tc.Pw1 = float(self.thermotab2.tw1.text) + 273.15, float(self.thermotab2.pw1.text)*1e5
                self.tc.mw_flow = float(self.thermotab2.mwflow.text)
                self.tc.Pinch_evap_init, self.tc.Pinch_cond__init = float(self.thermotab2.pinchevap.text), float(self.thermotab2.pinchcond.text)
                self.tc.DoSC_init, self.tc.DoSH_init = float(self.thermotab2.dosc.text), float(self.thermotab2.dosh.text)
                self.tc.y_exh = [0, 0, 1, 0] if self.thermotab2.HeatSource == "WATER" else [self.thermotab2.nN2, self.thermotab2.nCO2, self.thermotab2.nH2O, self.thermotab2.nO2]
                self.tc.m_flow = float(self.thermotab1.mflow.text)
                self.tc.nturb, self.tc.npump = float(self.thermotab2.nturb.text), float(self.thermotab2.npump.text)

                self.m_flow_max = self.tc.maximum_mass_flow()
                if self.thermotab1.massflowopt.active == True:
                    self.tc.mass_flow_optimisation()
                else:
                    if self.tc.m_flow <= self.m_flow_max:
                        if self.thermotab1.WorkingFluidType[self.thermotab1.WorkingFluidCoolProp.index(self.tc.fluid)] == "Dry":
                            self.tc.Cycle_Dry_States(self.tc.m_flow)
                        elif self.thermotab1.WorkingFluidType[self.thermotab1.WorkingFluidCoolProp.index(self.tc.fluid)] == "Wet":
                            self.tc.Cycle_Wet_States(self.tc.m_flow)
                    else:
                        self.Error_Type = 2
                        Error = True
            if Error == False:
                if self.tc.DoSH > self.tc.DoSH_init: self.dosh_change = True
                self.thermotab2.th2.text, self.thermotab2.ph2.text = "{:.2f}".format(self.tc.Th2-273.15), "{:.3f}".format(self.tc.Ph2/1e5)
                self.thermotab2.tw2.text, self.thermotab2.pw2.text = "{:.2f}".format(self.tc.Tw2-273.15), "{:.3f}".format(self.tc.Pw2/1e5)
                self.thermotab2.dosh.text, self.thermotab2.pinchevap.text = "{:.2f}".format(self.tc.DoSH), "{:.2f}".format(self.tc.Pinch_evap) 
                self.thermotab2.t1.text, self.thermotab2.p1.text = "{:.2f}".format(self.tc.T1-273.15), "{:.3f}".format(self.tc.P1/1e5)
                self.thermotab2.t2.text, self.thermotab2.p2.text = "{:.2f}".format(self.tc.T2-273.15), "{:.3f}".format(self.tc.P2/1e5)
                self.thermotab2.t21.text, self.thermotab2.p21.text = "{:.2f}".format(self.tc.T2-273.15), "{:.3f}".format(self.tc.P2/1e5)
                self.thermotab2.t3.text, self.thermotab2.p3.text = "{:.2f}".format(self.tc.T3-273.15), "{:.3f}".format(self.tc.P3/1e5)
                self.thermotab2.t4.text, self.thermotab2.p4.text, self.thermotab2.t4s.text = "{:.2f}".format(self.tc.T4-273.15), "{:.3f}".format(self.tc.P4/1e5), "{:.2f}".format(self.tc.T4s-273.15)
                self.thermotab2.doshsldr.value, self.thermotab2.pinchevapsldr.value = float(self.tc.DoSH), float(self.tc.Pinch_evap)
                self.pr.text = "Pressure Ratio : {:.3f} [-]".format(self.tc.PR)
                self.wout.text = "Turbine Power Output : {:.2f} [kW]".format(self.tc.W_out/1e3)
                self.win.text = "Pump Power Input : {:.2f} [kW]".format(self.tc.W_in/1e3); 
                self.wnet.text = "Net Power Output : {:.2f} [kW]".format(self.tc.W_net/1e3)
                self.qin.text = "Heat Duty : {:.2f} [kW]".format(self.tc.Q_in/1e3)
                self.nth.text = "Thermal Efficiency : {:.2f} [%]".format(self.tc.nth*1e2)
                self.mflowres.text = "Mass Flow : {:.2f} [kg/s]".format(self.tc.m_flow)
                self.ncarnot.text = "Carnot Efficiency : {:.2f} [%]".format(self.tc.n_carnot*1e2)
                self.thermotab1.mflow.text = "{:.2f}".format(self.tc.m_flow)
                self.thermotab1.mflowsldr.value = float(self.tc.m_flow)
                self.ThermCalcCompleted = 'Completed'

        except Exception as exc:
            self.exc = exc
            Error = True
            self.Error_Type = 0

        self.ThermFinish()
        self.spinner_toggle()

    def unexpected_error(self, exc):
        self.dialog = MDDialog(
        title="[color={}][b] Calculation Error [/b][/color]".format("#4863A0"),
        text="Oops. An unexpeted error seems to have been appeared. We are working on that. Please select some other inputs for the calculations. Error : {}".format(exc),
        buttons=[MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog),],size_hint=(0.75,1))
        self.dialog.open()

    def ThermCalculations_thread(self):
        if self.dosh_change == True and round(self.tc.DoSH,2) == float(self.thermotab2.dosh.text):
                self.dialog_warning = MDDialog(
                title="[color={}][b] Warning [/b][/color]".format("#4863A0"),
                text="Degrees of Superheating have changed during previous calculation. Do you want to keep to new value or to reset to the initial value?",
                buttons=[MDFlatButton(text="RESET", text_color=(0.28, 0.39, 0.63, 1), on_release=self.reset_button),
                MDFlatButton(text="KEEP", text_color=(0.28, 0.39, 0.63, 1), on_release=self.keep_button)],size_hint=(0.9,1))
                self.dialog_warning.open()
        else:
            self.spinner_toggle()
            self.therm_thread = threading.Thread(target=(self.ThermCalculations))
            self.therm_thread.start()
              
            
    def reset_button(self,obj) -> None:
        self.thermotab2.dosh.text = "{:.2f}".format(0)
        self.thermotab2.doshsldr.value = float(0)
        self.close_dialog_warning(None)
        self.ThermCalculations_thread()

    def keep_button(self,obj) -> None:
        self.dosh_change = False
        self.close_dialog_warning(None)
        self.ThermCalculations_thread()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def close_dialog_warning(self,obj):
        self.dialog_warning.dismiss()
        
                
class MainScreen(Screen):
    pass
    
class InformationScreen(Screen):
    infotext = ObjectProperty(None)
    infovalue = ObjectProperty(None)
    infobar = ObjectProperty(None)
    infoimage = ObjectProperty(None)
    infocard = ObjectProperty(None)
            
    def dialog_text(self, i):
        switcher={
            0:"Simulate the Organic Rankine Cycle from the thermodynamic point of view. Determine the heat source, the heat sink and some component parameters, such as pump's isentropic efficiency and the pinch point in the evaporator and the condenser. Select the proper working fluid from a organic fluid library. Environmental and safety parameters, such as GWP100 or ODP and ASHRAE34, are connected with every working fluid, in order to show the appropriateness of the fluid selection. The app will identify then all the thermodynamic properties, in every cycle's state and will calculate the required, pressure ratio, the attributed net-power output, as well the total thermal efficiency and the Carnot efficiency",
            1:"Considering the results from the thermodynamic cycle, determine the velocity triangles of the corresponding turbine. Select the appropriate design parametres, such as the turbine's degree of reaction, the axial stage Mach number, the inlet flow angle, the hub to tip ratio and number of turbine's blades. For the given pressure ratio, calculated in the thermodynamic cycle, the absolute and relovite Mach numbers are calculated, as well with the corresponing absolute and relative angles. Note the fact that in ORC applications, supersonic turbines are selected, so the Mach number calculations are expected to be above unity, in most cases. Other calculations, such as the rotor rotational speed, the total enthlapy difference and the load and flow factors complement a complete velocity triangles calculation",
            2:"Design the stator blades of turbine, regarding the calculations of the velocity triangles. Consindering the supersonic regime in ORC applications, the stator blade is divided in 3 distinct sectors: Inlet sector, convergent sector and divergent sector. Set the preferable design parameters in every blade sector, and combined with the calculated parameters from the velocity triangles, generate the prelimenary stator geometry. Finally, export the generated geometry in a completed coordinates text file.",
            3:"Design the rotor blades of turbine, regarding the calculations of the velocity triangles. Select the proper blade design form a number of options. For supersonic regime, the impulse rotor design is considered as the most efficient rotor blade design. Set the preferable design parameters in every blade sector, and combined with the calculated parameters from the velocity triangles, generate the prelimenary rotor geometry. Finally, export the generated geometry in a completed coordinates text file"}
        return str(switcher.get(i))
    
    def title_color(self, i):
        switcher={0:"#4863A0",1:"#30A234",2:"#e65c00",3:"#7a00cc"}
        return str(switcher.get(i))
    
    def select_image(self, i):
        switcher={0:"ORCFigureLayout.JPG",1:"VelocityTriangles.png",2:"StatorBladeImage.png",3:"RotorBladeImage.png"}
        return str(switcher.get(i))

    def button_color(self, i):
        switcher={0:(0.28, 0.39, 0.63, 1),1:(0.19, 0.64, 0.20, 1),2:(0.90, 0.36, 0.0, 1),3:(0.48, 0.0, 0.80, 1)}
        return switcher.get(i)
    
    def card_height(self, i):
        switcher={0:600,1:600,2:600,3:600}
        return switcher.get(i)
        
    def on_pre_enter(self, *args):
        self.infotext.text = self.dialog_text(self.infovalue)
        self.infotext.color = self.button_color(self.infovalue)
        self.infobar.md_bg_color = self.button_color(self.infovalue)
        self.infoimage.source = self.select_image(self.infovalue)
        self.infocard.height = self.card_height(self.infovalue)


class ItemIndDialog(OneLineIconListItem):
    divider = None
    var = StringProperty()
    value = StringProperty()
    id = StringProperty()
    nn2 = ObjectProperty(None)

    def composition_check(self):
        composition = [float(cf.comp_dialog.items[x].comptext.text) for x in range(0,len(cf.comp_dialog.items))]
        if sum(composition) != 1:
            self.comp_msg = Snackbar(text="Sum of gas composition is not 1",snackbar_x="10dp",snackbar_y="10dp")
            self.comp_msg.open()

    def correct_composition(self, var):
        [nN2, nCO2, nH2O, nO2] = [float(cf.comp_dialog.items[x].comptext.text) for x in range(0,len(cf.comp_dialog.items))]
        if var == "nN2":
            cf.comp_dialog.items[0].comptext.text = "{:.3f}".format(1 - nCO2 - nH2O - nO2)
        elif var =="nCO2":
            cf.comp_dialog.items[1].comptext.text = "{:.3f}".format(1 - nN2 - nH2O - nO2)
        elif var =="nH2O":
            cf.comp_dialog.items[2].comptext.text = "{:.3f}".format(1 - nN2 - nCO2 - nO2)
        elif var == "nO2":
            cf.comp_dialog.items[3].comptext.text = "{:.3f}".format(1 - nN2 - nCO2 - nH2O)

    
class ItemThermState(OneLineIconListItem):
    divider = None
    var = StringProperty()
    value = StringProperty()
    units = StringProperty()
    
class ItemVelState(OneLineIconListItem):
    divider = None
    var = StringProperty()
    value = StringProperty()
    units = StringProperty()
    
class ItemTCArcs(OneLineIconListItem):
    divider = None
    var = StringProperty()
    value = StringProperty()
    units = StringProperty()

    
class ThermodynamicsScreen(Screen):
    mflow = ObjectProperty(None)
    th1 = ObjectProperty(None)
    ph1 = ObjectProperty(None)
    mhflow = ObjectProperty(None)
    th2 = ObjectProperty(None)
    ph2 = ObjectProperty(None)
    tw1= ObjectProperty(None)
    pw1 = ObjectProperty(None)
    mwflow = ObjectProperty(None)
    tw2 = ObjectProperty(None)
    pw2 = ObjectProperty(None)
    t1 = ObjectProperty(None)
    p1 = ObjectProperty(None)
    t2 = ObjectProperty(None)
    p2 = ObjectProperty(None)
    t21 = ObjectProperty(None)
    p21 = ObjectProperty(None)
    t3 = ObjectProperty(None)
    p3 = ObjectProperty(None)
    t4 = ObjectProperty(None)
    p4 = ObjectProperty(None)
    pr = ObjectProperty(None)
    qin = ObjectProperty(None)
    wout = ObjectProperty(None)
    win = ObjectProperty(None)
    wnet = ObjectProperty(None)
    nth = ObjectProperty(None)
    ncar = ObjectProperty(None)
    pinchevap = ObjectProperty(None)
    dosh = ObjectProperty(None)
    pinchcond = ObjectProperty(None)
    dosc = ObjectProperty(None)
    nn2 = ObjectProperty(None)
    nco2 = ObjectProperty(None)
    nh2o = ObjectProperty(None)
    no2 = ObjectProperty(None)
    npump = ObjectProperty(None)
    presscalculate = ObjectProperty(None)
    massflowopt = ObjectProperty(None)
    WorkingFluid = ObjectProperty(None)
    HeatSource = ObjectProperty(None)
    ThermCalcCompleted = ObjectProperty(None)
    Tstate = ListProperty([])
    Pstate = ListProperty([])
    rhostate = ListProperty([])
    vstate = ListProperty([])
    cstate = ListProperty([])
    hstate = ListProperty([])
    sstate = ListProperty([])
    Zstate = ListProperty([])
    Gstate = ListProperty([])
    Cpstate = ListProperty([])
    Cvstate = ListProperty([])
    snackbar = ObjectProperty(None)
    
class ThermoStateScreen(Screen):
    statebar = ObjectProperty(None)
    rho = ObjectProperty(None)
    vspec = ObjectProperty(None)
    enth = ObjectProperty(None)
    entr = ObjectProperty(None)
    soundspeed = ObjectProperty(None)
    comprfactor = ObjectProperty(None)
    fundder = ObjectProperty(None)
    cp = ObjectProperty(None)
    cv = ObjectProperty(None)
    temp = ObjectProperty(None)
    pres = ObjectProperty(None)
    
    def on_pre_enter(self, *args):
        if self.manager.screens[2].ids.thermotab3.ThermCalcCompleted == None:
            Tvalue = "None"; Pvalue = "None"; rhovalue = "None"; vvalue = "None"; hvalue = "None"; svalue = "None"; cvalue = "None"; Zvalue = "None"; Gvalue = "None"; Cpvalue = "None"
            Cvvalue = "None"
        else:
            fluid = self.manager.screens[2].ids.thermotab3.tc.fluid
            Tstates = [self.manager.screens[2].ids.thermotab3.tc.T1, self.manager.screens[2].ids.thermotab3.tc.T2, self.manager.screens[2].ids.thermotab3.tc.T3, self.manager.screens[2].ids.thermotab3.tc.T4]
            Pstates = [self.manager.screens[2].ids.thermotab3.tc.P1, self.manager.screens[2].ids.thermotab3.tc.P2, self.manager.screens[2].ids.thermotab3.tc.P3, self.manager.screens[2].ids.thermotab3.tc.P4]
            Zstates = ["N/A in liquid phase", "N/A in liquid phase", round(self.manager.screens[2].ids.thermotab3.tc.Z3,3), round(self.manager.screens[2].ids.thermotab3.tc.Z4,3)]
            Tvalue = "{:.2f}".format(Tstates[self.manager.screens[2].ids.thermotab2.statepressed - 1] - 273.15)
            Pvalue = "{:.3f}".format(Pstates[self.manager.screens[2].ids.thermotab2.statepressed - 1]/1e5)
            Zvalue = "{}".format(Zstates[self.manager.screens[2].ids.thermotab2.statepressed - 1])

            rhovalue = tf.density_liquid('mass', fluid, float(Tvalue)+273.15) if self.manager.screens[2].ids.thermotab2.statepressed <= 2 else tf.density(float(Pvalue)*1e5, float(Tvalue) + 273.15, fluid)
            vvalue = 1/rhovalue
            rhovalue, vvalue = "{:.3f}".format(rhovalue), "{:.3f}".format(vvalue)
            hvalue = tf.enthalpy_liquid('mass', float(Pvalue)*1e5, float(Tvalue) + 273.15, 101325, 298.15, fluid) if self.manager.screens[2].ids.thermotab2.statepressed <= 2 else tf.enthalpy('mass', float(Pvalue)*1e5, float(Tvalue) + 273.15, 101325, 298.15, fluid)
            svalue = tf.entropy_liquid('mass', float(Pvalue)*1e5, float(Tvalue) + 273.15, 101325, 298.15, fluid) if self.manager.screens[2].ids.thermotab2.statepressed <= 2 else tf.entropy('mass', float(Pvalue)*1e5, float(Tvalue) + 273.15, 101325, 298.15, fluid)
            hvalue, svalue = "{:.2f}".format(hvalue/1e3), "{:.3f}".format(svalue/1e3)
            Cpvalue = tf.ideal_cpmolar_liquid('mass',fluid,float(Tvalue) + 273.15) if self.manager.screens[2].ids.thermotab2.statepressed <= 2 else polyval(tf.ideal_cpmolar(fluid), float(Tvalue) + 273.15)/(tf.molar_mass(fluid)*1e-3)
            Cvvalue = Cpvalue - 8314/tf.molar_mass(fluid)
            Cpvalue, Cvvalue = "{:.3f}".format(Cpvalue/1e3), "{:.3f}".format(Cvvalue/1e3)
            if self.manager.screens[2].ids.thermotab2.statepressed > 2: cvalue = tf.speed_of_sound(float(Pvalue)*1e5, float(Tvalue) + 273.15, fluid)
            cvalue = "{:.3f}".format(cvalue) if self.manager.screens[2].ids.thermotab2.statepressed > 2 else "N/A in liquid phase"
            Gvalue = "None"
        
        self.statebar.title = "State {}".format(self.manager.screens[2].ids.thermotab2.statepressed)
        self.temp.text = "Temperature : {} [C]".format(Tvalue)
        self.pres.text = "Pressure : {} [bar]".format(Pvalue)
        self.rho.text = "Density : {} [kg/m3]".format(rhovalue)
        self.vspec.text = "Specific Volume : {} [m3/kg]".format(vvalue)
        self.enth.text = "Enthalpy : {} [kJ/kg]".format(hvalue)
        self.entr.text = "Entropy : {} [kJ/kg-K]".format(svalue)
        self.soundspeed.text = "Speed of sound : {} [m/s]".format(cvalue)
        self.comprfactor.text = "Compressibility Factor : {} [-]".format(Zvalue)
        self.fundder.text = "Foundamental Derivative : {} [-]".format(Gvalue)
        self.cp.text = "Specific Heat Capacity Cp : {} [kJ/kg-K]".format(Cpvalue)
        self.cv.text = "Specific Heat Capacity Cv : {} [kJ/kg-K]".format(Cvvalue)


class WorkingFluidInfoScreen(Screen):
    pass

class HeatSourceInfoScreen(Screen):
    pass               
        
class MyMainApp(MDApp):
    dialog = None
    WFLUID = "Select"
    Clock.max_iteration = 20
    counter = 0

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass        

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "ORCestra"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
    
    def build(self, *args):
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.theme_style = 'Light'
        
        
        cf.WFLUID = "Working Fluid : Select"; cf.WorkingFluid = "None"; cf.TET = "None"; cf.PET = "None"; cf.mflow = "None"; cf.PR = "None"; cf.Wout = "None"
        cf.Win = "None"; cf.M2 = None; cf.Gamma = None; cf.MaterialSelected = False; cf.Rtips = "None"; cf.Rhubs = "None"; cf.Rms = "None"; cf.Hs = "None"; cf.ythroat = None; cf.dte = None; cf.pitch = "None"; cf.rho1 = "None"; cf.M1 = "None" ; cf.h1 = "None"; cf.s1 = "None"; cf.h01 = "None" ; cf.a2 = "None"; cf.Zs = None; cf.M2_forslider = "None"; cf.M_contour = []; cf.Gamma_contour = []; cf.Ashape_contour = []; cf.Mrel2 = None; cf.Mrel3 = None; cf.b2 = None; cf.b3 = None; cf.nozzlelinewidth = 2
        
        self.screen_helper = Builder.load_file("main_test.kv")
        return self.screen_helper
        
    def change_screen(self, screen):
        self.screen_helper.current = screen
        self.screen_helper.transition.direction = "right"
    
    def close_dialog(self,obj):
        self.dialog.dismiss()
        
    def on_start(self):
        self.screen_helper.transition = NoTransition()
        self.screen_helper.current = 'main'
        self.screen_helper.transition = SlideTransition()
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')

MyMainApp().run()
