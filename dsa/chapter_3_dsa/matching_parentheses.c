#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100

typedef struct {
    char items[MAX_SIZE];
    int top;
} Stack;

void initStack(Stack *s) {
    s->top = -1;
}

int isEmpty(Stack *s) {
    return s->top == -1;
}

int isFull(Stack *s) {
    return s->top == MAX_SIZE - 1;
}

void push(Stack *s, char c) {
    if (!isFull(s)) {
        s->items[++(s->top)] = c;
    }
}

char pop(Stack *s) {
    if (!isEmpty(s)) {
        return s->items[(s->top)--];
    }
    return '\0';
}

int parenthesesMatched(char *expr) {
    Stack s;
    initStack(&s);

    for (int i = 0; expr[i] != '\0'; i++) {
        if (expr[i] == '(' || expr[i] == '[' || expr[i] == '{') {
            push(&s, expr[i]);
            continue;
        }

        if (expr[i] == ')' || expr[i] == ']' || expr[i] == '}') {
            if (isEmpty(&s)) {
                return 0;
            }
                char top = pop(&s);
                if ((expr[i] == ')' && top != '(') ||
                (expr[i] == ']' && top != '[') ||
                (expr[i] == '}' && top != '{')) {
                return 0;  // Mismatched brackets
            }
        }
    }
    return isEmpty(&s);
}

int main() {
    char expr[MAX_SIZE];
    printf("Enter an expression with parentheses: ");
    fgets(expr, MAX_SIZE, stdin);
    expr[strcspn(expr, "\n")] = 0;  // Remove trailing newline
    
    if (areParenthesesMatched(expr)) {
        printf("Parentheses are balanced\n");
    } else {
        printf("Parentheses are not balanced\n");
    }
    
    return 0;
}
