package test.junit;

public class ChildrenTest extends ParentTest{  
    public ChildrenTest(){  
        System.out.println("Children Constructor invoked");  
    }  
    static{  
        System.out.println("Children static invoked");  
    }  
      
    {  
        System.out.println("Children invoked");  
    }
}
