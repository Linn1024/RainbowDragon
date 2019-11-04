#include<stdio.h>

int main(){
	char s;
	float d = 12345;
	scanf("%c:%f", &s, &d);
	printf("%c%%%.2f", s, d);
}