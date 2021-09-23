#include <stdio.h>

int flush_buf() {
    return fflush(stdout);
}