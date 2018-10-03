//after winter comes summer,
//Find the shortest winter,
//Def winter: all subsecuently numbers are higher than this number.
unsigned indx;
unsigned i;
int solution(int T[], int N)
{
    unsigned walker = N;

    while (walker--) {
    int max = T[0], min = T[N-1];
        for (i = walker; i < N; i++){
            if (min > T[i]){
                min = T[i];
            }
        }

        for (i = 0; i < walker; i++){
            if (T[i] > max){
                max = T[i];
            }
        }

        if (!(min < max))
            indx = walker;
    }

    return indx;
}

int main(int argc, char const *argv[])
{
   int T[7] = {-5, -5, -5, -42, 6, 6,-42, 12};
    printf("sol: %d\n", solution(T, 8));
    return 0;
}
