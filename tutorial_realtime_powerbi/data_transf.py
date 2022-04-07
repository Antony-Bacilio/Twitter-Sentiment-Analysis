# libraries for data creation and preprocessing
import pvlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pvlib.temperature import sapm_cell, TEMPERATURE_MODEL_PARAMETERS
import requests
import datetime
from pvlib import pvsystem
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

"""
Dummy Data Creation For Jodhpur Location
Since location of solar plant site plays very critical role, so it will be good to know some of key information about solar irradition for a desired location, i.e Jodhpur.
 Maximum Solar Radimation Intensity of about 6-7kWh/ Sq.m/day and more than 325 sunny days in a year with a very low average rainfall.
The mean duration of bright sunshine in this region is 8.0 to 8.8 hr/day.
     The maximum sunshine period of 9.6 to 9.8 hr/day is in October for western part of Rajasthan whereas it is 10.0 to 10.5 hr/day  during April and May for eastern part.
In rainy month of August the sunshine is available only for about 4.4 to 7.1 hrs/day.
        Even during rainy season of July and August, the skies remain clear for 8-9 days/month in west Rajasthan and for 4-5 days/month in east Rajasthan.
    The cloud cover decreases to a great extent over the entire state during October.
Feature Details
    HV_Temp:High voltage temperature - temperature of transformer side which is connected to load.
    LV_W1_Temp:low voltage temperature - temperature of windings (one)  of transformer side which is connected to supply
    LV_W2_Temp:low voltage temperature - temperature of windings (second) 
    OTI_Temp:Oil temperature indicators is used to signifies amount of loss 
    INV1_TOT_ACT_PWR:total inverter ac transmission power
    INV2_TOT_ACT_PWR:total inverter2 ac transmission power 
Expression Based Approach
Here we will try to create dummy dataset using some relationship among the features that we have selected for our transformer analysis.
it is found the there are many factors that can affect the power of pv module/cell like cell temperature, dirt/soil, shadowing etc. and the extent of these factors can be collected from the manufacturers and along with we will also be requiring the STC (standard test condition) parameters.
For now we are these factors for data creation and can be later manipulated and all the losses the cable losses, mppt losses etc are also assumed. 
If we can have the ambient temperature data for our plant location then the dummy data can resembles with our real data.
"""


class TransformerDataGenerator:

    def get_ambient_temp(self):
        try:
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Jodhpur,Rajasthan,"
                                    "India&APPID=fd21b466b83ff9db3eef78c0d35c0eb3")
            temp = response.json()['main']['temp']
            if temp <= 0:
                temp = 25.23
            else:
                temp = temp - 273.15
        except Exception as e:
            print("Please check the exception:", e)
        else:
            return temp

    """
    It is found that there is positive correlation between ambient temperature and solar irradiance.So predict the solar irradiance for a particular location of PV system, we can fit line.
    Here in this case, I have assumed the parameters for best fit line with the reference from some paper.
    Here m is slope of best fit line  and c is the intercept of best fit line
    """

    def solar_irradiance(self, amb_temp, m=25, c=300):
        """
        amb_temp=ambient temperature Data
        m=slope of best fit line
        c=intercept of best fit line
        """

        if m > 0:
            solar_irr = m * amb_temp + c
        else:
            raise Exception("please check the value of m, it should be positive", m)

        return solar_irr

    """
    ....
    Cell temperature has negative correlation with module power output. 
    Here I'm using pvlib library for determining cell temperature and the parameters are taken for sapm model for insulated_back_glass_polymer and considering wind speed to its minimum.

    model parameters:{'a': -2.81, 'b': -0.0455, 'deltaT': 0}
    rack: racking type used while install the module
    model: model used to calculate cell temperature 
    wind_speed: wind speed at location

    ....
    """

    def cell_temperature(self, solar_irr, amb_temp, cell_temp_model="sapm", rack='insulated_back_glass_polymer',
                         wind_speed=1, noise_c_temp_per=(0.9, 0.03)):
        try:

            params = TEMPERATURE_MODEL_PARAMETERS[cell_temp_model][rack]
            cell_temp = sapm_cell(solar_irr, amb_temp, wind_speed, **params)
            cell_temp = cell_temp * np.random.normal(noise_c_temp_per[0], noise_c_temp_per[1], 1)

        except Exception as e:
            print('please read the exception:', e)
        else:

            return cell_temp

    """
    ....
    Module power output have many dependencies like solar irradiance, cell temperature, temperature coefficient  and standard testing conditions(STC)
    Here In this case, I have considered STC parameters to evaluate the module power output.
    pdc0: power at standard testing condition
    gamma_pdc:temperature coefficient 
    temp_ref: reference temperature of the location
    ....
    """

    def module_power_output(self, solar_irradiance, cell_temp, pdc0=240, gamma_pdc=-0.005, temp_ref=25.0):
        try:
            module_power_output = pvlib.pvsystem.pvwatts_dc(g_poa_effective=solar_irradiance, temp_cell=cell_temp,
                                                            pdc0=pdc0, gamma_pdc=gamma_pdc, temp_ref=temp_ref)

        except Exception as e:
            print("Please check the exception:", e)
        else:

            return module_power_output

    """
    ....
    Measuring current and voltage for module by considering the required parameters (Canadian solar plant).
    alpha_sc : float
        The short-circuit current temperature coefficient of the
        module in units of A/C.
    beta_oc:float
       The open-circuit current temperature coefficient of the
        module in units of A/C
    gamma_ref : float
        The diode ideality factor
    mu_gamma : float
        The temperature coefficient for the diode ideality factor, 1/K
    I_L_ref : float
        The light-generated current (or photocurrent) at reference conditions,
        in amperes.
    I_o_ref : float
        The dark or diode reverse saturation current at reference conditions,
        in amperes.
    R_sh_ref : float
        The shunt resistance at reference conditions, in ohms.
    R_sh_0 : float
        The shunt resistance at zero irradiance conditions, in ohms.
    R_s : float
        The series resistance at reference conditions, in ohms.
    cells_in_series : integer
        The number of cells connected in series.
    R_sh_exp : float
        The exponent in the equation for shunt resistance, unitless. Defaults
        to 5.5.
    EgRef : float
        The energy bandgap at reference temperature in units of eV.
        1.121 eV for crystalline silicon. EgRef must be >0.
    BIPV:
    Building-integrated photovoltaics (BIPV) are photovoltaic materials that are used to replace
    conventional building materials in parts of the building envelope such as the roof, skylights, or facades.

    T_NOCT:Nominal Operating Cell Temperature

    dEgdT:float
    The temperature dependence of the energy bandgap at reference conditions in units of 1/K. May be either a scalar value (e.g. -0.0002677 as in [1]) or a DataFrame (this may be useful if dEgdT is a modeled as a function of temperature). 
    For parameters from the SAM CEC module database, dEgdT=-0.0002677 is implicit for all cell types in the parameter estimation algorithm used by NREL.
    A_c': Cell Area
    N_s: Number of cell in series
    ....
    """
    parameters = {
        'Name': 'Canadian Solar CS5P-220M',
        'BIPV': 'N',
        'Date': '10/5/2009',
        'T_NOCT': 42.4,
        'A_c': 1.7,
        'N_s': 96,
        'I_sc_ref': 5.1,
        'V_oc_ref': 59.4,
        'I_mp_ref': 4.69,
        'V_mp_ref': 46.9,
        'alpha_sc': 0.004539,
        'beta_oc': -0.22216,
        'a_ref': 2.6373,
        'I_L_ref': 5.114,
        'I_o_ref': 8.196e-10,
        'R_s': 1.065,
        'R_sh_ref': 381.68,
        'gamma_r': -0.476,
        'Technology': 'Mono-c-Si',
    }

    def dc_current_voltage(self, solar_irradiance, cell_temp, parameters, EgRef=1.121, dEgdT=-0.0002677,
                           ivcurve_pnts=100, method='lambertw', noise_dc_c_v_per=(0.9, 0.03)):

        try:
            IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
                solar_irradiance,
                cell_temp,
                alpha_sc=parameters['alpha_sc'],
                a_ref=parameters['a_ref'],
                I_L_ref=parameters['I_L_ref'],
                I_o_ref=parameters['I_o_ref'],
                R_sh_ref=parameters['R_sh_ref'],
                R_s=parameters['R_s'],
                EgRef=EgRef,
                dEgdT=dEgdT
            )
            curve_info = pvsystem.singlediode(
                photocurrent=IL,
                saturation_current=I0,
                resistance_series=Rs,
                resistance_shunt=Rsh,
                nNsVth=nNsVth,
                ivcurve_pnts=ivcurve_pnts,
                method=method
            )
            module_dc_voltage = curve_info['v'][:, 50] * np.random.normal(noise_dc_c_v_per[0], noise_dc_c_v_per[1], 1)
            module_dc_current = curve_info['i'][:, 50] * np.random.normal(noise_dc_c_v_per[0], noise_dc_c_v_per[1], 1)
        except Exception as e:
            print('Please read the exception:', e)
        else:
            return module_dc_current, module_dc_voltage

    """
    ....
    Here we are using two different inverters with different configuration and evaluating the AC power for them.
    and sandia model is used to calculate the ac power.
    name: name of inverter
    model: model of inverter
    ....
    """

    def inv_config_retrieve(self, name1='ABB__MICRO_0_25_I_OUTD_US_208__208V_', model1='CECInverter',
                            name2='ABB__MICRO_0_25_I_OUTD_US_240__240V_', model2='CECInverter'):
        try:

            invdb = pvsystem.retrieve_sam(model1)
            inverter1 = invdb[name1]
            invdb = pvsystem.retrieve_sam(model2)
            inverter2 = invdb[name2]
        except Exception as e:
            print('Please the check exception:', e)
        else:
            return inverter1, inverter2

    def ac_power_current(self, v_dc, p_dc, inverter1, inverter2, noise_ac_p_c=(5.5, 1.5)):
        r'''
        Calculate the inverter AC power without clipping
        Pac0:AC-power output from inverter based on input power and voltage (W)
        Pdc0:DC-power input to inverter, typically assumed to be equal to the PV array maximum power (W)
        Vdc0:DC-voltage level at which the AC-power rating is achieved at the reference operating condition (V)
        Ps0:DC-power required to start the inversion process, or self-consumption by inverter, strongly influences inverter efficiency at low power levels (W)
        C0:Parameter defining the curvature (parabolic) of the relationship between ac-power and dc-power at the reference operating condition, default value of zero gives a linear relationship (1/W)
        C1:Empirical coefficient allowing Pdco to vary linearly with dc-voltage input, default value is zero (1/V)
        C2:Empirical coefficient allowing Pso to vary linearly with dc-voltage input, default value is zero (1/V)
        C3:Empirical coefficient allowing Co to vary linearly with dc-voltage input, default value is zero (1/V)
        '''
        try:
            Paco1 = inverter1['Paco']
            Pdco1 = inverter1['Pdco']
            Vdco1 = inverter1['Vdco']
            C01 = inverter1['C0']
            C11 = inverter1['C1']
            C21 = inverter1['C2']
            C31 = inverter1['C3']
            Pso1 = inverter1['Pso']

            A1 = Pdco1 * (1 + C11 * (v_dc - Vdco1))
            B1 = Pso1 * (1 + C21 * (v_dc - Vdco1))
            C1 = C01 * (1 + C31 * (v_dc - Vdco1))

            ac_power1 = (Paco1 / (A1 - B1) - C1 * (A1 - B1)) * (p_dc - B1) + C1 * (p_dc - B1) ** 2 + np.random.normal(
                noise_ac_p_c[0], noise_ac_p_c[1], 1)
            ac_current_lv_w1 = ac_power1 / float(inverter1['Vac']) + np.random.normal(noise_ac_p_c[0], noise_ac_p_c[1],
                                                                                      1)

            Paco2 = inverter2['Paco']
            Pdco2 = inverter2['Pdco']
            Vdco2 = inverter2['Vdco']
            C02 = inverter2['C0']
            C12 = inverter2['C1']
            C22 = inverter2['C2']
            C32 = inverter2['C3']
            Pso2 = inverter2['Pso']

            A2 = Pdco2 * (1 + C12 * (v_dc - Vdco2))
            B2 = Pso2 * (1 + C22 * (v_dc - Vdco2))
            C2 = C02 * (1 + C32 * (v_dc - Vdco2))

            ac_power2 = (Paco2 / (A2 - B2) - C2 * (A2 - B2)) * (p_dc - B2) + C2 * (p_dc - B2) ** 2 + np.random.normal(
                noise_ac_p_c[0], noise_ac_p_c[1], 1)
            ac_current_lv_w2 = ac_power2 / float(inverter2['Vac']) + np.random.normal(noise_ac_p_c[0], noise_ac_p_c[1],
                                                                                      1)


        except Exception as e:
            print('please check the exception:', e)
        else:
            return ac_power1, ac_power2, ac_current_lv_w1, ac_current_lv_w2

    """
    Current for high voltage side is calculated using turning ratio.
    considering turning ratio to be 10:1 and primary windings 80 and secondary windings 800 and mean turn length(mlt) =3.69 cm
    considering truning ratio ti  be 8:1 and primary windings as 100 and secondary windings as 800  
    Rcu=1.678uohm/cm
    """

    def current_hv(self, ac_current_lv_w1, ac_current_lv_w2, turns_ratio=(10, 1), noise_c_hv_per=(0.85, 0.05)):
        try:
            current_hv = (ac_current_lv_w1 + ac_current_lv_w2) * turns_ratio[1] / turns_ratio[0] * np.random.normal(
                noise_c_hv_per[0], noise_c_hv_per[1], 1)

        except Exception as e:
            print('please check the exception', e)

        else:
            return current_hv

    """
    ....
    Mean Turning Length=mlt
    Resistance of Copper per unit Length=rcu
    Number of Turns for primary windings 1=np1
    Number of Turns for primary windings 2=np2
    Number of Turns for secondary windings=ns
    Resistance of primary windings 1=Rp1
    Resistance of primary windings 2=Rp2
    Resistance of secondary windings= Rs
    ....
    """

    def resistance_lvw1_lvw2_hv(self, mlt=3.69, rcu=1.678, n_turns_lv1_lv2_hv=(80, 100, 800)):
        Rp1 = mlt * rcu * n_turns_lv1_lv2_hv[0]

        Rp2 = mlt * rcu * n_turns_lv1_lv2_hv[1]

        Rs = mlt * rcu * n_turns_lv1_lv2_hv[2]

        return Rp1, Rp2, Rs

    """
    ....
    Power loss at low valtage windings/primary and high voltage windings/secondary I2R
    Power of primary windings 1=Pp
    Power of primary windings 2=Pp1
    Power of secondary windings=Ps
    Sum all the powers=total_power
    ....
    """

    def power_lv1_lv2_hv(self, ac_current_lv_w1, ac_current_lv_w2, ac_current_hv, Rp1, Rp2, Rs,
                         noise_p_lv1_lv2_hv=(5.5, 1.5)):
        Pp1 = ac_current_lv_w1 ** 2 * Rp1 + np.random.normal(noise_p_lv1_lv2_hv[0], noise_p_lv1_lv2_hv[1], 1)
        Pp2 = ac_current_lv_w2 ** 2 * Rp2 + np.random.normal(noise_p_lv1_lv2_hv[0], noise_p_lv1_lv2_hv[1], 1)
        Ps = ac_current_hv ** 2 * Rs + np.random.normal(noise_p_lv1_lv2_hv[0], noise_p_lv1_lv2_hv[1], 1)
        total_power = Pp1 + Pp2 + Ps
        return total_power, Pp1, Pp2, Ps

    """
    ....
    Calculating temperature in low voltage side windings by considering the area of transformer plate.
    temperature rise in deltaT=power/A
    consider A=105*70 cm2
    ...
    """

    def temp_lv1_lv2_hv(self, amb_temp, Pp1, Pp2, Ps, area=7350, noise_t_lv1_lv2_hv=(6.5, 2)):
        temp_lv_w1 = (Pp1 / 7350) ** 0.833 + amb_temp + np.random.normal(noise_t_lv1_lv2_hv[0], noise_t_lv1_lv2_hv[1],
                                                                         1)
        temp_lv_w2 = (Pp2 / 7350) ** 0.833 + amb_temp + np.random.normal(noise_t_lv1_lv2_hv[0], noise_t_lv1_lv2_hv[1],
                                                                         1)
        temp_hv = (Ps / 7350) ** 0.833 + amb_temp + np.random.normal(noise_t_lv1_lv2_hv[0], noise_t_lv1_lv2_hv[1], 1)

        return temp_lv_w1, temp_lv_w2, temp_hv

    # pt=total_power
    def oti_temp(self, pt, temp_lv_w1, temp_lv_w2, temp_hv, amb_temp, noise_oti_t=(6.5, 1.8)):

        nu_product = (temp_lv_w1)
        nu_product1 = (pt * temp_lv_w2)
        de_product = pt * temp_hv
        n = np.log((nu_product + nu_product1) / de_product)
        d = np.log((temp_lv_w1 + temp_lv_w2) / temp_hv)
        OTI_temp = n / d + amb_temp + np.random.normal(noise_oti_t[0], noise_oti_t[1], 1)
        return OTI_temp

    def loaded_model(self, fileloc):
        loaded_model = load_model(fileloc)
        return loaded_model

    def transform_tensor(self, data):
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(data)
        X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
        return scaler, X_train

    def data_generator(self):
        amb_temp = self.get_ambient_temp()
        solar_irr = self.solar_irradiance(amb_temp)
        cell_temp = self.cell_temperature(solar_irr, amb_temp)
        module_power = self.module_power_output(solar_irr, cell_temp)
        dc_current_voltage = self.dc_current_voltage(solar_irr, cell_temp)
        inv1, inv2 = self.inv_config_retrieve()
        ac_power1, ac_power2, ac_lv_w1, ac_lv_w2 = self.ac_power_current(dc_current_voltage[1], module_power, inv1,
                                                                         inv2)
        ac_current_hv = self.current_hv(ac_lv_w1, ac_lv_w2)
        Rp1, Rp2, Rs = self.resistance_lvw1_lvw2_hv()
        Pt, Pp1, Pp2, Ps = self.power_lv1_lv2_hv(ac_lv_w1, ac_lv_w2, ac_current_hv, Rp1, Rp2, Rs)
        t_lv1, t_lv2, t_hv = self.temp_lv1_lv2_hv(amb_temp, Pp1, Pp2, Ps)
        oti_t = self.oti_temp(Pt, t_lv1, t_lv2, t_hv, amb_temp)
        model = self.loaded_model(r"my_model.h5")

        tf1 = pd.DataFrame({'TEMPERATURE LV W1': t_lv1,
                            'TEMPERATURE LV W2': t_lv2,
                            'TEMPERATURE HV': t_hv,
                            'OTI TEMPERATURE': oti_t,
                            })
        tf1_arr = np.array(tf1)
        tf1_arr_transform = self.transform_tensor(tf1_arr)[1]
        tf1_arr_pred = model.predict(tf1_arr_transform) + np.random.normal(1.5, 1.5, len(tf1_arr))
        tf1_arr_pred_reshaped = tf1_arr_pred.reshape(tf1_arr_pred.shape[0], tf1_arr_pred.shape[2])
        scaler = self.transform_tensor(tf1_arr)[0]
        tf1_arr_pred_inv = scaler.inverse_transform(tf1_arr_pred_reshaped)
        columns_pred = ['TEMPERATURE LV W1 PREDICTED', 'TEMPERATURE LV W2 PREDICTED', 'TEMPERATURE HV PREDICTED',
                        'OTI TEMPERATURE PREDICTED']
        tf1_pred_df = pd.DataFrame(tf1_arr_pred_inv, columns=columns_pred)
        tf1_c = pd.concat([tf1, tf1_pred_df], axis=1)
        tf1_c['AMBIENT TEMPERATURE'] = amb_temp,
        tf1_c['SOLAR IRRADIANCE'] = solar_irr,
        tf1_c['TOTAL POWER'] = Pt
        tf1_c['CELL TEMPERATURE'] = cell_temp
        tf1_c['TIMESTAMPS'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tf1_c['TRANFORMER'] = "TF1"

        """

        tf2=pd.DataFrame({
                 'temp_lv_w1':t_lv1+np.random.normal(2.5,0.5,1),
                'temp_lv_w2':t_lv2+np.random.normal(2.5,0.5,1),
                'temp_hv':t_hv+np.random.normal(2.5,0.5,1),
                'OTI_temp':oti_t+np.random.normal(2.5,0.5,1),
                })
        tf2_arr=np.array(tf2)
        tf2_arr_transform=self.transform_tensor(tf2_arr)[1]
        tf2_arr_pred=model.predict(tf2_arr_transform)
        tf2_arr_pred_reshaped=tf2_arr_pred.reshape(tf2_arr_pred.shape[0],tf2_arr_pred.shape[2])
        scaler=self.transform_tensor(tf2_arr)[0]
        tf2_arr_pred_inv=scaler.inverse_transform(tf2_arr_pred_reshaped)
        columns_pred=['temp_lv_w1_pred', 'temp_lv_w2_pred', 'temp_hv_pred', 'OTI_temp_pred']
        tf2_pred_df=pd.DataFrame(tf2_arr_pred_inv,columns=columns_pred)
        tf2_c=pd.concat([tf2,tf2_pred_df],axis=1)
        tf2_c['Timestamps']=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        tf2_c['Transformer']="tf2"

        tf3=pd.DataFrame({
                 'temp_lv_w1':t_lv1+np.random.normal(2.5,0.8,1),
                'temp_lv_w2':t_lv2+np.random.normal(2.5,0.8,1),
                'temp_hv':t_hv+np.random.normal(2.5,0.8,1),
                'OTI_temp':oti_t+np.random.normal(2.5,0.8,1)})
        tf3_arr=np.array(tf3)
        tf3_arr_transform=self.transform_tensor(tf3_arr)[1]
        tf3_arr_pred=model.predict(tf3_arr_transform)
        tf3_arr_pred_reshaped=tf3_arr_pred.reshape(tf3_arr_pred.shape[0],tf3_arr_pred.shape[2])
        scaler=self.transform_tensor(tf3_arr)[0]
        tf3_arr_pred_inv=scaler.inverse_transform(tf3_arr_pred_reshaped)
        columns_pred=['temp_lv_w1_pred', 'temp_lv_w2_pred', 'temp_hv_pred', 'OTI_temp_pred']
        tf3_pred_df=pd.DataFrame(tf3_arr_pred_inv,columns=columns_pred)
        tf3_c=pd.concat([tf3,tf3_pred_df],axis=1)
        tf3_c['Timestamps']=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        tf3_c['Transformer']="tf3"

        trans_data=pd.concat([tf1_c,tf2_c,tf3_c],axis=0)


        tf1_dict={'Timestamps':datetime.datetime.now().strftime("%H:%M:%S"),
                          'Date':datetime.datetime.now().strftime("%Y:%m:%d"),
                         'temp_lv_w1':t_lv1,
                        'temp_lv_w2':t_lv2,
                        'temp_hv':t_hv,
                        'OTI_temp':oti_t,
                        'transformer':"tf1"}
        """
        trans_json = tf1_c.to_json(orient='records')
        trans_dict = tf1_c.to_dict()

        return trans_json, trans_dict


if __name__ == '__main__':
    print('data generation module for transformer')
