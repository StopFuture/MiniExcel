from __future__ import division
from functools import total_ordering


class OperatorBase(object):
    def __init__(self, token, precedence, operands=2, associativity='left'):

        self.token = token
        self.precedence = precedence
        self.operands = operands
        self.associativy = associativity

    def is_unary(self):
        return self.operands == 1

    def is_binary(self):
        return self.operands == 2

    def is_left_assoc(self):
        return self.associativy == 'left'

    def is_right_assoc(self):
        return self.associativy == 'right'

    def eval(self, *args):
        assert len(args) == self.operands, "Bad number of operands for operator %s: expected %d, got %d" % (
            self, self.operands, len(args))
        return self.do_eval(*args)

    def __eq__(self, other):
        if other is None:
            return False
        return self.precedence == other.precedence

    def __ne__(self, other):  # for python2 compatibility
        return not self == other

    def __lt__(self, other):
        if other is None:  # None act as "sentinel"
            return False
        if self.is_unary():
            return other.precedence >= self.precedence
        # from here, self is binary
        if other.is_binary():
            if other.precedence > self.precedence:
                return True
            if other.precedence == self.precedence and other.is_left_assoc():
                return True
            return False
        if other.is_unary():
            return True

    def do_eval(self, *args):
        raise NotImplementedError()


class Plus(OperatorBase):

    def __init__(self):
        super(Plus, self).__init__('+', 3)

    def do_eval(self, *args):
        return args[0] + args[1]


class Minus(OperatorBase):


    def __init__(self):
        super(Minus, self).__init__('-', 3)

    def do_eval(self, *args):
        return args[0] - args[1]


class Multiply(OperatorBase):

    def __init__(self):
        super(Multiply, self).__init__('*', 5)

    def do_eval(self, *args):
        return args[0] * args[1]


class Divide(OperatorBase):

    def __init__(self):
        super(Divide, self).__init__('/', 5)

    def do_eval(self, *args):
        return args[0] / args[1] if args[1] != 0 else float("Inf")


class Pow(OperatorBase):
    def __init__(self):
        super(Pow, self).__init__('^', 6, associativity='right')

    def do_eval(self, *args):
        return args[0] ** args[1]


class UnaryMinus(OperatorBase):

    def __init__(self):
        super(UnaryMinus, self).__init__('-', 4, operands=1)

    def do_eval(self, *args):
        return args[0] * (-1)



OPERATORS = [
    Plus(), Minus(), Multiply(), Divide(), UnaryMinus(), Pow()
]

BINARY_OPS = {op.token: op for op in OPERATORS if op.is_binary()}
UNARY_OPS = {op.token: op for op in OPERATORS if op.is_unary()}


VALID_TOKENS_SET = {op.token for op in OPERATORS}
VALID_TOKENS_SET.add('(')
VALID_TOKENS_SET.add(')')


class InvalidTokenError(Exception):
    pass


class MalformedExpressionError(Exception):
    pass


def remove_quotes(expr):
    return expr.replace('\'', '').replace('\"', '')


def tokenize(expr):
    if not expr:
        return []
    result_list = []
    start = 0
    for index, char in enumerate(expr):
        if char in VALID_TOKENS_SET:
            curr_token = (expr[start:index]).strip()
            if len(curr_token) > 0:
                result_list.extend(curr_token.split())

            result_list.append(char)
            start = index + 1
    if start == 0:
        return expr.split()
    remainder_token = (expr[start:index + 1]).strip()
    if len(remainder_token) > 0:
        result_list.extend(remainder_token.split())
    return result_list


def is_value(token):

    if token is None:
        return False
    try:
        float(token)
        return True
    except ValueError:
        return False


def validate_token(token):

    if is_value(token) or token in VALID_TOKENS_SET:
        return token
    raise InvalidTokenError(token)


class EvaluatorBase(object):
    def __init__(self, tokexpr):
        assert tokexpr is not None, "Expression to recognize cannot be None, should at least be []"
        self.tokens = tokexpr
        self.cursor = 0

    def _next(self):

        if self.cursor < len(self.tokens):
            return self.tokens[self.cursor]
        return None  # all tokens consumed

    def _consume(self):

        self.cursor += 1  # move cursor up

    def _error(self, msg=None):

        raise MalformedExpressionError(msg)

    def _expect(self, token):
        try:
            assert self._next() == token
            self._consume()
        except AssertionError:
            self._error("Expected %s, got %s" % (token, self._next()))

    @staticmethod
    def _binary(token):

        return BINARY_OPS.get(token)

    @staticmethod
    def _unary(token):

        return UNARY_OPS.get(token)

    def _eval_leaf(self, token):

        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                self._error("'%s' cannot be cast to a number" % token)

    def _eval_node(self, operator, *args):

        return operator.eval(*args)

    def evaluate(self):

        raise NotImplementedError()

def eval_dec_inc(value):
    for _ in range(10):
        st = set(list(value))
        if len(value) > 1 :

            dec = value.find("dec")
            if dec != -1:
                dec_st = dec + 4
                dec_fn = -1
                for i in range(dec_st, len(value)):
                    if value[i] == ")":
                        dec_fn = i
                        break
                value = value[:dec] + "(" + value[dec_st:dec_fn] + "-1)" + value[dec_fn + 1:]
            inc = value.find("inc")
            if inc != -1:
                inc_st = inc + 4
                inc_fn = -1
                for i in range(inc_st, len(value)):
                    if value[i] == ")":
                        inc_fn = i
                        break
                value = value[:inc] + "(" + value[inc_st:inc_fn] + "+1)" + value[inc_fn + 1:]
        value = "".join(value)

    return value

class ShuntingYardEvaluator(EvaluatorBase):
    def evaluate(self):
        operators = []
        operands = []
        operators.append(None)
        self._e(operators, operands)
        self._expect(None)
        return operands[-1]

    def _e(self, operators, operands):
        self._p(operators, operands)
        while self._next() in BINARY_OPS:
            self._pushoperator(self._binary(self._next()), operators, operands)
            self._consume()
            self._p(operators, operands)
        # remaining operators are ordered by precedence desc : pop it all taking operands in operands stack :
        while operators[-1] is not None:
            self._popoperator(operators, operands)

    def _p(self, operators, operands):
        if self._next() and self._next() not in VALID_TOKENS_SET:
            operands.append(self._eval_leaf(self._next()))
            self._consume()
        elif self._next() == '(':
            self._consume()
            operators.append(None)
            self._e(operators, operands)
            self._expect(')')
            operators.pop()
        elif self._next() in UNARY_OPS:
            self._pushoperator(self._unary(self._next()), operators, operands)
            self._consume()
            self._p(operators, operands)
        else:
            self._error()

    def _popoperator(self, operators, operands):
        if operators[-1] is not None and operators[-1].is_binary():
            second = operands.pop()
            first = operands.pop()
            operands.append(self._eval_node(operators.pop(), first, second))
        else:  # unary
            operands.append(self._eval_node(operators.pop(), operands.pop()))

    def _pushoperator(self, op, operators, operands):
        while operators[-1] > op:
            self._popoperator(operators, operands)
        operators.append(op)


class PrecedenceClimbingEvaluator(EvaluatorBase):


    def evaluate(self):
        val = self._exp(0)
        self._expect(None)
        return val

    def _exp(self, precedence):
        t = self._p()
        while self._next() in BINARY_OPS and EvaluatorBase._binary(self._next()).precedence >= precedence:
            op = EvaluatorBase._binary(self._next())
            self._consume()
            if op.is_right_assoc():
                q = op.precedence
            else:
                q = op.precedence + 1
            t1 = self._exp(q)
            t = self._eval_node(op, t, t1)
        return t

    def _p(self):
        if self._next() in UNARY_OPS:
            op = EvaluatorBase._unary(self._next())
            self._consume()
            q = op.precedence
            t = self._exp(q)
            return self._eval_node(op, t)
        elif self._next() == '(':
            self._consume()
            t = self._exp(0)
            self._expect(')')
            return t
        elif self._next() and self._next() not in VALID_TOKENS_SET:
            t = self._eval_leaf(self._next())
            self._consume()
            return t
        else:
            self._error()


def calc(expr, evaluator_class=PrecedenceClimbingEvaluator):
    tokens = tokenize(remove_quotes(expr))
    for t in tokens:
        validate_token(t)
    return evaluator_class(tokens).evaluate()
