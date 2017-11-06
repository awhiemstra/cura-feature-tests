Feature: Basic Operation of Cura

    Scenario: Add a machine
        Given Cura is running
         When we add a machine "ultimaker3" named as "UM3"
         Then check if the current machine is "UM3"

    Scenario: Add another UM3
        Given Cura is running
         When we add a machine "ultimaker3" named as "UM3"
         Then machine "UM3" should exist
          And machine "UM3 #2" should exist
          And check if the current machine is "UM3 #2"

    Scenario: Set active machine to UM3
        Given Cura is running
         When we set active machine to "UM3"
         Then check if the current machine is "UM3"

    Scenario: Rename UM3 to UM3_2
        Given Cura is running
         When we rename machine "UM3" to "UM3_2"
         Then check if the current machine is "UM3_2"

    Scenario: Remove UM3 #2
        Given Cura is running
         When we remove machine "UM3 #2"
         Then machine "UM3 #2" should not exist
