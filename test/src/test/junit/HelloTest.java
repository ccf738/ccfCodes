package test.junit;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class HelloTest {
	Hello hello = new Hello();

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testAds() {
		int delta = 0;
		assertEquals("¾ø¶ÔÖµÊ§°Üle",14,hello.ads(12),delta);
		fail("Not yet implemented");
	}

}
