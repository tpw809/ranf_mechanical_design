"""Process spring json input file.

Use functional programming instead of object oriented...

focus on web-app interface...

User can input as little or as much as they want...

Unitless... must use consistent units:

Metric: mm, N, MPa, C

English: in, lb, psi, F

Parameters:

- name: descriptor

"""
import numpy as np


def process_helical_compression_spring_json_input(input_dict: dict):
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
    
    assert input_dict['E'] > 0.0
    
    ###########################################
    # identify / alert any missing required data:
    ###########################################
    
    
    
    ###########################################
    # check for inputs and compute missing data:
    ###########################################
    
    # check / fill contact yield strength:
    if input_dict.get('Scy') is None:
        input_dict['Scy'] = calc_Scy(input_dict['Sty'])
    else:
        assert input_dict['Scy'] >= 0.0
    

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
    