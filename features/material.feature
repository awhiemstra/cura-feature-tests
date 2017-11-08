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

    Scenario: Create a new material
        Given Cura is running
         When we create a new material "my_material" named as "My Material"
         Then material "my_material" should exist

    Scenario: Duplicate a material
        Given Cura is running
         When we duplicate from material "generic_abs" as "my_duplicated_abs"
         Then the following materials are present
              | id                | name           |
              | my_duplicated_abs | Generic ABS #2 |
              | my_material       | My Material    |

    Scenario: Remove a material
        Given Cura is running
         When we remove material "my_duplicated_abs"
         Then material "my_duplicated_abs" should not exist

    Scenario: Rename a material
        Given Cura is running
         When we rename material "my_material" as "My New Material"
         Then the following materials are present
              | id                | name            |
              | my_material       | My New Material |

    Scenario: Import a material
        Given Cura is running
         When we import material "data/test_abs_material.xml.fdm_material"
         Then the following materials are present
              | id                | name          | brand | material |
              | test_abs_material | Test Material | Test  | ABS      |

    Scenario: Export a material
        Given Cura is running
         When we export material "test_abs_material" to file "output/test_abs_material.xml.fdm_material"
         Then files "data/test_abs_material.xml.fdm_material" and "output/test_abs_material.xml.fdm_material" are the same
