from kivymd.app import MDApp
from kivy.clock import mainthread, Clock
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
import numpy as np
import time
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
import config as cf

Window.size = (350, 650)

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
        
    def WorkingFluid_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet()
        self.WorkingFluidData = ["Acetone", "Benzene", "Butane", "Cyclohexane", "Cyclopentane", "Cyclopropane", "D4", "D5", "D6", "Ethanol", "Heptane", "Isohexane", "Isopentane", "Isobutane", "MD2M", "MD3M", "MD4M", "MDM", "Methanol", "MM", "Nonane", "Octane", "Propane", "Propylene", "R11", "R12", "R13", "R14", "R21", "R22", "R23", "R32", "R41", "R113", "R114", "R115", "R116", "R123", "R124", "R125", "R134a", "R141b", "R142b", "R143a", "R152a", "R161", "R227ea", "R236ea", "R236fa", "R245fa", "R365mfc", "R1234yf", "R1234ze", "R404a", "RC318", "Toluene", "Water"]
        self.WorkingFluidCoolProp = ["ACETONE", "BENZENE", "BUTANE", "CYCLOHEX", "CYCLOPEN", "CYCLOPRO", "D4", "D5", "D6", "ETHANOL", "HEPTANE", "IHEXANE", "IPENTANE", "ISOBUTAN", "MD2M", "MD3M", "MD4M", "MDM", "METHANOL", "MM", "NONANE", "OCTANE", "PROPANE", "PROPYLEN", "R11", "R12", "R13", "R14", "R21", "R22", "R23", "R32", "R41", "R113", "R114", "R115", "R116", "R123", "R124", "R125", "R134A", "R141B", "R142B", "R143A", "R152A", "R161", "R227EA", "R236EA", "R236FA", "R245FA", "R365MFC", "R1234YF", "R1234ZE", "R404A.MIX", "RC318", "TOLUENE", "WATER"]
        
        self.WorkingFluidType = ["Wet", "Dry", "Dry", "Dry", "Dry", "Wet", "Dry", "Dry", "Dry", "Wet", "Dry", "Dry", "Dry", "Dry", "Dry", "Dry", "Dry", "Dry", "Wet", "Dry", "Dry", "Dry", "Wet", "Wet", "Isentropic", "Wet", "Wet", "Wet", "Wet", "Wet", "Wet", "Wet", "Wet", "Dry", "Dry", "Dry", "Isentropic", "Dry", "Dry", "Isentropic", "Wet", "Dry", "Isentropic", "Wet", "Wet", "Wet", "Dry", "Dry", "Dry", "Dry", "Dry", "Isentropic", "Isentropic", "Wet", "Dry", "Dry", "Wet"]
                
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
        if args[0] == "Industrial Gases":
            self.dialog = MDDialog(
                title="[color={}][b] Industrial Gases Composition [/b][/color]".format("#4863A0"),
                type="simple",
                items=[
                    ItemIndDialog(var="nN2",value="0.657"),
                    ItemIndDialog(var="nCO2",value="0.158"),
                    ItemIndDialog(var="nH2O",value="0.103"),
                    ItemIndDialog(var="nO2",value="0.072")],
                buttons=[
                    MDRaisedButton(text="OK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_and_save_ind),
                    MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog),
                ],size_hint=(0.75,1))
            self.dialog.set_normal_height()
            self.dialog.open()
            
    def close_dialog(self,obj):
        self.dialog.dismiss()
        
    def close_and_save_ind(self,obj):
        self.dialog.dismiss()
        
    def HeatSource_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet()
        self.HeatSourceData = ["Industrial Gases","Water/Steam","Hydrogen"]
        self.HeatSourceCoolProp = ["NITROGEN&CO2&WATER&OXYGEN","WATER","HYDROGEN"]
        for i in range(0, len(self.HeatSourceData)):
            bottom_sheet_menu.add_item(
                self.HeatSourceData[i],
                lambda x, y=i: self.callback_for_heatsource_items(self.HeatSourceData[y]))
        bottom_sheet_menu.open()
        
    def Thermstate_dialog(self):
        if self.thermotab3.ThermCalcCompleted == None:
            rhovalue = "None"; vvalue = "None"; hvalue = "None"; svalue = "None"; cvalue = "None"; Zvalue = "None"; Gvalue = "None"; Cpvalue = "None"
            Cvvalue = "None"
        else:
            rhovalue = "{:.2f}".format(self.rhostate[self.statepressed-1]); vvalue = "{:.3f}".format(self.vstate[self.statepressed-1])
            hvalue = "{:.2f}".format(self.hstate[self.statepressed-1]); svalue = "{:.3f}".format(self.sstate[self.statepressed-1])
            cvalue = "{:.2f}".format(self.cstate[self.statepressed-1]); Cpvalue = "{:.3f}".format(self.Cpstate[self.statepressed-1])
            Zvalue = "{:.3f}".format(self.Zstate[self.statepressed-1]) if self.statepressed>=3 else self.Zstate[self.statepressed-1]
            Gvalue = "{:.3f}".format(self.Gstate[self.statepressed-1]) if self.statepressed>=3 else self.Gstate[self.statepressed-1] 
            Cvvalue = "{:.3f}".format(self.Cvstate[self.statepressed-1])
        self.dialog = MDDialog(
            title="[color={}][b] State {} [/b][/color]".format("#4863A0",str(self.statepressed)),
            type="simple",
            items=[
                ItemThermState(var="Density :",value=rhovalue, units=" [kg/m3]"),
                ItemThermState(var="Specific Volume :",value=vvalue, units=" [m3/kg]"),
                ItemThermState(var="Enthalpy :",value=hvalue, units=" [kJ/kg]"),
                ItemThermState(var="Entropy :",value=svalue, units=" [kJ/kg-K]"),
                ItemThermState(var="Speed of sound :",value=cvalue, units=" [m/s]"),
                ItemThermState(var="Compressibility Factor :",value=Zvalue, units=""),
                ItemThermState(var="Foundamental Derivative :",value=Gvalue, units=""),
                ItemThermState(var="Specific Heat Capacity Cp :",value=Cpvalue, units=" [kJ/kg-K]"),
                ItemThermState(var="Specific Heat Capacity Cv :",value=Cvvalue, units=" [kJ/kg-K]")
            ],
            buttons=[MDFlatButton(text="GO BACK", text_color=(0.28, 0.39, 0.63, 1), on_release=self.close_dialog)],
            size_hint=(0.85,1))
        self.dialog.open()
        
class Thermotab3(BoxLayout, MDTabsBase):
    app = App.get_running_app()
    pr = ObjectProperty(None)
    qin = ObjectProperty(None)
    wout = ObjectProperty(None)
    win = ObjectProperty(None)
    wnet = ObjectProperty(None)
    nth = ObjectProperty(None)
    ncar = ObjectProperty(None)
    presscalculate = ObjectProperty(None)
    ThermCalcCompleted = ObjectProperty(None)
    thermotab1 = ObjectProperty(None)
    thermotab2 = ObjectProperty(None)
    thermspinner = ObjectProperty(None)           


class VelTriatab1(BoxLayout, MDTabsBase):
    workingfluidvel = ObjectProperty(None)
    tet = ObjectProperty(None)
    pet = ObjectProperty(None)
    mflowvel = ObjectProperty(None)
    prorm2text = ObjectProperty("Pressure Ratio [-]:")
    prorm2 = ObjectProperty(None)
    mx2 = ObjectProperty(None)
    rn = ObjectProperty(None)
    rotationalspeed = ObjectProperty(None)
    maxrotspeed = ObjectProperty(None)
    material = ObjectProperty(None)
    sf = ObjectProperty(None)
    htr = ObjectProperty(None)
    zs = ObjectProperty(None)
    smin = ObjectProperty(None)
    custom_sheet = ObjectProperty(None)
    rotspeedlabel = ObjectProperty(None)
    rotspeedicon = ObjectProperty(None)
    mx2sldr = ObjectProperty(None)
    rnsldr = ObjectProperty(None)
    rotspeedminus = ObjectProperty(None)
    rotspeedplus = ObjectProperty(None)
    rotspeedsldr = ObjectProperty(None)
    rotspeedrestore = ObjectProperty(None)
    rotspeedround = ObjectProperty(None)
    sfsldr = ObjectProperty(None)
    htrsldr = ObjectProperty(None)
    zssldr = ObjectProperty(None)
    sminsldr = ObjectProperty(None)
    
    def callback_for_pressureratio(self, *args):
        self.prorm2text.text = args[0]
        if args[0] == "Mach Number M2 [-]":
            self.prorm2.text = "2.00"
        else:
            self.prorm2.text = cf.PR
        
    
    def PressureRatio_bottom_sheet(self, **kwargs):
        bottom_sheet_menu = MDListBottomSheet()
        self.PressureorMachData = ["Pressure Ratio [-]:", "Mach Number M2 [-]:"]
        for i in range(0, len(self.PressureorMachData)):
            bottom_sheet_menu.add_item(
                self.PressureorMachData[i],
                lambda x, y=i: self.callback_for_pressureratio(self.PressureorMachData[y]))
        bottom_sheet_menu.open()
        
    def callback_for_material(self, *args):
        self.material.text = "Material : {}".format(args[0])
        self.materialchoice = args[0]
        cf.MaterialSelected = True
        
    def Material_bottom_sheet(self, **kwargs):
        bottom_sheet_menu = MDListBottomSheet()
        self.MaterialData = ["St 37-2", "St 44-2", "St 50-2", "St 52-3", "St 60-2", "St 70-2", "StE 355", "StE 420", "StE 460", "C10E", "17Cr3", "16MnCr5", "20MnCr5", "20MoCrS4", "18CrNiMo7-6", "1C22", "2C22", "1C25", "1C30", "1C35", "1C40", "1C45", "2C45", "1C50", "1C60", "46Cr2", "41Cr4", "34CrMo4", "42CrMo4", "50CrMo4", "36CrNiMo4", "30CrNiMo8", "34CrNiMo6", "31CrMo12", "31CrMoV9", "15CrMoV59", "34CrAlMo5", "34CrAlNi7"]
        for i in range(0, len(self.MaterialData)):
            bottom_sheet_menu.add_item(
                self.MaterialData[i],
                lambda x, y=i: self.callback_for_material(self.MaterialData[y]))
        bottom_sheet_menu.open()
        
    def show_custom_bottom_sheet(self, choice):
        def get_title(i):
            switcher={
                "prorm2":"Pressure Ratio or Mach Number",
                "mx2":"Axial Mach Number",
                "rn":"Degree of Reaction",
                "rotationalspeed":"Rotational Speed",
                "sf":"Material and Safety Factor",
                "htr":"Hub to Tip ratio",
                "zs":"Number of blades",
                "smin":"Minimun blade thickness"}
            return str(switcher.get(i))
        
        def get_text(i):
            switcher={
                "prorm2":"Select pressure ratio or stator's exit Mach number as input and set value",
                "mx2":"Set the axial Mach number, which is constant through the stator and rotor",
                "rn":"Set the turbine's degree of reaction in prercentage. Degrees of reaction of 0% (impulse turbine) are prefered in these applications",
                "rotationalspeed":"Define the rotational speed in the rotor blade in rpm or select the maximum possible rotational speed, based of the centrifugal stresses limits",
                "sf":"Define the material of the rotor blade and set the safety factor of the construction. The safety factor sets the maximun rotational speed of the rotor blade according to the centrifugal stresses",
                "htr":"Define the stator blade's hub to tip ratio",
                "zs":"Define the number of blades of the stator",
                "smin":"Set the minimum possible value for the blade thickness in mm. The minimum blade thickness is also equal the the diameter in the trailing edge"}
            return str(switcher.get(i))
        
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet(title = get_title(choice), text = get_text(choice)))
        self.custom_sheet.open()
        
    def MaxRotActivate(self):
        if self.maxrotspeed.active == True:
            self.rotationalspeed.disabled = True
            self.rotspeedminus.disabled = True
            self.rotspeedplus.disabled = True
            self.rotspeedsldr.disabled = True
            self.rotspeedround.disabled = True
            self.rotspeedrestore.disabled = True
            self.rotspeedlabel.text_color = [128/255,128/255,128/255, 1]
            self.rotspeedicon.text_color = [128/255,128/255,128/255, 1]
        else:
            self.rotationalspeed.disabled = False
            self.rotspeedminus.disabled = False
            self.rotspeedplus.disabled = False
            self.rotspeedsldr.disabled = False
            self.rotspeedround.disabled = False
            self.rotspeedrestore.disabled = False
            self.rotspeedlabel.text_color = [0.19, 0.64, 0.20, 1]
            self.rotspeedicon.text_color = [0.19, 0.64, 0.20, 1]


class VelTriatab2(BoxLayout, MDTabsBase):
    dh0 = ObjectProperty(None)
    ublade = ObjectProperty(None)
    mblade = ObjectProperty(None)
    nrotational = ObjectProperty(None)
    prvel = ObjectProperty(None)
    psi = ObjectProperty(None)
    phi = ObjectProperty(None)
    woutact = ObjectProperty(None)
    wnetact = ObjectProperty(None)
    nexerg = ObjectProperty(None)
    veltriaspinner = ObjectProperty(None)

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def VelStator_dialog(self):
        if self.ublade.text == "Blade Velocity U : None [m/s]":
            M1 = "None"; V1 = "None"; M2 = "None"; V2 = "None"; a1 = "None"; a2 = "None"
        else:
            M1 = "{:.3f}".format(self.M1); V1 = "{:.3f}".format(self.V1); M2 = "{:.3f}".format(self.M2); V2 = "{:.3f}".format(self.V2); 
            a1 = "{:.3f}".format(0); a2 = "{:.3f}".format(self.a2)
        self.dialog = MDDialog(
            title="[color={}][b] {} [/b][/color]".format("#30A234","Stator Results"),
            type="simple",
            items=[
                ItemVelState(var="Mach Inlet M1 :",value=M1, units=""),
                ItemVelState(var="Velocity Inlet V1 :",value=V1, units=" [m/s]"),
                ItemVelState(var="Mach Outlet M2 :",value=M2, units=""),
                ItemVelState(var="Velocity Outlet V2 :",value=V2, units=" [m/s]"),
                ItemVelState(var="Inlet Flow angle U+03b1 1 :",value=a1, units=" [deg]"),
                ItemVelState(var="Outlet Flow angle U+03b1 2 :",value=a2, units=" [deg] "),
            ],
            buttons=[MDFlatButton(text="GO BACK", text_color=(0.19, 0.64, 0.20, 1), on_release=self.close_dialog)],
            size_hint=(0.85,1))
        self.dialog.open()
        
    def VelRotor_dialog(self):
        if self.ublade.text == "Blade Velocity U : None [m/s]":
            Mrel2 = "None"; W2 = "None"; Mrel3 = "None"; W3 = "None"; M3 = "None"; V3 = "None"; b2 = "None"; b3 = "None"; a3 = "None"
        else:
            Mrel2 = "{:.3f}".format(self.Mrel2); W2 = "{:.3f}".format(self.W2); Mrel3 = "{:.3f}".format(self.Mrel3); W3 = "{:.3f}".format(self.W3)
            M3 = "{:.3f}".format(self.M3); V3 = "{:.3f}".format(self.V3); b2 = "{:.3f}".format(self.b2); b3 = "{:.3f}".format(self.b3)
            a3 = "{:.3f}".format(self.a3)
        self.dialog = MDDialog(
            title="[color={}][b] {} [/b][/color]".format("#30A234","Rotor Results"),
            type="simple",
            items=[
                ItemVelState(var="Relative Mach Inlet Mrel,2 :",value=Mrel2, units=""),
                ItemVelState(var="Relative Velocity Inlet W2 :",value=W2, units=" [m/s]"),
                ItemVelState(var="Relative Mach Outlet Mrel,3 :",value=Mrel3, units=""),
                ItemVelState(var="Relative Velocity Outlet W3 :",value=W3, units=" [m/s]"),
                ItemVelState(var="Absolute Mach Outlet M3 :",value=M3, units=""),
                ItemVelState(var="Absolute Velocity Outlet V3 :",value=V3, units=" [m/s]"),
                ItemVelState(var="Relative Flow Inlet angle β2 :",value=b2, units=" [deg]"),
                ItemVelState(var="Relative Flow Outlet angle β3 :",value=b3, units=" [deg] "),
                ItemVelState(var="Absolute Flow Outlet angle α3 :",value=a3, units=" [deg] "),
            ],
            buttons=[MDFlatButton(text="GO BACK", text_color=(0.19, 0.64, 0.20, 1), on_release=self.close_dialog)],
            size_hint=(0.85,1))
        self.dialog.open()
        
                
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
        switcher={0:45223*Window.width**(-0.822),1:43821*Window.width**(-0.803),2:43821*Window.width**(-0.803),3:43821*Window.width**(-0.803)}
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
            Tvalue = "{:.2f}".format(self.manager.screens[2].ids.thermotab2.Tstate[ self.manager.screens[2].ids.thermotab2.statepressed-1] - 273.15)
            Pvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.vstate[ self.manager.screens[2].ids.thermotab2.statepressed-1]/1e5)
            rhovalue = "{:.2f}".format(self.manager.screens[2].ids.thermotab2.rhostate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            vvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.vstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            hvalue = "{:.2f}".format(self.manager.screens[2].ids.thermotab2.hstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            svalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.sstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            cvalue = "{:.2f}".format(self.manager.screens[2].ids.thermotab2.cstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            Cpvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.Cpstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
            Zvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.Zstate[ self.manager.screens[2].ids.thermotab2.statepressed-1]) if self.manager.screens[2].ids.thermotab2.statepressed>=3 else self.manager.screens[2].ids.thermotab2.Zstate[self.manager.screens[2].ids.thermotab2.statepressed-1]
            Gvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.Gstate[ self.manager.screens[2].ids.thermotab2.statepressed-1]) if self.manager.screens[2].ids.thermotab2.statepressed>=3 else self.manager.screens[2].ids.thermotab2.Gstate[ self.manager.screens[2].ids.thermotab2.statepressed-1] 
            Cvvalue = "{:.3f}".format(self.manager.screens[2].ids.thermotab2.Cvstate[ self.manager.screens[2].ids.thermotab2.statepressed-1])
        
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

class VelTriaScreen(Screen):    
    pass        
class StatorScreen(Screen):
    check = ObjectProperty(None)
    rhubs = ObjectProperty(None)
    rtips = ObjectProperty(None)
    hs = ObjectProperty(None)
    ythroat = ObjectProperty(None)
    pitch = ObjectProperty(None)
    dte = ObjectProperty(None)
    gridexs = NumericProperty(-1)
    charlinesexs = NumericProperty(-1)
    gridtext = ObjectProperty(None)
    linestext = ObjectProperty(None)
    mab = ObjectProperty(None)
    gammasldr = ObjectProperty(None)
    m2sldr = ObjectProperty(None)
    r2r1sldr = ObjectProperty(None)
    mabsldr = ObjectProperty(None)
    statorspinner = ObjectProperty(None)
    schord = ObjectProperty(None)
    ssolidity = ObjectProperty(None)
    schratio = ObjectProperty(None)
    
    def on_pre_enter(self):
        self.rtips.text = "{:.3f}".format(cf.Rtips*1e3) if cf.M2 != None else cf.Rtips
        self.rhubs.text = "{:.3f}".format(cf.Rhubs*1e3) if cf.M2 != None else cf.Rhubs
        self.hs.text  = "{:.3f}".format(cf.Hs*1e3) if cf.M2 != None else cf.Hs
        self.ythroat.text = "{:.3f}".format(cf.ythroat) if cf.ythroat != None else "1"
        self.dte.text = "{:.3f}".format(cf.dte*1e3) if cf.M2 != None else "None"
        self.pitch.text = "{:.3f}".format(cf.pitch*1e3) if cf.M2 != None else cf.pitch
        
    def show_statorblade_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.StatorBladeCustomSheet())
        self.custom_sheet.open()
        
    def show_statorsectionab_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.StatorSectionAbCustomSheet())
        self.custom_sheet.open()
        
    def show_statorR2R1_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.StatorR2R1CustomSheet())
        self.custom_sheet.open()
                
            
    def close_dialog(self,obj):
        self.dialog.dismiss()        
                   
class RotorScreen(Screen):
    labelmrel2 = ObjectProperty(None)
    labelmrel3 = ObjectProperty(None)
    labelb2 = ObjectProperty(None)
    labelb3 = ObjectProperty(None)
    labelgamma = ObjectProperty(None)
    mrel2sldr = ObjectProperty(None)
    mrel3sldr = ObjectProperty(None)
    b2sldr = ObjectProperty(None)
    b3sldr = ObjectProperty(None)
    gammasldr = ObjectProperty(None)
    rhubr = ObjectProperty(None)
    rtipr = ObjectProperty(None)
    hr = ObjectProperty(None)
    dte = ObjectProperty(None)
    msssldr = ObjectProperty(None)
    mss = ObjectProperty(None)
    mpssldr = ObjectProperty(None)
    mps = ObjectProperty(None)
    rchord = ObjectProperty(None)
    rpitch = ObjectProperty(None)
    rsolidity = ObjectProperty(None)
    rchratio = ObjectProperty(None)
    rsonic = ObjectProperty(None)
    mrel2ini = NumericProperty(1.40)
    mrel3ini = NumericProperty(1.50)
    b2ini = NumericProperty(60.0)
    b3ini = NumericProperty(60.0)
    gammaini = NumericProperty(1.40)
    mssini = NumericProperty(1.80)
    mpsini = NumericProperty(1.20)
    gridexs = NumericProperty(-1)
    envelopexs = NumericProperty(-1)
    arcexs = NumericProperty(-1)
    gridtext = ObjectProperty(None)
    envelopetext = ObjectProperty(None)
    arcstext = ObjectProperty(None)
    
    def on_pre_enter(self, *args):
        self.errorcalc = False
        
        self.Mrel2 = cf.Mrel2 if cf.Mrel2 != None else 1.4
        self.Mrel3 = cf.Mrel3 if cf.Mrel3 != None else 1.5
        self.b2 = float(cf.b2) if cf.b2 != None else float(60)
        self.b3 = float(cf.b3) if cf.b3 != None else float(60)
        self.Gamma = float(cf.Gamma) if cf.Gamma != None else 1.4
        self.mrel2ini = float(self.Mrel2); self.mrel3ini = float(self.Mrel3); self.b2ini = self.b2; self.b3ini = self.b3; self.gammaini = self.Gamma;
        self.mssini = self.mrel2ini + 0.4
        self.mpsini = self.mrel2ini - 0.2 if self.mrel2ini - 0.2 > 1 else 1.01
                
    def show_rotor_custom_bottom_sheet(self, choice):
        def get_title(i):
            switcher={
                "mrel2":"Inlet Relative Mach number",
                "mrel3":"Outlet Relative Mach number",
                "b2":"Inlet Relative Flow angle",
                "b3":"Inlet Relative Flow angle",
                "gamma":" Polytropic Index k",
                "mss":"Mach number in sunction side",
                "mps":"Mach number in pressure side"}
            return str(switcher.get(i))
        
        def get_text(i):
            switcher={
                "mrel2":"Select the Mach number in the rotor's inlet. This Mach number is a relative Mach number as it is derived from the relative velocity W2.  Mrel2 = W2/c2",
                "mrel3":"Select the Mach number in the rotor's inlet. This Mach number is a relative Mach number as it is derived from the relative velocity W3.  Mrel3 = W3/c3",
                "b2":"Select the flow angle in the rotor's inlet. This flow angle is the relative flow angle, as it is derived from the relative velocity W2.",
                "b3":"Select the flow angle in the rotor's outlet. This flow angle is the relative flow angle, as it is derived from the relative velocity W3.",
                "gamma": "Set the polytropic index of the proposed process, or calculate it through the thermodynamic cycle and the velocity triangles analysis. The polytropic index defines finally the shape of the blade",
                "mss":"Specify the Mach number in the sunction side, which is the maximum Mach number in the blade passage. Note that the Mach number in sunction side must be greater than the Mach number in inlet and the outlet",
                "mps":"Specify the Mach number in the pressure side, which is the minimum Mach number in the blade passage. Note that the Mach number in pressure side must be lower than the Mach number in inlet and the outlet"}
            return str(switcher.get(i))
        
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.RotorCustomSheet(title = get_title(choice), text = get_text(choice)))
        self.custom_sheet.open()
                
    def close_dialog(self,obj):
        self.dialog.dismiss()
        
    def sunc_pres_limits(self,choice,**kwargs):
        if choice == "mps":
            if self.mpssldr.value > min(self.mrel2sldr.value,self.mrel3sldr.value) - 1e-3:
                self.mpssldr.value = min(self.mrel2sldr.value,self.mrel3sldr.value) - 1e-3
                self.mps.text = "{:.2f}".format(self.mpssldr.value)
        elif choice == "mss":
            if self.msssldr.value < max(self.mrel2sldr.value,self.mrel3sldr.value):
                self.msssldr.value = max(self.mrel2sldr.value,self.mrel3sldr.value)
                self.mss.text = "{:.2f}".format(self.msssldr.value)
                
        
class MyMainApp(MDApp):
    dialog = None
    WFLUID = "Select"
    Clock.max_iteration = 20

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass        
    
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


MyMainApp().run()
