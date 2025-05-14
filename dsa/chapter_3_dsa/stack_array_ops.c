#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

static int *s;
static int maxSize; // the max size of the stack (when implemented in array) must be predefined 
static int numItems; // current number of items in stack

void STACKinit(int capacity) {
    s = malloc(capacity * sizeof(int));
    if (!s) {
        fprintf(stderr, "Error: malloc failed\n");
        exit(EXIT_FAILURE);
    }
    maxSize  = capacity;
    numItems = 0;
}

int STACKempty() {
    return numItems == 0;
}

int STACKfull() {
    return numItems == maxSize;
}

void STACKpush(int item) {
    if (STACKfull()) {
        fprintf(stderr, "Error: stack is full\n");
        exit(EXIT_FAILURE);
    }
    else {
        s[numItems] = item;
        numItems++;
    }
}

int STACKpop(void) {
    if (STACKempty()) {
        fprintf(stderr, "Error: stack is empty\n");
        exit(EXIT_FAILURE);
    }
    return s[--numItems];
}

int main(void) {
    printf("Running stack ops unit tests...\n");

    STACKinit(3);
    assert(STACKempty());

    // push 3 items
    STACKpush(10);
    STACKpush(20);
    STACKpush(30);
    assert(STACKfull());

    // pop them off in LIFO order
    int v = STACKpop();
    assert(v == 30);
    v = STACKpop();
    assert(v == 20);
    v = STACKpop();
    assert(v == 10);
    assert(STACKempty());

    printf("All stack tests passed!\n");
    return 0;
}