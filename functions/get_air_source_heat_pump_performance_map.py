from sys import argv
from typing import Literal

from resdx import (
    EnergyPlusSystemType,
    FanMotorType,
    RESNETDXModel,
    StagingType,
    get_idf_string,
)


def get_performance_map(
    stage_type: str,
    cooling_capacity_95_W: str,
    heating_capacity_47_W: str,
    heating_capacity_17_W: str,
    minimum_rated_temperature_degC: str,
    seer2: str,
    eer2: str,
    hspf2: str,
    motor_type: str,
    duct_type: str,
    heating_type: str,
) -> str:
    """
    Get IDF objects
    """
    stage_type_var: StagingType = StagingType[stage_type]

    cooling_capacity_95 = float(cooling_capacity_95_W)
    heating_capacity_47 = float(heating_capacity_47_W)
    heating_capacity_17 = float(heating_capacity_17_W)

    minimum_rated_temperature = float(minimum_rated_temperature_degC)

    seer2_value: float = float(seer2)
    eer2_value: float = float(eer2)
    hspf2_value: float = float(hspf2)

    motor_type_value: FanMotorType = FanMotorType[motor_type]

    if duct_type == "DUCTED":
        is_ducted = True
    else:  # duct_type == "DUCTLESS"
        is_ducted = False

    heating_type_enum: Literal["GAS", "ASHP", "ELECTRIC"]
    if heating_type == "ASHP":
        heating_type_enum = "ASHP"
    elif heating_type == "GAS":  # heating_type == "GAS" or heating_type == "ELECTRIC"
        heating_type_enum = "GAS"
    elif heating_type == "ELECTRIC":
        heating_type_enum = "ELECTRIC"
    else:
        raise TypeError(f"heating_type must be one of 'GAS', 'ASHP', or 'ELECTRIC'; got {heating_type}")
    

    unit = RESNETDXModel(
        staging_type=stage_type_var,
        rated_net_total_cooling_capacity=cooling_capacity_95,
        rated_net_heating_capacity=heating_capacity_47,
        rated_net_heating_capacity_17=heating_capacity_17,
        heating_off_temperature=minimum_rated_temperature,
        input_seer=seer2_value,
        input_eer=eer2_value,
        input_hspf=hspf2_value,
        motor_type=motor_type_value,
        is_ducted=is_ducted,
    )

    return get_idf_string(
        unit=unit,
        heating_type=heating_type_enum,
        system_name="HVAC",
        system_type=EnergyPlusSystemType.UNITARY_SYSTEM,
        autosize=False,
        normalize=False,
        get_fan=True,
        get_cooling_performance_map=True,
        get_heating_performance_map=True,
    )


if __name__ == "__main__":
    stage_type = argv[1]
    cooling_capacity_95_W = argv[2]
    heating_capacity_47_W = argv[3]
    heating_capacity_17_W = argv[4]
    minimum_rated_temperature_degC = argv[5]
    seer2 = argv[6]
    eer2 = argv[7]
    hspf2 = argv[8]
    motor_type = argv[9]
    duct_type = argv[10]
    heating_type = argv[11]    

    print(
        get_performance_map(
            stage_type=stage_type,
            cooling_capacity_95_W=cooling_capacity_95_W,
            heating_capacity_47_W=heating_capacity_47_W,
            heating_capacity_17_W=heating_capacity_17_W,
            minimum_rated_temperature_degC=minimum_rated_temperature_degC,
            seer2=seer2,
            eer2=eer2,
            hspf2=hspf2,
            motor_type=motor_type,
            duct_type=duct_type,
            heating_type=heating_type,
        )
    )
