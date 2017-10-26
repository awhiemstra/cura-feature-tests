Feature: Basic Operation of Cura

    Scenario: Load a model
        Given Cura is running
        When we load model 20x20x20.stl
        Then it will start slicing
