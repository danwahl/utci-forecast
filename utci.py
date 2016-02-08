# -*- coding: utf-8 -*-
"""
utci calculator

borrowed from:
http://james-ramsden.com/calculate-utci-c-code/

valid for:
-50 <= Ta <= 50
0.5 <= va <= 17
-30 <= D_Tmrt <= 70
0 <= RH <= 100
"""

import math
import solar

# Sonntag 1990
DEWPOINT_A = 6.112    
DEWPOINT_B = 18.678
DEWPOINT_C = 257.14
DEWPOINT_D = 234.50

utci_name = ['extreme cold stress', 'very strong cold stress', 'strong cold stress', \
    'moderate cold stress', 'slight cold stress', 'no thermal stress', 'moderate heat stress', \
    'strong heat stress', 'very strong heat stress', 'extreme heat stress']
utci_color = [0x000080, 0x0000C0, 0x0000FF, 0x0060FF, 0x00C0FF, 0x00C000, 0xFF6600, 0xFF3300, 0xCC0000, 0x800000]
utci_scale = [-40, -27, -13, 0, 9, 26, 32, 38, 46]

def get_name(cat):
    return utci_name[cat]

def get_color(cat):
    return utci_color[cat]

def get_cat(utci):
#    if utci < utci_scale[0]:
#        return 0
#    elif utci > utci_scale[len(utci_scale) - 1]:
#        return len(utci_scale)
#    else:
#        for i in range(1, len(utci_scale)):
#            if utci < utci_scale[i]:
#                return i - 1 + (utci - utci_scale[i - 1])/(utci_scale[i] - utci_scale[i - 1])
        for i in range(len(utci_scale)):
            if utci < utci_scale[i]:
                return i
        return len(utci_scale) + 1

def get_utci(Ta, va, RH, lat, lon, cr, d):
    alt = solar.get_altitude(lat, lon, d)
    S = solar.get_radiation_cloud(d, alt, cr)/1000.0
    
    ehPa = get_es(Ta) * (RH / 100.0)
    Pa = ehPa / 10.0
    Tmrt = get_Tmrt(Ta, va, Pa, S)
    D_Tmrt = Tmrt - Ta
    
    #print alt, S, Pa, Tmrt
    
    return Ta + \
      (0.607562052) + \
      (-0.0227712343) * Ta + \
      (8.06470249 * math.pow(10, (-4))) * Ta * Ta + \
      (-1.54271372 * math.pow(10, (-4))) * Ta * Ta * Ta + \
      (-3.24651735 * math.pow(10, (-6))) * Ta * Ta * Ta * Ta + \
      (7.32602852 * math.pow(10, (-8))) * Ta * Ta * Ta * Ta * Ta + \
      (1.35959073 * math.pow(10, (-9))) * Ta * Ta * Ta * Ta * Ta * Ta + \
      (-2.25836520) * va + \
      (0.0880326035) * Ta * va + \
      (0.00216844454) * Ta * Ta * va + \
      (-1.53347087 * math.pow(10, (-5))) * Ta * Ta * Ta * va + \
      (-5.72983704 * math.pow(10, (-7))) * Ta * Ta * Ta * Ta * va + \
      (-2.55090145 * math.pow(10, (-9))) * Ta * Ta * Ta * Ta * Ta * va + \
      (-0.751269505) * va * va + \
      (-0.00408350271) * Ta * va * va + \
      (-5.21670675 * math.pow(10, (-5))) * Ta * Ta * va * va + \
      (1.94544667 * math.pow(10, (-6))) * Ta * Ta * Ta * va * va + \
      (1.14099531 * math.pow(10, (-8))) * Ta * Ta * Ta * Ta * va * va + \
      (0.158137256) * va * va * va + \
      (-6.57263143 * math.pow(10, (-5))) * Ta * va * va * va + \
      (2.22697524 * math.pow(10, (-7))) * Ta * Ta * va * va * va + \
      (-4.16117031 * math.pow(10, (-8))) * Ta * Ta * Ta * va * va * va + \
      (-0.0127762753) * va * va * va * va + \
      (9.66891875 * math.pow(10, (-6))) * Ta * va * va * va * va + \
      (2.52785852 * math.pow(10, (-9))) * Ta * Ta * va * va * va * va + \
      (4.56306672 * math.pow(10, (-4))) * va * va * va * va * va + \
      (-1.74202546 * math.pow(10, (-7))) * Ta * va * va * va * va * va + \
      (-5.91491269 * math.pow(10, (-6))) * va * va * va * va * va * va + \
      (0.398374029) * D_Tmrt + \
      (1.83945314 * math.pow(10, (-4))) * Ta * D_Tmrt + \
      (-1.73754510 * math.pow(10, (-4))) * Ta * Ta * D_Tmrt + \
      (-7.60781159 * math.pow(10, (-7))) * Ta * Ta * Ta * D_Tmrt + \
      (3.77830287 * math.pow(10, (-8))) * Ta * Ta * Ta * Ta * D_Tmrt + \
      (5.43079673 * math.pow(10, (-10))) * Ta * Ta * Ta * Ta * Ta * D_Tmrt + \
      (-0.0200518269) * va * D_Tmrt + \
      (8.92859837 * math.pow(10, (-4))) * Ta * va * D_Tmrt + \
      (3.45433048 * math.pow(10, (-6))) * Ta * Ta * va * D_Tmrt + \
      (-3.77925774 * math.pow(10, (-7))) * Ta * Ta * Ta * va * D_Tmrt + \
      (-1.69699377 * math.pow(10, (-9))) * Ta * Ta * Ta * Ta * va * D_Tmrt + \
      (1.69992415 * math.pow(10, (-4))) * va * va * D_Tmrt + \
      (-4.99204314 * math.pow(10, (-5))) * Ta * va * va * D_Tmrt + \
      (2.47417178 * math.pow(10, (-7))) * Ta * Ta * va * va * D_Tmrt + \
      (1.07596466 * math.pow(10, (-8))) * Ta * Ta * Ta * va * va * D_Tmrt + \
      (8.49242932 * math.pow(10, (-5))) * va * va * va * D_Tmrt + \
      (1.35191328 * math.pow(10, (-6))) * Ta * va * va * va * D_Tmrt + \
      (-6.21531254 * math.pow(10, (-9))) * Ta * Ta * va * va * va * D_Tmrt + \
      (-4.99410301 * math.pow(10, (-6))) * va * va * va * va * D_Tmrt + \
      (-1.89489258 * math.pow(10, (-8))) * Ta * va * va * va * va * D_Tmrt + \
      (8.15300114 * math.pow(10, (-8))) * va * va * va * va * va * D_Tmrt + \
      (7.55043090 * math.pow(10, (-4))) * D_Tmrt * D_Tmrt + \
      (-5.65095215 * math.pow(10, (-5))) * Ta * D_Tmrt * D_Tmrt + \
      (-4.52166564 * math.pow(10, (-7))) * Ta * Ta * D_Tmrt * D_Tmrt + \
      (2.46688878 * math.pow(10, (-8))) * Ta * Ta * Ta * D_Tmrt * D_Tmrt + \
      (2.42674348 * math.pow(10, (-10))) * Ta * Ta * Ta * Ta * D_Tmrt * D_Tmrt + \
      (1.54547250 * math.pow(10, (-4))) * va * D_Tmrt * D_Tmrt + \
      (5.24110970 * math.pow(10, (-6))) * Ta * va * D_Tmrt * D_Tmrt + \
      (-8.75874982 * math.pow(10, (-8))) * Ta * Ta * va * D_Tmrt * D_Tmrt + \
      (-1.50743064 * math.pow(10, (-9))) * Ta * Ta * Ta * va * D_Tmrt * D_Tmrt + \
      (-1.56236307 * math.pow(10, (-5))) * va * va * D_Tmrt * D_Tmrt + \
      (-1.33895614 * math.pow(10, (-7))) * Ta * va * va * D_Tmrt * D_Tmrt + \
      (2.49709824 * math.pow(10, (-9))) * Ta * Ta * va * va * D_Tmrt * D_Tmrt + \
      (6.51711721 * math.pow(10, (-7))) * va * va * va * D_Tmrt * D_Tmrt + \
      (1.94960053 * math.pow(10, (-9))) * Ta * va * va * va * D_Tmrt * D_Tmrt + \
      (-1.00361113 * math.pow(10, (-8))) * va * va * va * va * D_Tmrt * D_Tmrt + \
      (-1.21206673 * math.pow(10, (-5))) * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-2.18203660 * math.pow(10, (-7))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt + \
      (7.51269482 * math.pow(10, (-9))) * Ta * Ta * D_Tmrt * D_Tmrt * D_Tmrt + \
      (9.79063848 * math.pow(10, (-11))) * Ta * Ta * Ta * D_Tmrt * D_Tmrt * D_Tmrt + \
      (1.25006734 * math.pow(10, (-6))) * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-1.81584736 * math.pow(10, (-9))) * Ta * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-3.52197671 * math.pow(10, (-10))) * Ta * Ta * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-3.36514630 * math.pow(10, (-8))) * va * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (1.35908359 * math.pow(10, (-10))) * Ta * va * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (4.17032620 * math.pow(10, (-10))) * va * va * va * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-1.30369025 * math.pow(10, (-9))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (4.13908461 * math.pow(10, (-10))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (9.22652254 * math.pow(10, (-12))) * Ta * Ta * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-5.08220384 * math.pow(10, (-9))) * va * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-2.24730961 * math.pow(10, (-11))) * Ta * va * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (1.17139133 * math.pow(10, (-10))) * va * va * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (6.62154879 * math.pow(10, (-10))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (4.03863260 * math.pow(10, (-13))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (1.95087203 * math.pow(10, (-12))) * va * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (-4.73602469 * math.pow(10, (-12))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt + \
      (5.12733497) * Pa + \
      (-0.312788561) * Ta * Pa + \
      (-0.0196701861) * Ta * Ta * Pa + \
      (9.99690870 * math.pow(10, (-4))) * Ta * Ta * Ta * Pa + \
      (9.51738512 * math.pow(10, (-6))) * Ta * Ta * Ta * Ta * Pa + \
      (-4.66426341 * math.pow(10, (-7))) * Ta * Ta * Ta * Ta * Ta * Pa + \
      (0.548050612) * va * Pa + \
      (-0.00330552823) * Ta * va * Pa + \
      (-0.00164119440) * Ta * Ta * va * Pa + \
      (-5.16670694 * math.pow(10, (-6))) * Ta * Ta * Ta * va * Pa + \
      (9.52692432 * math.pow(10, (-7))) * Ta * Ta * Ta * Ta * va * Pa + \
      (-0.0429223622) * va * va * Pa + \
      (0.00500845667) * Ta * va * va * Pa + \
      (1.00601257 * math.pow(10, (-6))) * Ta * Ta * va * va * Pa + \
      (-1.81748644 * math.pow(10, (-6))) * Ta * Ta * Ta * va * va * Pa + \
      (-1.25813502 * math.pow(10, (-3))) * va * va * va * Pa + \
      (-1.79330391 * math.pow(10, (-4))) * Ta * va * va * va * Pa + \
      (2.34994441 * math.pow(10, (-6))) * Ta * Ta * va * va * va * Pa + \
      (1.29735808 * math.pow(10, (-4))) * va * va * va * va * Pa + \
      (1.29064870 * math.pow(10, (-6))) * Ta * va * va * va * va * Pa + \
      (-2.28558686 * math.pow(10, (-6))) * va * va * va * va * va * Pa + \
      (-0.0369476348) * D_Tmrt * Pa + \
      (0.00162325322) * Ta * D_Tmrt * Pa + \
      (-3.14279680 * math.pow(10, (-5))) * Ta * Ta * D_Tmrt * Pa + \
      (2.59835559 * math.pow(10, (-6))) * Ta * Ta * Ta * D_Tmrt * Pa + \
      (-4.77136523 * math.pow(10, (-8))) * Ta * Ta * Ta * Ta * D_Tmrt * Pa + \
      (8.64203390 * math.pow(10, (-3))) * va * D_Tmrt * Pa + \
      (-6.87405181 * math.pow(10, (-4))) * Ta * va * D_Tmrt * Pa + \
      (-9.13863872 * math.pow(10, (-6))) * Ta * Ta * va * D_Tmrt * Pa + \
      (5.15916806 * math.pow(10, (-7))) * Ta * Ta * Ta * va * D_Tmrt * Pa + \
      (-3.59217476 * math.pow(10, (-5))) * va * va * D_Tmrt * Pa + \
      (3.28696511 * math.pow(10, (-5))) * Ta * va * va * D_Tmrt * Pa + \
      (-7.10542454 * math.pow(10, (-7))) * Ta * Ta * va * va * D_Tmrt * Pa + \
      (-1.24382300 * math.pow(10, (-5))) * va * va * va * D_Tmrt * Pa + \
      (-7.38584400 * math.pow(10, (-9))) * Ta * va * va * va * D_Tmrt * Pa + \
      (2.20609296 * math.pow(10, (-7))) * va * va * va * va * D_Tmrt * Pa + \
      (-7.32469180 * math.pow(10, (-4))) * D_Tmrt * D_Tmrt * Pa + \
      (-1.87381964 * math.pow(10, (-5))) * Ta * D_Tmrt * D_Tmrt * Pa + \
      (4.80925239 * math.pow(10, (-6))) * Ta * Ta * D_Tmrt * D_Tmrt * Pa + \
      (-8.75492040 * math.pow(10, (-8))) * Ta * Ta * Ta * D_Tmrt * D_Tmrt * Pa + \
      (2.77862930 * math.pow(10, (-5))) * va * D_Tmrt * D_Tmrt * Pa + \
      (-5.06004592 * math.pow(10, (-6))) * Ta * va * D_Tmrt * D_Tmrt * Pa + \
      (1.14325367 * math.pow(10, (-7))) * Ta * Ta * va * D_Tmrt * D_Tmrt * Pa + \
      (2.53016723 * math.pow(10, (-6))) * va * va * D_Tmrt * D_Tmrt * Pa + \
      (-1.72857035 * math.pow(10, (-8))) * Ta * va * va * D_Tmrt * D_Tmrt * Pa + \
      (-3.95079398 * math.pow(10, (-8))) * va * va * va * D_Tmrt * D_Tmrt * Pa + \
      (-3.59413173 * math.pow(10, (-7))) * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (7.04388046 * math.pow(10, (-7))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (-1.89309167 * math.pow(10, (-8))) * Ta * Ta * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (-4.79768731 * math.pow(10, (-7))) * va * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (7.96079978 * math.pow(10, (-9))) * Ta * va * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (1.62897058 * math.pow(10, (-9))) * va * va * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (3.94367674 * math.pow(10, (-8))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (-1.18566247 * math.pow(10, (-9))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (3.34678041 * math.pow(10, (-10))) * va * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (-1.15606447 * math.pow(10, (-10))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * Pa + \
      (-2.80626406) * Pa * Pa + \
      (0.548712484) * Ta * Pa * Pa + \
      (-0.00399428410) * Ta * Ta * Pa * Pa + \
      (-9.54009191 * math.pow(10, (-4))) * Ta * Ta * Ta * Pa * Pa + \
      (1.93090978 * math.pow(10, (-5))) * Ta * Ta * Ta * Ta * Pa * Pa + \
      (-0.308806365) * va * Pa * Pa + \
      (0.0116952364) * Ta * va * Pa * Pa + \
      (4.95271903 * math.pow(10, (-4))) * Ta * Ta * va * Pa * Pa + \
      (-1.90710882 * math.pow(10, (-5))) * Ta * Ta * Ta * va * Pa * Pa + \
      (0.00210787756) * va * va * Pa * Pa + \
      (-6.98445738 * math.pow(10, (-4))) * Ta * va * va * Pa * Pa + \
      (2.30109073 * math.pow(10, (-5))) * Ta * Ta * va * va * Pa * Pa + \
      (4.17856590 * math.pow(10, (-4))) * va * va * va * Pa * Pa + \
      (-1.27043871 * math.pow(10, (-5))) * Ta * va * va * va * Pa * Pa + \
      (-3.04620472 * math.pow(10, (-6))) * va * va * va * va * Pa * Pa + \
      (0.0514507424) * D_Tmrt * Pa * Pa + \
      (-0.00432510997) * Ta * D_Tmrt * Pa * Pa + \
      (8.99281156 * math.pow(10, (-5))) * Ta * Ta * D_Tmrt * Pa * Pa + \
      (-7.14663943 * math.pow(10, (-7))) * Ta * Ta * Ta * D_Tmrt * Pa * Pa + \
      (-2.66016305 * math.pow(10, (-4))) * va * D_Tmrt * Pa * Pa + \
      (2.63789586 * math.pow(10, (-4))) * Ta * va * D_Tmrt * Pa * Pa + \
      (-7.01199003 * math.pow(10, (-6))) * Ta * Ta * va * D_Tmrt * Pa * Pa + \
      (-1.06823306 * math.pow(10, (-4))) * va * va * D_Tmrt * Pa * Pa + \
      (3.61341136 * math.pow(10, (-6))) * Ta * va * va * D_Tmrt * Pa * Pa + \
      (2.29748967 * math.pow(10, (-7))) * va * va * va * D_Tmrt * Pa * Pa + \
      (3.04788893 * math.pow(10, (-4))) * D_Tmrt * D_Tmrt * Pa * Pa + \
      (-6.42070836 * math.pow(10, (-5))) * Ta * D_Tmrt * D_Tmrt * Pa * Pa + \
      (1.16257971 * math.pow(10, (-6))) * Ta * Ta * D_Tmrt * D_Tmrt * Pa * Pa + \
      (7.68023384 * math.pow(10, (-6))) * va * D_Tmrt * D_Tmrt * Pa * Pa + \
      (-5.47446896 * math.pow(10, (-7))) * Ta * va * D_Tmrt * D_Tmrt * Pa * Pa + \
      (-3.59937910 * math.pow(10, (-8))) * va * va * D_Tmrt * D_Tmrt * Pa * Pa + \
      (-4.36497725 * math.pow(10, (-6))) * D_Tmrt * D_Tmrt * D_Tmrt * Pa * Pa + \
      (1.68737969 * math.pow(10, (-7))) * Ta * D_Tmrt * D_Tmrt * D_Tmrt * Pa * Pa + \
      (2.67489271 * math.pow(10, (-8))) * va * D_Tmrt * D_Tmrt * D_Tmrt * Pa * Pa + \
      (3.23926897 * math.pow(10, (-9))) * D_Tmrt * D_Tmrt * D_Tmrt * D_Tmrt * Pa * Pa + \
      (-0.0353874123) * Pa * Pa * Pa + \
      (-0.221201190) * Ta * Pa * Pa * Pa + \
      (0.0155126038) * Ta * Ta * Pa * Pa * Pa + \
      (-2.63917279 * math.pow(10, (-4))) * Ta * Ta * Ta * Pa * Pa * Pa + \
      (0.0453433455) * va * Pa * Pa * Pa + \
      (-0.00432943862) * Ta * va * Pa * Pa * Pa + \
      (1.45389826 * math.pow(10, (-4))) * Ta * Ta * va * Pa * Pa * Pa + \
      (2.17508610 * math.pow(10, (-4))) * va * va * Pa * Pa * Pa + \
      (-6.66724702 * math.pow(10, (-5))) * Ta * va * va * Pa * Pa * Pa + \
      (3.33217140 * math.pow(10, (-5))) * va * va * va * Pa * Pa * Pa + \
      (-0.00226921615) * D_Tmrt * Pa * Pa * Pa + \
      (3.80261982 * math.pow(10, (-4))) * Ta * D_Tmrt * Pa * Pa * Pa + \
      (-5.45314314 * math.pow(10, (-9))) * Ta * Ta * D_Tmrt * Pa * Pa * Pa + \
      (-7.96355448 * math.pow(10, (-4))) * va * D_Tmrt * Pa * Pa * Pa + \
      (2.53458034 * math.pow(10, (-5))) * Ta * va * D_Tmrt * Pa * Pa * Pa + \
      (-6.31223658 * math.pow(10, (-6))) * va * va * D_Tmrt * Pa * Pa * Pa + \
      (3.02122035 * math.pow(10, (-4))) * D_Tmrt * D_Tmrt * Pa * Pa * Pa + \
      (-4.77403547 * math.pow(10, (-6))) * Ta * D_Tmrt * D_Tmrt * Pa * Pa * Pa + \
      (1.73825715 * math.pow(10, (-6))) * va * D_Tmrt * D_Tmrt * Pa * Pa * Pa + \
      (-4.09087898 * math.pow(10, (-7))) * D_Tmrt * D_Tmrt * D_Tmrt * Pa * Pa * Pa + \
      (0.614155345) * Pa * Pa * Pa * Pa + \
      (-0.0616755931) * Ta * Pa * Pa * Pa * Pa + \
      (0.00133374846) * Ta * Ta * Pa * Pa * Pa * Pa + \
      (0.00355375387) * va * Pa * Pa * Pa * Pa + \
      (-5.13027851 * math.pow(10, (-4))) * Ta * va * Pa * Pa * Pa * Pa + \
      (1.02449757 * math.pow(10, (-4))) * va * va * Pa * Pa * Pa * Pa + \
      (-0.00148526421) * D_Tmrt * Pa * Pa * Pa * Pa + \
      (-4.11469183 * math.pow(10, (-5))) * Ta * D_Tmrt * Pa * Pa * Pa * Pa + \
      (-6.80434415 * math.pow(10, (-6))) * va * D_Tmrt * Pa * Pa * Pa * Pa + \
      (-9.77675906 * math.pow(10, (-6))) * D_Tmrt * D_Tmrt * Pa * Pa * Pa * Pa + \
      (0.0882773108) * Pa * Pa * Pa * Pa * Pa + \
      (-0.00301859306) * Ta * Pa * Pa * Pa * Pa * Pa + \
      (0.00104452989) * va * Pa * Pa * Pa * Pa * Pa + \
      (2.47090539 * math.pow(10, (-4))) * D_Tmrt * Pa * Pa * Pa * Pa * Pa + \
      (0.00148348065) * Pa * Pa * Pa * Pa * Pa * Pa

def get_Tmrt(Ta, va, pa, S):
    # https://en.wikipedia.org/wiki/Mean_radiant_temperature
    Tg = get_Tg(Ta, va, pa, S)
    return pow(pow(Tg + 273, 4) + 2.5*pow(10, 8)*pow(va, 0.6)*(Tg - Ta), 0.25) - 273

def get_Tg(Ta, va, Pa, S):
    # http://www.srh.noaa.gov/images/tsa/pubs/WBGTpaper2.pdf
    ea = 0.575*pow(Pa, 1.0/7.0)
    B = S/pow(5.67, -8) + ea*pow(Ta, 4)
    C = 0.315*pow(va*3600.0, 0.58)/pow(5.3865, -8)
    #print ea, B, C
    return (B + C*Ta + 7680000)/(C + 256000)
    

def get_Td(Ta, RH):
    # dew point calculation (http://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point)
    g = math.log(RH/100.0*math.exp((DEWPOINT_B - ta/DEWPOINT_D)*(Ta/(DEWPOINT_C + Ta))))
    return DEWPOINT_C*g/(DEWPOINT_B - g);

'''
calculates saturation vapour pressure over water in hPa for input air temperature (ta) in celsius according to:
Hardy, R.; ITS-90 Formulations for Vapor Pressure, Frostpoint Temperature, Dewpoint Temperature and Enhancement Factors in the Range -100 to 100 °C; 
Proceedings of Third International Symposium on Humidity and Moisture; edited by National Physical Laboratory (NPL), London, 1998, pp. 214-221
http://www.thunderscientific.com/tech_info/reflibrary/its90formulas.pdf (retrieved 2008-10-01)
'''
def get_es(ta):
    g = [-2836.5744, -6028.076559, 19.54263612, -0.02737830188, 0.000016261698, ((7.0229056 * math.pow(10, -10))), ((-1.8680009 * math.pow(10, -13)))]
    tk = ta + 273.15
    es = 2.7150305 * math.log(tk)
    
    for count in range(len(g)):
        i = g[count]
        es = es + (i * math.pow(tk, (count - 2)))
    
    return math.exp(es) * 0.01
    # http://www.srh.noaa.gov/images/epz/wxcalc/vaporPressure.pdf
    #return 6.11*pow(10, (7.5*ta)/(237.3 + ta))