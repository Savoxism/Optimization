#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_SIZE 100

typedef struct {
    double items[MAX_SIZE];
    int top;
} NumberStack;

typedef struct {
    char items[MAX_SIZE];
    int top;
} OperatorStack;

void initNumberStack(NumberStack *s) {
    s->top = -1;
}

void pushNumber(NumberStack* s, double value) {
    if (s->top < MAX_SIZE - 1) {
        s->items[++(s->top)] = value;
    }
}

double popNumber(NumberStack *s) {
    if (s->top >= 0) {
        return s->items[(s->top)--];
    }
    return 0;
}

// Stack operations for operator stack
void initOperatorStack(OperatorStack *s) {
    s->top = -1;
}

void pushOperator(OperatorStack *s, char op) {
    if (s->top < MAX_SIZE - 1) {
        s->items[++(s->top)] = op;
    }
}

char popOperator(OperatorStack *s) {
    if (s->top >= 0) {
        return s->items[(s->top)--];
    }
    return '\0';
}

int getPriority(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        case '^':
            return 3;
    }
    return 0;
}

double processOperation(double a, double b, char op) {
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
        case '^': {
            double result = 1;
            for (int i = 0; i < b; i++) {
                result *= a;
            }
            return result;
        }
    }
    return 0;
}

void processOperations(NumberStack *numbers, OperatorStack *operators, char nextOp) {
    while (operators->top >= 0 && 
           (nextOp == '\0' || getPriority(operators->items[operators->top]) >= getPriority(nextOp))) {
        char op = popOperator(operators);
        double b = popNumber(numbers);
        double a = popNumber(numbers);
        pushNumber(numbers, processOperation(a, b, op));
    }
}

double evaluateExpression(const char *expr) {
    NumberStack numbers;
    OperatorStack operators;
    initNumberStack(&numbers);
    initOperatorStack(&operators);
    
    int i = 0;
    while (expr[i] != '\0') {
        if (isspace(expr[i])) {
            i++;
            continue;
        }
        
        if (isdigit(expr[i])) {
            double value = 0;
            while (isdigit(expr[i])) {
                value = value * 10 + (expr[i] - '0');
                i++;
            }
            pushNumber(&numbers, value);
            continue;
        }
        
        if (strchr("+-*/^", expr[i])) {
            processOperations(&numbers, &operators, expr[i]);
            pushOperator(&operators, expr[i]);
            i++;
            continue;
        }
        
        if (expr[i] == '(') {
            pushOperator(&operators, expr[i]);
            i++;
            continue;
        }

        if (expr[i] == ')') {
            while (operators.top >= 0 && operators.items[operators.top] != '(') {
                processOperations(&numbers, &operators, '\0');
            }
            popOperator(&operators); // Remove '('
            i++;
            continue;
        }
    }
    processOperations(&numbers, &operators, '\0');
    return popNumber(&numbers);
}

int main() {
    char expr[MAX_SIZE];
    printf("Enter an arithmetic expression: ");
    fgets(expr, MAX_SIZE, stdin);
    expr[strcspn(expr, "\n")] = 0;
    
    double result = evaluateExpression(expr);
    printf("Result: %.2f\n", result);
    
    return 0;
}