Feature: Basic Operation of Cura

    Scenario: Add a machine
        Given Cura is running
         When we add a machine "ultimaker3" named as "UM3"
         Then check if the current machine is "UM3"

    Scenario: Set active quality to "normal"
        Given Cura is running
         When we set active quality to "normal"
         Then the quality below is activated
              | quality_type |
              |       normal |

    Scenario: Set active quality to "draft"
        Given Cura is running
         When we set active quality to "draft"
         Then the quality below is activated
              | quality_type |
              |        draft |

    Scenario: Save Gcode to file
        Given Cura is running
         When we load model "data/20x20x20.stl"
          And we slice
         Then we wait for 5 seconds
          And we save gcode to "output/gcode-20x20x20.gcode"
          And we wait for 5 seconds
