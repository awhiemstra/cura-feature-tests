import os
import hashlib

from behave import when, then
from hamcrest import assert_that, equal_to


@then('the following files are present')
def step_check_file_is_present(context):
    assert context.table, "a table of files is required"

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    # process the table
    missing_file_list = []
    for row in context.table:
        file_path = os.path.join(base_path, row["file"])

        if not os.path.exists(file_path):
            missing_file_list.append(row["file"])

    assert_that(missing_file_list, equal_to([]), "Found missing files")


@then('files "{file1}" and "{file2}" are the same')
def step_check_files_are_the_same(context, file1, file2):
    file1_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", file1))
    file2_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", file2))

    assert_that(os.path.exists(file1_path), "file1 [%s] should exist" % file1_path)
    assert_that(os.path.exists(file2_path), "file2 [%s] should exist" % file2_path)

    hash1 = hashlib.sha1()
    hash2 = hashlib.sha1()
    with open(file1_path, "rb") as f:
        hash1.update(f.read())
    with open(file2_path, "rb") as f:
        hash2.update(f.read())

    assert_that(hash1.hexdigest(), equal_to(hash2.hexdigest()))
