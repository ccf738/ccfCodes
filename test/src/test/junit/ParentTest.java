package test.junit;
public class ParentTest {  
    public ParentTest(){  
        System.out.println("Parent Constructor invoked");  
    }  
    static{  
        System.out.println("parent static invoked");  
    }  
      
    {  
        System.out.println("parent invoked");  
    }  
}  