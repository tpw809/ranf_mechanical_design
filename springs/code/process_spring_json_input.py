"""Process spring json input file.

Use functional programming instead of object oriented...

focus on web-app interface...

User can input as little or as much as they want...

Unitless... must use consistent units:

Metric: mm, N, MPa, C

English: in, lb, psi, F

Parameters:

- name: descriptor
- ultimate_safety_factor
- yield_safety_factor
- material name
- material ultimate strength
- material yield strength
- material elastic limit
- material modulus
- end constraints for buckling
- handedness (left or right)
- end type
- condition (peened, preset)
- wire diameter
- wire diameter tolerance
- minimum tensile strength 
- spring rate
- spring index
- natural frequency
- coil inner diameter
- coil mean diameter
- coil outer diameter
- number of active coils
- number of total coils
- pitch
- pitch angle
- free length
- solid length
- load at solid length
- corrected stress at solid length
- corrected % of MTS at solid
- expanded coil outer diameter at solid
-length at buckling


Load Case Specific Parameters:

- load
- load tolerance
- length at load
- deflection at load
- % of max deflection
- corrected stress
- corrected stress % of MTS
- uncorrected stress
- uncorrected stress % of MTS
- expanded coil outer diameter

Design Scenarios:

- two-load
- one-load
- rate
- dimensional
- minimum weight

References:

- MIL-STD-29A
- AFFDL-TR-69-42 Stress Analysis Manual, section 1.5.4
- Shigley, Mechanical Engineering Design, 5th Ed.
- Machinery Handbook
- NASA-STD-5017B

"""
import numpy as np


def process_helical_compression_spring_json_input(
        input_dict: dict, 
        verbose:bool=False,
    ):
    """Process input dictionary and compute missing parameters.
    
    type: helical_compression_spring
    
    Must supply:
    - name: descriptor
    - 
    
    Optional:
    - 
    """
    ###########################################
    # check input validity:
    ###########################################
    
    assert input_dict['type'] == 'helical_compression_spring', "type must be helical_compression_spring"
    
    assert input_dict.get('name') is not None
    
    # if name is "", generate unique name...
    
    assert input_dict['material']['E'] > 0.0
    
    
    
    
    
    assert input_dict['yield_safety_factor']['E'] > 1.0
    assert input_dict['ultimate_safety_factor']['E'] > 1.0
    
    ###########################################
    # identify / alert any missing required data:
    ###########################################
    
    
    # wire shape:
    #shape = 'square'
    #shape = 'rectangular'
    shape = 'round'
    
    # End Type:
    # end_type = 'open_not_ground'
    # end_type = 'open_end_ground'
    # end_type = 'closed_not_ground'
    end_type = 'closed_end_ground'
    
    
    # [mm], wire diameter:
    d_wire = 1.0
    
    # [mm], wire side length of square wire:
    b = 1.0
    
    # [mm], mean coil diameter at free length:
    D_mean = 10.0
    
    # [mm/turn], pitch at free length:
    p = 1.0
    
    # [mm], spring radius:
    r = D_mean / 2.0
    
    
    
    
    
    # Service:
    # Light: static loads, small deflections, seldom used, 1e3 to 1e4 deflections
    # Average: general use, 1e5 to 1e6 deflections
    # Severe: rapid deflections, shock loading, valves, 1e6 to 1e7 deflections
    
    
    
    
    ###########################################
    # [-], Spring Index (C):
    ###########################################
    
    # Spring index should be from 5 to 15, 7 to 9 is ideal
    # typically 6 to 12 (Shigley)
    # called 'm' in stress analysis manual
    if shape == 'round':
        C = D_mean / d_wire
    elif shape == 'square':
        C = D_mean / b
    
    if verbose:
        print(f"Spring Index, C = D / d = {C}")
    
    input_dict['spring_index'] = C
    
    
    ############################################
    # Solid Height:
    ############################################
    
    # TC = total coils
    
    if end_type == 'open_not_ground':
        SH = (TC + 1) * d_wire
    elif end_type == 'open_end_ground':
        SH = TC * d_wire
    elif end_type == 'closed_not_ground':
        SH = (TC + 1) * d_wire
    elif end_type == 'closed_end_ground':
        SH = TC * d_wire
    else:
        raise Exception('select valid end_type')
    
    if verbose:
        print(f"solid height (SH): {SH}")
    
    input_dict['solid_height'] = SH
    
    ###########################################
    # check for inputs and compute missing data:
    ###########################################
    
    # check / fill contact yield strength:
    if input_dict.get('Scy') is None:
        input_dict['Scy'] = calc_Scy(input_dict['Sty'])
    else:
        assert input_dict['Scy'] >= 0.0
    
    
    
    
    ############################################
    # MIL-STD-29A, section 21.1: Design Formulas
    ############################################
    
    # Table II:
    
    if shape == 'round':
        # torsional stress:
        # S_t = (P * D) / (0.393 * d**2)
        S_t = 8.0 * P * D_mean / (np.pi * d_wire**3)
        # S_t = (G * d * F) / (np.pi * N *D**2)
    
        # deflection:
        F = (8.0 * P * N * D_mean**3) / (G * d_wire**4)
        # F = (w * S_t * N * D**3) / (G * d)
        
        # helical compression spring rate:
        k = (G * d_wire**4) / (8.0 * D_mean**3 * N)
        
        # spring rate (shigley):
        k_shigley = d_wire**4 * G / (8.0 * D_mean**3 * N)
        
        # max shear stress in the spring:
        # stress analysis manual, pg 1-95:
        # s_max = 16.0 * P * r / (np.pi * d**3) * (1.0 + d / (4.0 * r))
        s_max = 16.0 * P * r / (np.pi * d_wire**3)
        
        # max shear stress in wire (Shigley):
        tau_max = 8.0 * P * D_mean / (np.pi * d_wire**3)
        
        # deflection:
        # stress analysis manual, pg 1-95:
        delta = 64.0 * P*r**3*N / (G * d_wire**4)
    
    elif shape == 'square':
        # max shear stress in the spring:
        # stress analysis manual, pg 1-96:
        s_max = 4.80 * P * r / b**3
        
        # deflection:
        # stress analysis manual, pg 1-96:
        delta = 44.5 * P * r**3 * N / (G * b**4)
    
    
    
    
    ############################################
    # MIL-STD-29A, section 21.3: Diameter Changes in Compression Springs
    ############################################
    
    # Increase in outside diameter when compressed:
    
    # OD_c = outside diameter at solid length:
    OD_c = np.sqrt(D_mean**2 + (p**2 - d_wire**2)/np.pi**2) + d_wire
    
    if verbose:
        print(f"OD_c = {OD_c}")

    input_dict['OD_c'] = OD_c
    
    
    
    ############################################
    # MIL-STD-29A, section 21.11: Curvature Stress-Correction Factors
    ############################################
    
    # Shear Stress Correction Factor:
    k_shear = (2.0 * C + 1.0) / (2.0 * C)
    
    if verbose:
        print(f"k_shear = {k_shear}")
    
    input_dict['k_shear'] = k_shear
    
    
    # Curvature Stress Correction Factor: K
    # Wahl Stress Correction Factor, K_w
    K_wahl = (4.0 * C - 1.0) / (4.0 * C - 4.0) + 0.615 / C
    
    if verbose:
        print(f"K_wahl = {K_wahl}")
    
    input_dict['k_wahl'] = k_wahl
    
    
    # Bergstrasser Factor:
    K_berg = (4.0 * C + 2.0) / (4.0 * C - 3.0)
    
    if verbose:
        print(f"K_berg = {K_berg}")
    
    input_dict['k_berg'] = k_berg
    
    
    # Curvature stress correction factor:
    k_curv = K_wahl / k_shear
    
    if verbose:
        print(f"k_curv = {k_curv}")
    
    input_dict['k_curv'] = k_curv
    
    
    # Max shear stress:
    s_max = s_max * K_wahl
    
    if verbose:
        print(f"s_max = {s_max} [MPa]")
    
    S_t_max = S_t * K_wahl
    
    if verbose:
        print(f"S_t_max = {S_t_max} [MPa]")
    
    # max shear stress in wire (Shigley):
    tau_max = tau_max * K_wahl
    
    if verbose:
        print(f"tau_max = {tau_max} [MPa]")
    
    # as spring diameter increases, this approaches:
    # (1.0 + d / (4.0 * r))
    
    
    
    
    
    
    
    ############################################
    # Buckling Stability
    ############################################
    
    # alpha = end condition constant
    alpha = 0.0
    
    # lambda_eff = slenderness ratio
    lambda_eff = alpha * L0 / D
    
    
    y_cr = L0 * c1 * (1.0 - (1.0 - c2/lambda_eff**2)**(0.5))
    
    
    
    
    
    
    ############################################
    # Spring Strength Margin of Safety
    ############################################
    
    MS_shear = ((SF_ultimate * tau_max) / S_su) - 1.0
    
    if verbose:
        print(f"MS_shear = {MS_shear}")
    
    input_dict['MS_shear'] = MS_shear
    

    ###########################################
    # return dictionary with new data:
    ###########################################
    
    return input_dict


def main() -> None:
    
    input_dict = {
        "type": "helical_compression_spring",
        "name": "LeeSpring_LHL_375B_04_Hefty_Die",
        "units": "lb_in_F",
        "wire_shape": "round",
        "end_type": "closed_end_ground",
        "wire_diameter": 0.059,
        "mean_diameter": 10.0,
        "free_length": 1.75,
        "free_length_pitch": None,
        "mean_radius": 5.0,
        "service": "light",
        "spring_index": None,
        "outer_diameter": None,
        "inner_diameter": None,
        "spring_rate": 58.0,
        "active_coils": 15.75,
        "total_coils": 17.75,
        "yield_safety_factor": 1.25,
        "ultimate_safety_factor": 1.4,
        "material": {
            "name": "Music Wire",
            "spec": "ASTM A228",
            "units": "lb_in_F",
            "elastic_modulus": 30.0e6,
            "torsion_modulus": 11.5e6,
            "elastic_limit_ratio": 0.6,
            "ultimate_tensile_strength": 300.0e3,
            "ultimate_shear_strength": None,
            "max_operating_temperature": 250.0,
            "density": 0.28,
            "description": "",
        },
        "axial_load": 1.0,
        "solid_height": 1.04,
        "load_at_solid_height": None,
        "torsional_stress": None,
        "deflection": None,
        "outer_diameter_increase": None,
        "slenderness_ratio": None,
        "helix_direction": None,
        "shear_stress_correction_factor": None,
        "wahl_curvature_stress_correction_factor": None,
        "shear_stress_margin": None,
        "natural_frequency": None,
    }
    print(f"\ninput_dict = \n{input_dict}\n")
    
    output_dict = process_helical_compression_spring_json_input(input_dict)
    print(f"\noutput_dict = \n{output_dict}\n")
    
    
if __name__ == "__main__":
    main()
    