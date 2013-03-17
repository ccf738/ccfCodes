import java.util.Scanner;

public class ccf{
 public static int yunsuanjibie(String expression) {
  int r = 0;
  int NumberOfOperators = 0;
  for (int i = 0; i < expression.length(); i++) {
   if (expression.charAt(i) == '+' || expression.charAt(i) == '-' || expression.charAt(i) == '*'
     || expression.charAt(i) == '/') {
	   NumberOfOperators++;
   }
  }
  
  //to get all the factors
  String characters[] = new String[2 * NumberOfOperators + 1];
  int NumberOffactors = 0;
  int BeginOfFactors = 0;
  for (int i = 0; i < expression.length(); i++) {
   if (expression.charAt(i) == '+' || expression.charAt(i) == '-' || expression.charAt(i) == '*'
     || expression.charAt(i) == '/') {
	   characters[NumberOffactors] = expression.substring(BeginOfFactors, i);
	   NumberOffactors++;
    characters[NumberOffactors] = "" + expression.charAt(i);
    NumberOffactors++;
    BeginOfFactors = i + 1;
   }
  }
  //the last factor
  characters[NumberOffactors] = expression.substring(BeginOfFactors, expression.length());
  int kp = NumberOfOperators;
  while (kp > 0) {
   for (int i = 0; i < characters.length; i++) {
    if (characters[i].equals("*") || characters[i].equals("/")) {
     int l;
     for (l = i - 1; l > -1; l--) {
      if (!(characters[l].equals("p")))
       break;
     }
     int q;
     for (q = i + 1; q < characters.length; q++) {
      if (!(characters[l].equals("p")))
       break;
     }
     if (characters[i].equals("*")) {
    	 characters[i] = ""
        + (Integer.parseInt(characters[l]) * Integer
          .parseInt(characters[q]));
    	 characters[l] = "p";
    	 characters[q] = "p";
      kp--;
     } else {
    	 characters[i] = ""
        + (Integer.parseInt(characters[l]) / Integer
          .parseInt(characters[q]));
    	 characters[l] = "p";
    	 characters[q] = "p";
      kp--;
     }
     break;
    }
   }
   for (int i = 0; i < 2 * NumberOfOperators + 1; i++) {
    if (characters[i].equals("+") || characters[i].equals("-")) {
     int l;
     for (l = i - 1; l > -1; l--) {
      if (!(characters[l].equals("p")))
       break;
     }
     int q;
     for (q = i + 1; q < characters.length; q++) {
      if (!(characters[q].equals("p")))
       break;
     }
     if (characters[i].equals("+")) {
    	 characters[i] = ""
        + (Integer.parseInt(characters[l]) + Integer
          .parseInt(characters[q]));
    	 characters[l] = "p";
    	 characters[q] = "p";
      kp--;
     } else {
    	 characters[i] = ""
        + (Integer.parseInt(characters[l]) - Integer
          .parseInt(characters[q]));
    	 characters[l] = "p";
    	 characters[q] = "p";
      kp--;
     }
     break;
    }
   }
   for (int i = 0; i < characters.length; i++) {
    if (!(characters[i].equals("p"))) {
     r = Integer.parseInt(characters[i]);
     break;
    }
   }
  }
  System.out.println("r----------------" + r);
  return r;
 }

 public static void sizeyunsuan(String s) {
  while (true) {
   int first = 0;
   int last = 0;
   for (int i = 0; i < s.length(); i++) {
    if (s.charAt(i) == '(')
     first = i;
    if (s.charAt(i) == ')') {
     last = i;
     break;
    }
   }
   if (last == 0) {
    System.out.println(yunsuanjibie(s));
    return;
   } else {
    String s1 = s.substring(0, first);
    String s2 = s.substring(first + 1, last);
    String s3 = s.substring(last + 1, s.length());
    s = s1 + yunsuanjibie(s2) + s3;
   }
  }
 }

 public static void main(String[] args) {
                  String s=(new Scanner(System.in)).next();
  sizeyunsuan(s);
 }
}

