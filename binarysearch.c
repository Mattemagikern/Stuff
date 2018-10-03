#define NULL 0
struct tree {
    int x;
    struct tree *l;
    struct tree *r;
};

int rec(struct tree *T, int value)
{
    if (T == NULL)
        return 0;

    if (T->x > value)
        return 1;

    if (value == T->x)
        return 1 + rec(T->r, value) + rec(T->l, value);

    return rec(T->r, value) + rec(T->l, value);
}

int solution(struct tree *T)
{
    if (T == NULL)
        return 0;

    return 1 + rec(T->r, T->x) + rec(T->l, T->x);
}


int main(int argc, char const *argv[])
{
    struct tree T = {
        .x = 5,
        .l = &((struct tree)
        {
            .x = 3,
            .l = &((struct tree) {
                .x = 6,
                .l = NULL,
                .r = NULL,
            }),
            .r = NULL
        }),
        .r = &((struct tree)
        {
            .x = 4,
            .l = NULL,
            .r = NULL,
        }),
    };
    printf("%d\n", solution(&T));
    return 0;
}
