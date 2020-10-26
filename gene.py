import random


class TreeNode:
    left = None
    right = None

    def __init__(self, value: str):
        self.value = value


class Gene:
    def __init__(self, head_len, FUNCTION_A1, FUNCTION_A2, TERMINAL):
        self.head_len = head_len
        self.gene = None
        self.root = None
        self.expression = None

        self.FUNCTION_A1 = FUNCTION_A1
        self.FUNCTION_A2 = FUNCTION_A2
        self.TERMINAL = TERMINAL

    def random_init(self):
        gene = []
        FUNCTION = self.FUNCTION_A1 + self.FUNCTION_A2
        TERMINAL = self.TERMINAL
        flag = random.randint(0, 1)
        for _ in range(self.head_len):
            if flag == 1:
                i = random.randint(0, len(FUNCTION) - 1)
                gene.append(FUNCTION[i])
            else:
                i = random.randint(0, len(TERMINAL) - 1)
                gene.append(TERMINAL[i])
        for _ in range(self.head_len + 1):
            i = random.randint(0, len(TERMINAL) - 1)
            gene.append(TERMINAL[i])
        self.gene = gene

    def construct(self):
        v = self.gene.copy()
        q = []
        root = TreeNode(v.pop(0))
        q.append(root)

        while len(q) != 0:
            node = q.pop(0)

            if node.value in self.FUNCTION_A1:
                # function nodes with arity 1 only have left child node
                left = TreeNode(v.pop(0))
                node.left = left
                q.append(left)

            elif node.value in self.FUNCTION_A2:
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

    def evaluate(self):
        return eval(self.expression)


if __name__ == "__main__":
    FUNCTION_A1 = ["np.sin({})", "np.cos({})", "np.exp({})", "np.log(abs({}))"]
    FUNCTION_A2 = ["{} + {}", "{} - {}", "{} * {}", "{} / {} ", "G1({}, {})", "G2({}, {})"]
    TERMINAL = ["np.e", "np.pi", "a", "b"]

    a = Gene(3, FUNCTION_A1, FUNCTION_A2, TERMINAL)
    a.random_init()
    print(a.gene)
    print(a.compile())
