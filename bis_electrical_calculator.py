import math

class BISElectricalCalculator:
    """
    Python calculation engine for Indian Electrical Standards (BIS Codes)
    Covers:
    - Conduit Fill & Space Factor (IS 732 / NEC / IS 9537)
    - Cable Derating & Sizing (IS 732 / IS 694 / IS 1554 / IS 7098)
    - Earth Electrode Resistance (IS 3043)
    """

    # Non-metallic conduits (MMS Grade) internal cross-sectional area (mm²) per IS 9537-3
    CONDUIT_SIZES_MMS = {
        16: 133.0,
        20: 224.0,
        25: 360.0,
        32: 607.0,
        40: 984.0,
        50: 1541.0,
        63: 2552.0
    }

    # Cable Cross-sectional areas (mm²) for single-core PVC cables per IS 694
    CABLE_AREAS_IS694 = {
        0.5: 4.15,
        0.75: 4.91,
        1.0: 5.73,
        1.5: 8.55,  # Class 2 stranded
        2.5: 12.57,
        4.0: 16.62,
        6.0: 21.24,
        10.0: 35.26,
        16.0: 47.78
    }

    @staticmethod
    def calculate_conduit_size(cables_dict, num_90_bends=0):
        """
        cables_dict: dict of {cable_size_sqmm: quantity}
        num_90_bends: number of 90 degree bends in run
        Returns selected conduit size (mm) and fill details
        """
        total_cable_area = 0.0
        total_cables_count = sum(cables_dict.values())

        for size_sqmm, qty in cables_dict.items():
            if size_sqmm not in BISElectricalCalculator.CABLE_AREAS_IS694:
                raise ValueError(f"Unsupported cable size: {size_sqmm} sqmm")
            total_cable_area += BISElectricalCalculator.CABLE_AREAS_IS694[size_sqmm] * qty

        # Permissible Fill Factor as per National Electrical Code (NEC) & IS 732:
        # 1 cable: 53%, 2 cables: 31%, 3+ cables: 40%
        if total_cables_count == 1:
            fill_factor = 0.53
        elif total_cables_count == 2:
            fill_factor = 0.31
        else:
            fill_factor = 0.40

        required_conduit_area = total_cable_area / fill_factor

        # Bend derating: For every two 90 degree bends, conduit area capacity reduced by 15%
        if num_90_bends >= 2:
            bend_derating = 0.85 ** (num_90_bends // 2)
        else:
            bend_derating = 1.0

        selected_conduit = None
        for size_mm, area_sqmm in sorted(BISElectricalCalculator.CONDUIT_SIZES_MMS.items()):
            effective_area = area_sqmm * bend_derating
            if effective_area >= required_conduit_area:
                selected_conduit = size_mm
                break

        return {
            "total_cables": total_cables_count,
            "total_cable_area_sqmm": round(total_cable_area, 2),
            "fill_factor_percentage": fill_factor * 100,
            "required_conduit_area_sqmm": round(required_conduit_area, 2),
            "bend_derating_factor": round(bend_derating, 2),
            "recommended_conduit_size_mm": selected_conduit,
            "standard_reference": "IS 732:2019 / IS 9537 Part 3"
        }

    @staticmethod
    def calculate_pipe_earth_resistance(soil_resistivity_ohm_m, pipe_length_m, pipe_diameter_m):
        """
        Pipe Electrode resistance formula per IS 3043:
        R = (100 * rho / (2 * pi * L)) * ln(4 * L / d)   [in Ohms]
        rho: Soil resistivity (Ohm-meter)
        L: Pipe length in cm
        d: Pipe diameter in cm
        """
        L_cm = pipe_length_m * 100.0
        d_cm = pipe_diameter_m * 100.0

        R = (100.0 * soil_resistivity_ohm_m / (2.0 * math.pi * L_cm)) * math.log(4.0 * L_cm / d_cm)
        return {
            "soil_resistivity_ohm_m": soil_resistivity_ohm_m,
            "pipe_length_m": pipe_length_m,
            "pipe_diameter_mm": pipe_diameter_m * 1000,
            "calculated_earth_resistance_ohms": round(R, 3),
            "standard_reference": "IS 3043:2018 Section 2 (Clause 9)"
        }

    @staticmethod
    def calculate_plate_earth_resistance(soil_resistivity_ohm_m, plate_area_sqm):
        """
        Plate Electrode resistance formula per IS 3043:
        R = (rho / 4) * sqrt(pi / Area)
        rho: Soil resistivity (Ohm-meter)
        Area: Plate surface area (sq. meters)
        """
        R = (soil_resistivity_ohm_m / 4.0) * math.sqrt(math.pi / plate_area_sqm)
        return {
            "soil_resistivity_ohm_m": soil_resistivity_ohm_m,
            "plate_area_sqm": plate_area_sqm,
            "calculated_earth_resistance_ohms": round(R, 3),
            "standard_reference": "IS 3043:2018 Section 2 (Clause 9)"
        }

    @staticmethod
    def calculate_derated_cable_current(base_current_amps, ambient_temp_c, harmonic_percentage=0):
        """
        Derating factor calculation based on IS 732 / Annexure III & Table 3
        """
        # Ambient temperature correction factor for PVC in air (base 30 C)
        temp_factors_pvc = {
            20: 1.12, 25: 1.06, 30: 1.00, 35: 0.94,
            40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61
        }
        temp_factor = temp_factors_pvc.get(ambient_temp_c, 1.00)

        # Harmonic reduction factor per Table 3
        if harmonic_percentage <= 15:
            harmonic_factor = 1.0
        elif harmonic_percentage <= 33:
            harmonic_factor = 0.86
        else:
            harmonic_factor = 0.86  # Based on neutral current sizing

        derated_capacity = base_current_amps * temp_factor * harmonic_factor
        return {
            "base_current_amps": base_current_amps,
            "ambient_temp_c": ambient_temp_c,
            "temp_correction_factor": temp_factor,
            "harmonic_reduction_factor": harmonic_factor,
            "derated_safe_current_amps": round(derated_capacity, 2),
            "standard_reference": "IS 732:2019 Annex S / BIS Handbook Table 3"
        }

if __name__ == "__main__":
    print("=== Testing BIS Electrical Calculator Engine ===")
    calc = BISElectricalCalculator()

    # Test 1: Conduit Size for 9 cables (2x1.5 + 2x4.0 + 1x1.5 + 4x1.5) with 2 bends
    conduit_res = calc.calculate_conduit_size({1.5: 5, 4.0: 2, 2.5: 2}, num_90_bends=2)
    print("Conduit Calculation Result:", conduit_res)

    # Test 2: Pipe Earth Resistance (100 Ohm-m soil, 2.5m GI Pipe 50mm dia)
    pipe_res = calc.calculate_pipe_earth_resistance(soil_resistivity_ohm_m=100, pipe_length_m=2.5, pipe_diameter_m=0.050)
    print("Pipe Earth Resistance Result:", pipe_res)

    # Test 3: Plate Earth Resistance (100 Ohm-m soil, 0.6m x 0.6m CI Plate)
    plate_res = calc.calculate_plate_earth_resistance(soil_resistivity_ohm_m=100, plate_area_sqm=0.36)
    print("Plate Earth Resistance Result:", plate_res)

    # Test 4: Cable Derating for 32A load at 45°C with 20% harmonic content
    derate_res = calc.calculate_derated_cable_current(base_current_amps=32, ambient_temp_c=45, harmonic_percentage=20)
    print("Cable Derating Result:", derate_res)
