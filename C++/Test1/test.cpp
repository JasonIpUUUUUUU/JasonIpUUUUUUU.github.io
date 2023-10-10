#include <string>
#include <iostream>
#include <bitset>
#include <vector>

using namespace std;

char alphabet[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};

vector<string> dancingBacon(string cText){
    int index = 0;
    char *ptr = alphabet;
    string element = "";
    vector<string> outputs, binaryCodes;
    for(char c : cText){
        if(c != ' '){
        int character = int(toupper(c)) - 65;
        bitset<6> binaryRepresentation(character);
        binaryCodes.push_back(binaryRepresentation.to_string());
        }
    }
    for(string binary: binaryCodes){
            for(char bit: binary){
                if(bit == '0'){
                    index--;
                }
                else{
                    index++;
                }
                if(index < 0){
                    index = 25;
                }
                else if(index > 25){
                    index = 0;
                }
                element += alphabet[index];
            }
            outputs.push_back(element);
            element = "";
    }
    return outputs;
}

int main(){
    vector<string> thing = dancingBacon("This is a test");
    for(string element : thing){
        cout << element;
    }
    return 0;
}