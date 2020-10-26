import random

FUNCTION_A1 = ["np.sin({})", "np.cos({})", "np.exp({})", "np.log(abs({}))"]
FUNCTION_A2 = ["({} + {})", "({} - {})", "({} * {})", "({} / np.sqrt(1 + {}**2))"]
ADF = ["G1({}, {})", "G2({}, {})"]  # only in main head
TERMINAL = ["np.e", "np.pi"]
INPUT_ARGUMENT = ["a", "b"]  # only in adf


class TreeNode:
    left = None
    right = None

    def __init__(self, value: str):
        self.value = value


class Gene:
    def __init__(self, head_len, var_num=0, is_adf=False):
        self.head_len = head_len
        self.var_num = var_num
        self.is_adf = is_adf

        self.gene = None
        self.root = None
        self.expression = None

    def random_init(self):
        gene = []
        FUNCTION = FUNCTION_A1 + FUNCTION_A2
        if self.is_adf:
            for _ in range(self.head_len):  # init head
                element_type = random.randint(0, 1)
                if element_type == 0:  # function
                    i = random.randint(0, len(FUNCTION) - 1)
                    gene.append(FUNCTION[i])
                elif element_type == 1:  # input argument
                    i = random.randint(0, len(INPUT_ARGUMENT) - 1)
                    gene.append(INPUT_ARGUMENT[i])
            for _ in range(self.head_len + 1):  # init tail
                i = random.randint(0, len(INPUT_ARGUMENT) - 1)
                gene.append(INPUT_ARGUMENT[i])
        else:
            for _ in range(self.head_len):  # init head
                element_type = random.randint(0, 2)
                if element_type == 0:  # function
                    i = random.randint(0, len(FUNCTION) - 1)
                    gene.append(FUNCTION[i])
                elif element_type == 1:  # terminal
                    i = random.randint(0, len(TERMINAL) - 1 + self.var_num)
                    if i < len(TERMINAL):
                        gene.append(TERMINAL[i])
                    else:
                        gene.append(f"inputs[{i - len(TERMINAL)}]")
                elif element_type == 2:  # adf
                    i = random.randint(0, len(ADF) - 1)
                    gene.append(ADF[i])
            for _ in range(self.head_len + 1):  # init tail
                i = random.randint(0, len(TERMINAL) - 1 + self.var_num)
                if i < len(TERMINAL):
                    gene.append(TERMINAL[i])
                else:
                    gene.append(f"inputs[{i - len(TERMINAL)}]")
        self.gene = gene

    def construct(self):
        v = self.gene.copy()
        q = []
        root = TreeNode(v.pop(0))
        q.append(root)

        while len(q) != 0:
            node = q.pop(0)

            if node.value in FUNCTION_A1:
                # function nodes with arity 1 only have left child node
                left = TreeNode(v.pop(0))
                node.left = left
                q.append(left)

            elif node.value in FUNCTION_A2 or node.value in ADF:
                # function nodes with arity 2 have left and right child node
                left = TreeNode(v.pop(0))
                right = TreeNode(v.pop(0))
                node.left = left
                node.right = right
                q.append(left)
                q.append(right)

        self.root = root

    def __compile_helper(self, root: TreeNode):
        if root.left and root.right:
            l = self.__compile_helper(root.left)
            r = self.__compile_helper(root.right)
            return root.value.format(l, r)
        elif root.left and not root.right:
            child = self.__compile_helper(root.left)
            return root.value.format(child)
        else:
            return root.value

    def compile(self):
        if not self.root:
            self.construct()
        self.expression = self.__compile_helper(self.root)
        return self.expression


if __name__ == "__main__":
    a = Gene(3, var_num=3, is_adf=False)
    a.random_init()
    print(a.gene)
    print(a.compile())
