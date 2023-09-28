from __future__ import annotations

from compiler.parse import node
from compiler.utils import str_utils


def generate(file_name: str, node: node.Node) -> str:
    return Llvm(file_name, node).generate()


class Llvm:
    def __init__(self, file_name: str, node: node.Node) -> None:
        self.file_name = file_name
        self.node = node

        self.virtual_register_number = 0
        self.free_register_count = 0
        self.loaded_registers = []

        self.constants: list[str] = []
        self.attr_index = 0
        self.attributes: list[Attribute] = []
        self.declarations: list[str] = []

    def add_attribute(self, attribute: Attribute) -> int:
        attribute.set_index(self.attr_index)
        self.attributes.append(attribute)

        index = self.attr_index
        self.attr_index += 1
        return index

    def generate(self) -> str:
        body = self.body()
        return "\n".join(
            [
                self.preamble(),
                self.make_constants(),
                self.main(body),
                self.make_declarations(),
                self.make_attributes(),
                self.postamble(),
            ]
        )

    def preamble(self) -> str:
        """Generates the preamble of the LLVM program"""
        return str_utils.end_join(
            "; ModuleID = '{}'".format(self.file_name),
            'source_filename = "{}"'.format(self.file_name),
            'target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"',
            'target triple = "x86_64-pc-linux-gnu"',
        )

    def make_constants(self) -> str:
        return str_utils.end_join(*self.constants)

    def main(self, body: str, add_return: bool = True) -> str:
        """Generates code for the main function.

        Args:
            body: The body of the function.
            add_return: Whether to append a return statement to body.
        """
        if add_return:
            body = body + "ret i32 0"

        args = ["noinline", "nounwind", "optnone", "uwtable"]
        index = self.add_attribute(Attribute(args, {"min-legal-vector-width": "0"}))

        return str_utils.end_join(
            "; Function Attrs: {}".format(" ".join(args)),
            "define dso_local i32 @main() #{} {{".format(index),
            str_utils.indent(body),
            "}",
        )

    def make_attributes(self) -> str:
        return str_utils.end_join(*(str(attr) for attr in self.attributes))

    def make_declarations(self) -> str:
        return str_utils.end_join(*self.declarations)

    def postamble(self) -> str:
        """Generates the postamble of the LLVM program"""
        return str_utils.end_join(
            "!llvm.module.flags = !{!0, !1, !2, !3, !4}",
            "!llvm.ident = !{!5}\n",
            '!0 = !{i32 1, !"wchar_size", i32 4}',
            '!1 = !{i32 7, !"PIC Level", i32 2}',
            '!2 = !{i32 7, !"PIE Level", i32 2}',
            '!3 = !{i32 7, !"uwtable", i32 1}',
            '!4 = !{i32 7, !"frame-pointer", i32 2}',
            '!5 = !{!"Ubuntu clang version 10.0.0-4ubuntu1"}',
        )

    def print_int(self, register: int) -> str:
        index = self.add_attribute(Attribute())

        self.constants.append(
            '@.str = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1',
        )

        self.declarations.append(
            "declare i32 @printf(ptr noundef, ...) #{}".format(index)
        )

        return "%{} = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef 6)".format(
            register
        )

    def body(self) -> str:
        return (
            "%1 = alloca i32, align 4\nstore i32 0, ptr %1, align 4" + self.print_int(2)
        )


class Attribute:
    DEFAULT_PAIRS = {
        "stack-protector-buffer-size": "8",
        "frame-pointer": "all",
        "no-trapping-math": "true",
        "target-cpu": "x86-64",
        "target-features": "+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87",
        "tune-cpu": "generic",
    }

    def __init__(
        self,
        args: list[str] = [],
        pairs: dict[str, str] = {},
        add_default_pairs: bool = True,
    ) -> None:
        self.index = None
        self.args = args
        self.pairs = pairs
        if add_default_pairs:
            self.pairs.update(Attribute.DEFAULT_PAIRS)

    def set_index(self, index: int) -> None:
        self.index = index

    def attr_dict(self) -> str:
        result = " ".join(self.args)
        for key, value in self.pairs.items():
            result += ' "{}"="{}"'.format(key, str(value))
        return "{{{} }}".format(result)

    def __str__(self) -> str:
        if self.index is None:
            raise ValueError("Attribute index was not set.")
        return "attributes #{} = {}".format(self.index, self.attr_dict())
