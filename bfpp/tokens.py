from abc import ABC, abstractmethod


class Context:
    def __init__(self):
        self.locations_with_idxs = {}
        self.current_ptr = 0

    def __str__(self):
        return "Context(locs=" + str(self.locations_with_idxs) + ", ptr=" + str(self.current_ptr) + ")"


class BFPPToken(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def into_bf(self, ctx):
        pass


class BFToken(BFPPToken):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def into_bf(self, ctx):
        if self.token == ">":
            ctx.current_ptr += 1
        elif self.token == "<":
            ctx.current_ptr -= 1

        return self.token

    def __str__(self):
        return self.token

    def __repr__(self):
        return "BFToken('{}')".format(self)


class TokenList(BFPPToken):
    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens

    def into_bf(self, ctx):
        res = ""
        for x in self.tokens:
            res += x.into_bf(ctx)
        return res

    def __str__(self):
        return "(" + "".join(map(str, self.tokens)) + ")"

    def __repr__(self):
        return "TokenList(" + ",".join(map(repr, self.tokens)) + ")"


class BFLoop(BFPPToken):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def into_bf(self, ctx):
        ptr_before = ctx.current_ptr
        inner_bf = self.inner.into_bf(ctx)
        if ctx.current_ptr != ptr_before:
            # Invalidate locations
            ctx.locations_with_idxs = []
        return "[" + inner_bf + "]"

    def __str__(self):
        return "[" + str(self.inner) + "]"

    def __repr__(self):
        return "Loop(" + repr(self.inner) + ")"


class Repetition(BFPPToken):
    def __init__(self, inner, count):
        super().__init__()
        self.inner = inner
        self.count = count

    def __str__(self, ctx):
        return "(" + str(self.inner) + ") * " + str(self.count)

    def __repr__(self):
        return "Repetition(" + repr(self.inner) + ") * " + repr(self.count)

    def into_bf(self, ctx):
        res = ""
        for i in range(self.count):
            res += self.inner.into_bf(ctx)
        return res


class LocDec(BFPPToken):
    def __init__(self, locations, active_idx):
        super().__init__()
        self.locations = locations
        self.active_idx = active_idx

    def __str__(self, ctx):
        return \
            "(?" + \
            " ".join(
                (">" if i == self.active_idx else "") + x for i, x in enumerate(self.locations)
            ) + ")"

    def __repr__(self):
        return \
            "LocDec(" + \
            " ".join(
                (">" if i == self.active_idx else "") + x for i, x in enumerate(self.locations)
            ) + ")"

    def into_bf(self, ctx):
        for i, name in enumerate(self.locations):
            delta_ptr = i - self.active_idx
            ctx.locations_with_idxs[name] = ctx.current_ptr + delta_ptr

        return ""


class LocGoto(BFPPToken):
    def __init__(self, loc):
        super().__init__()
        self.location = loc

    def __str__(self, ctx):
        return "(!" + self.location + ")"

    def __repr__(self):
        return "LocGoto(" + self.location + ")"

    def into_bf(self, ctx):
        if self.location in ctx.locations_with_idxs:
            mem_idx = ctx.locations_with_idxs[self.location]
            delta = mem_idx - ctx.current_ptr
            ctx.current_ptr = mem_idx
            if delta > 0:
                return ">" * delta
            else:
                return "<" * (-delta)
        else:
            raise RuntimeError("Memory location " + self.location + " not found!")

class DeclareMacro(BFPPToken):
    def __init__(self, name, args, content):
        super().__init__()
        self.name = name
        self.args = args
        self.content = content

    def __str__(self, ctx):
        return "define " + self.name + str(self.args) + "{" + str(self.content) + "}"

    def __repr__(self):
        return "Define(name=" + self.name + ",args=" + repr(self.args) + ",content=" + repr(self.content) + ")"

    def into_bf(self, ctx):
        return ""

class InvokeMacro(BFPPToken):
    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args

    def __str__(self, ctx):
        return "invoke " + self.name + "(" + ",".join(self.args) + ")"

    def __repr__(self):
        return "Invoke(name=" + self.name + ",args=(" + ",".join(self.args) + ")"

    def into_bf(self, ctx):
        raise NotImplementedError()

if __name__ == "__main__":
    code = TokenList([
        BFToken("+"),
        BFToken(">"),
        BFToken("+"),
        BFToken("+"),
        BFLoop(BFToken("+")),
        BFToken("+"),
        BFToken("<"),
        BFToken("-"),
        Repetition(BFToken("+"), 10)
    ])

    print(code.into_bf(Centext()))