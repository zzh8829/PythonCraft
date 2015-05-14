import java.util.*;

class Test{

	public static void main(String[] args){
		Test test = new Test();
		long syst = test.sysTime();
		System.out.println(syst);

		for(int i=0;i!=100;i++){
			int a = 0;
		}
		syst = test.sysTime();
		System.out.println(syst);

	}

	public long sysTime(){
		return System.nanoTime()/1000000L;// Sys.getTime() * 1000L / Sys.getTimerResolution();
	}
}