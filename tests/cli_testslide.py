# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os

import testslide.cli as ts_cli
from testslide.dsl import context


@context
def testslide_cli_helpers(context) -> None:
    @context.sub_context
    def when_the_platform_looks_like_Windows(context) -> None:
        @context.before
        def before(self):
            self.mock_callable(os.path, "isfile").for_call(
                r".\test\joker.py"
            ).to_return_value(True).and_assert_called()
            self.mock_callable(os.path, "isabs").for_call(
                r".\test\joker.py"
            ).to_return_value(False).and_assert_called()
            # Getting the raw backslash is hard; Unicode to the rescue
            self.patch_attribute(os.path, "sep", "\u005C")

        @context.example
        def it_returns_the_right_module_name(self) -> None:
            self.assertEqual(
                ts_cli._filename_to_module_name(r".\test\joker.py"), "test.joker"
            )

    @context.sub_context
    def when_the_platform_looks_like_UNIX(context) -> None:
        @context.before
        def before(self):
            self.mock_callable(os.path, "isfile").for_call(
                "./test/joker.py"
            ).to_return_value(True).and_assert_called()
            self.mock_callable(os.path, "isabs").for_call(
                "./test/joker.py"
            ).to_return_value(False).and_assert_called()
            self.patch_attribute(os.path, "sep", "/")

        @context.example
        def it_returns_the_right_module_name(self) -> None:
            self.assertEqual(
                ts_cli._filename_to_module_name("./test/joker.py"), "test.joker"
            )
