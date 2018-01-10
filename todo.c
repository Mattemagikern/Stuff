#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define SIZE 5000
#define ADD 100
#define DEL 308
#define REMOVE_ALL 692

int i;
size_t len = 0;
char c;
size_t priority = 0;
FILE* fp;
const char* path = "/home/mattemagikern/.ToDo";
char* line = NULL;
ssize_t read;

int hash(const char* word ){
  int code = 0;
  int n = 0;
  for (int i = 0; word[i] != '\0'; i++) {
    if (isalpha(word[i]))
      n = word[i] - 'a' + 1;
    else
      n = 27;

    code = ((code << 3) + n) % SIZE;
  }
  return code;
}

void list() {
  fp = fopen(path, "r");
  if (fp == NULL) {
    printf("Error reading to file.\n");
    exit(1);
  }
  while ((read = getline(&line, &len, fp)) != EOF)
    printf("%s", line);

  free(line);
  fclose(fp);
}

void add(const char* task, int priority){
  fp = fopen(path, "a");
  if (fp == NULL) {
    printf("Error appending to file\n");
    exit(1);
  }
  fprintf(fp, "%c %s\n", priority+'0', task);
  fclose(fp);
}

void remove_item(char* task){
  fp = fopen(path, "r");
  if (fp == NULL) {
    printf("Error removing line in file.\n");
    exit(1);
  }
  fclose(fp);
}

void remove_all(){
  remove(path);
}

int main(int argc, char const* argv[])
{
  if (argc == 1) {
    list();
  }else{
    switch (hash(argv[1])) {
      case ADD:
        if (argc > 3) {
          priority = atoi(argv[3]);  
        }
        add(argv[2], priority);
        break;
      case DEL:
        if (argc > 3) {
          remove_item(argv[2]);
        }
        break;
      case REMOVE_ALL:
        remove_all();
        break;
    }
  }
  return 0;
}
