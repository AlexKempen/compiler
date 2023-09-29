from compiler.parse import node, visitor
from compiler.generate import llvm


class LlvmVisitor(visitor.Visitor):
    def __init__(self, llvm: llvm.Llvm) -> None:
        self.llvm = llvm
        self.out_register = 0

    def visit_integer_node(self, node: node.IntegerNode) -> None:
        self.out_register = self.llvm.reserve_virtual_register()
        self.llvm.body.extend(
            [
                "%{} = alloca i32, align 4".format(self.out_register),
                "store i32 {}, ptr %{}, align 4".format(node.value, self.out_register),
            ]
        )

    def visit_op_helper(
        self, node: node.BinaryOperation, op_name: str, nsw: bool = True
    ) -> None:
        left_register = self.visit(node.left).out_register
        right_register = self.visit(node.right).out_register

        temp_left_register = self.llvm.reserve_virtual_register()
        temp_right_register = self.llvm.reserve_virtual_register()
        op_register = self.llvm.reserve_virtual_register()
        self.out_register = self.llvm.reserve_virtual_register()

        self.llvm.body.extend(
            [
                "%{} = load i32, ptr %{}, align 4".format(
                    temp_left_register, left_register
                ),
                "%{} = load i32, ptr %{}, align 4".format(
                    temp_right_register, right_register
                ),
                "%{} = {} {}i32 %{}, %{}".format(
                    op_register,
                    op_name,
                    "nsw " if nsw else "",
                    temp_left_register,
                    temp_right_register,
                ),
                "%{} = alloca i32, align 4".format(self.out_register),
                "store i32 %{}, ptr %{}, align 4".format(
                    op_register, self.out_register
                ),
            ]
        )

    def visit_add(self, node: node.Add) -> None:
        self.visit_op_helper(node, "add")

    def visit_subtract(self, node: node.Subtract) -> None:
        self.visit_op_helper(node, "sub")

    def visit_multiply(self, node: node.Multiply) -> None:
        self.visit_op_helper(node, "mul")

    def visit_divide(self, node: node.Divide) -> None:
        self.visit_op_helper(node, "udiv", False)
