import time

from behave import when, then
from hamcrest import assert_that, equal_to


@when('we set active material to "{material_id}"')
def step_set_active_material(context, material_id):
    context.cura.setActiveMaterial(material_id)
    time.sleep(5)


@when('we create a new material "{material_id}" named as "{material_name}"')
def step_create_material(context, material_id, material_name):
    context.cura.createMaterial(material_id, material_name)
    time.sleep(5)


@when('we duplicate from material "{material_id}" as "{new_material_id}"')
def step_duplicate_material(context, material_id, new_material_id):
    context.cura.duplicateMaterial(material_id, new_material_id)
    time.sleep(5)


@when('we remove material "{material_id}"')
def step_remove_material(context, material_id):
    context.cura.removeMaterial(material_id)
    time.sleep(2)


@when('we rename material "{material_id}" as "{new_material_name}"')
def step_rename_material(context, material_id, new_material_name):
    context.cura.renameMaterial(material_id, new_material_name)
    time.sleep(1)


@then('check if the active material is "{material_id}"')
def step_check_active_material(context, material_id):
    active_material_id = context.cura.getActiveMaterial()["id"]
    assert_that(active_material_id, equal_to(material_id))


@then('material "{material_id}" should exist')
def step_has_material(context, material_id):
    result = context.cura.hasMaterial(material_id)
    assert_that(result, equal_to(True))


@then('the following materials are present')
def step_materials_are_present(context):
    assert context.table, "a table of materials is required"

    # process the table
    expected_materials = []
    for row in context.table:
        expected_materials.append({"id": row["id"],
                                   "name": row["name"]})

    # check expected materials
    for expected_material in expected_materials:
        actual_material_dict = context.cura.getMaterial(expected_material["id"])
        actual_material = None
        if actual_material_dict is not None:
            actual_material = {k: actual_material_dict[k] for k in expected_material}

        assert_that(actual_material, expected_material)


@then('material "{material_id}" should not exist')
def step_has_not_material(context, material_id):
    result = context.cura.hasMaterial(material_id)
    assert_that(result, equal_to(False))
