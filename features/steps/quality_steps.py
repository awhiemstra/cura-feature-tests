import time

from behave import when, then
from hamcrest import assert_that, equal_to


@when('we set active quality to "{quality_id}"')
def step_impl(context, quality_id):
    context.cura.setActiveQuality(quality_id)
    time.sleep(7)


@when('we slice')
def step_slice(context):
    context.cura.slice()


@then('the quality below is activated')
def step_impl(context):
    actual_quality_data = context.cura.getActiveQuality()
    assert context.table, "a table of quality is required"

    for row in context.table:
        for key, value in row.items():
            assert_that(key in actual_quality_data, "[%s] is not in the quality data [%s]" % (key, actual_quality_data))
            assert_that(str(value), equal_to(str(actual_quality_data[key])),
                        "field [%s] don't match" % key)
