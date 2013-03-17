package sorts;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class Eightsorts {
	private double a[];
	
	public Eightsorts () {
		
	}
	
	public Eightsorts (double array[]) {
		setA(array);
	}
	
	public double[] Bubblesort (double array[]) {
		for (int i = 1; i < array.length - 1; i++) {
			for (int j = 0; j < array.length - i; j++) {
				if(array[j] > array[j+1]){
					double temp = array[j];
					array[j] = array[j+1];
					array[j+1] = temp;
				}
			}
		}
		return array;
	}
	
	public double[] Directorysort(double[] array) {
		for (int i = 1; i < array.length; i++) {
			for (int j = 0; j <= i; j++) {
				if (array[i] < array[j]) {
					double temp = array[i];
					array[i] = array[j];
					array[j] = temp;
				}
				
			}
		}
		return array;
	}
	
	public double[] Shellsort(double[] array) {
		int gap = array.length / 2;
		System.out.println(array.length);
		while (gap > 0) {
			System.out.println(gap);
			for (int i = 0; i < array.length - gap; i++) {
				if (array[i] > array[i + gap]) {
					double temp = array[i];
					array[i] = array[i + gap];
					array[i + gap] = temp;
				}
			}
		gap = gap / 2;
		}
		return array;
		
	}
	
	public double[] SimpleSelectSort(double array[]) {
		for (int i = 0; i < array.length; i++) {
			double min = array[i];
			int index = i;
			for (int j = i; j < array.length; j++) {
				if (array[j] < min) {
					min = array[j];
					index = j;
					System.out.println(min);
				}
			}
			double temp = array[index];
			array[index] = array[i];
			array[i] = temp;
				
			}
		return array;
	}
	public double[] HeapSort(double array[]) {
		for (int child = 1; child < array.length; child++) {
			int parent = (child - 1) / 2;
			while (parent >= 0 && array[parent] < array[child]) {
				double temp = array[parent];
				array[parent] = array[child];
				array[child] = temp;
				child = parent;
				parent = (child - 1) / 2;
			}
			
			}
		for (int i = array.length - 1; i >= 0; i--) {
			double temp = array[i];
			array[i] = array[0];
			array[0] = temp;
			int parent = 0;
			while (true)  
            {  
                int leftChild = 2 * parent + 1;  
                if (leftChild >= i)  
                    break;
                int rightChild = leftChild + 1;  
                int maxChild = leftChild;  
                if (rightChild < i && array[leftChild] < array[rightChild])  
                    maxChild = rightChild;  
                if (array[parent] < array[maxChild])  
                {  
                   double tem = array[parent];
                   array[parent] = array[maxChild];
                   array[maxChild] = tem;
                   parent = maxChild;
                }  
                else  
                    break;
            }  
        }  
		return array;
	}
	
	public void QuickSort(double[] array,int low,int high) {
		int index = 0;
		if (low < high) {
			index = ForQuickSort(array, low, high);
			QuickSort(array, low, index - 1);
			QuickSort(array, index + 1, high);
		}
	}
	public int ForQuickSort(double[] array,int low,int high) {
		double pivot = array[low];
		while (low < high) {
			while (low < high && array[high] >= pivot) {
				high--;
			}
			array[low] = array[high];
			while (low < high && array[low] <= pivot) {
				low++;
			}
			array[high] = array[low];
		array[low] = pivot;
		}
		return low;
	}
	
	public double[] InsertSort(double[] array) {
		for (int i = 0; i < array.length - 1; i++) {
			int length = i + 1;
			while (length > 0 && array[length] < array[i]) {
				double temp = array[length];
				array[length] = array[i];
				array[i] = temp;
				length--;
				i--;
			}
		}
		return array;
	}
	
	public String FindSum(double[] array,double sum) {
		QuickSort(array, 0, array.length - 1);
		int begin = 0;
		int end = array.length - 1;
		while (begin < end) {
			if(array[begin] + array[end] > sum){
				--end;
			}
			else 
				if (array[begin] + array[end] < sum) {
					++begin;
				}
			else {
				return array[begin] + " " + array[end];
			}
		}
		return "Not Match";
	}

	public double[] getA() {
		return a;
	}

	public void setA(double a[]) {
		this.a = a;
	}
	
	public double convert2int(String string) {
		double result = 0;
		int length = 0;
		while (length < string.length()) {
			if (string.charAt(length) < 48 || string.charAt(length) > 57) {
				length++;
			}
			else {
				// JAVA 自带的判断字符是不是数字
				//boolean b = Character.isDigit(string.charAt(length));
				result = result * 10 + string.charAt(length) - 48;
				length++;
			}
		}
		return result;
	}
	
	public String MatchWithRegex(String regex) {
		String a = "Tom is a cat's name.";
		Pattern pattern = Pattern.compile(regex);
			Matcher matcher = pattern.matcher(a);
			if (matcher.find()) {
				System.out.println(matcher.group());
			}
		return " ";
	}
	
	public String FindString(String Wanted) {
		List<String> all = Arrays.asList("John","Tom","Mike");
		if (all.contains(Wanted)) {
			return "YES";
		}
		return "Not Found";
		
	}
	

}
