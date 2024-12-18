from mc_token import Token, TokenID

# 우선순위: 숫자가 높을수록 우선순위가 높다.
priority = {
    TokenID.OPEN_PARENTHESIS: 0,
    TokenID.PLUS: 1, 
    TokenID.MINUS: 1, 
    TokenID.MUL: 2, 
    TokenID.DIV: 2,
}

# 중위 표기법 -> 후위 표기법 변환
def infix_to_postfix(tokens: list[Token]):
    stack: list[Token] = []
    queue: list[Token] = []

    for token in tokens:
        token_id = token.get_id()
        if token_id == TokenID.DEC: # 피연산자인 경우 enqueue
            queue.append(token)
        elif (token_id == TokenID.PLUS or # 연산자인 경우
              token_id == TokenID.MINUS or 
              token_id == TokenID.MUL or 
              token_id == TokenID.DIV or
              token_id == TokenID.OPEN_PARENTHESIS or
              token_id == TokenID.CLOSE_PARENTHESIS):
            if len(stack) == 0: # 스택이 비어있는 경우 push
                stack.append(token)
            elif token_id == TokenID.OPEN_PARENTHESIS: # 여는 괄호인 경우 push
                stack.append(token)
            elif token_id == TokenID.CLOSE_PARENTHESIS: # 닫는 괄호인 경우 여는 괄호까지 pop
                while True:
                    popped = stack.pop()
                    if popped.get_id() == TokenID.OPEN_PARENTHESIS:
                        break
                    else:
                        queue.append(popped)
            else:
                # top의 우선순위 이하인 경우 pop -> enqueue
                while stack and priority[stack[-1].get_id()] >= priority[token_id]:
                    queue.append(stack.pop())
                stack.append(token)
    
    for token in stack[::-1]:
        queue.append(token)
    return queue

# 후위계산식 평가
def eval_post(exp: list[Token]):
    stack = []
    for token in exp:
        token_id = token.get_id()
        if token_id == TokenID.DEC: # 피연산자는 push
            stack.append(int(token.get_value()))
        elif token_id == TokenID.PLUS:
            op1, op2 = stack.pop(), stack.pop()
            stack.append(op1 + op2)
        elif token_id == TokenID.MINUS:
            op1, op2 = stack.pop(), stack.pop()
            stack.append(op2 - op1)
        elif token_id == TokenID.MUL:
            op1, op2 = stack.pop(), stack.pop()
            stack.append(op1 * op2)
        elif token_id == TokenID.DIV:
            op1, op2 = stack.pop(), stack.pop()
            stack.append(op2 / op1)
    return stack.pop()
