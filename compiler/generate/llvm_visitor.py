from compiler.parse import visitor, expression
from compiler.generate import llvm


class LlvmVisitor(visitor.Visitor):
    def __init__(self, llvm: llvm.Llvm) -> None:
        self.llvm = llvm
        self.out_register = 0

    def visit_call(self, node: expression.Call) -> None:
        # Print the last register... kinda dubious
        if node.id == "print":
            register = self.visit(node.arguments[0]).out_register
            self.llvm.body.append(self.llvm.print_int(register))

    def visit_integer_literal(self, node: expression.IntegerLiteral) -> None:
        self.out_register = self.llvm.reserve_virtual_register()
        self.llvm.body.extend(
            [
                "%{} = alloca i32, align 4".format(self.out_register),
                "store i32 {}, ptr %{}, align 4".format(node.value, self.out_register),
            ]
        )

    def op_name(self, operator: str) -> str:
        match operator:
            case "+":
                return "add"
            case "-":
                return "sub"
            case "*":
                return "mul"
            case "/":
                return "udiv"
        raise ValueError("Unrecognized operator {}".format(operator))

    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        left_register = self.execute(node.left).out_register
        right_register = self.execute(node.right).out_register

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
                    self.op_name(node.operator),
                    "nsw " if node.operator != "/" else "",
                    temp_left_register,
                    temp_right_register,
                ),
                "%{} = alloca i32, align 4".format(self.out_register),
                "store i32 %{}, ptr %{}, align 4".format(
                    op_register, self.out_register
                ),
            ]
        )
