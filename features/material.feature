Feature: Basic Operations for Materials in Cura

    Scenario: Set active material to Generic PP
        Given Cura is running
         When we add a machine "ultimaker3" named as "UM3"
          And we set active material to "generic_pp"
         Then check if the current machine is "UM3"
          And check if the active material is "generic_pp"

    Scenario: Set active material to Generic ABS
        Given Cura is running
         When we set active material to "generic_abs"
         Then check if the current machine is "UM3"
          And check if the active material is "generic_abs"

    Scenario: Set active material to Ultimaker CPE White
        Given Cura is running
         When we set active material to "ultimaker_cpe_white"
         Then check if the current machine is "UM3"
          And check if the active material is "ultimaker_cpe_white"
