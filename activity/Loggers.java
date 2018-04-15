import java.io.*;
import java.util.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.lang.*;

public class Loggers {
      
     public static void main(String[] args)
	{
		 String key=null;
		 String[] log;
         String et=null,st=null;
        try 
		{
			HashMap<String,LogTime > hmap = new HashMap<String,LogTime>();
		    FileReader reader = new FileReader("t_log.txt");
            BufferedReader bufferedReader = new BufferedReader(reader);
			FileWriter writer = new FileWriter("Project_log.txt", true);
            PrintWriter printwriter=new PrintWriter(writer);
           
			String line=bufferedReader.readLine();
           
		   while (line!= null) {
			log= line.split("\\s+");
			if(log.length>=5)
			{
				// the fifth element is the name of application
			    key=log[3];
				System.out.print("\n"+key);
				line=bufferedReader.readLine();
				if (line != null){
					log = line.split("\\s+");
					if(log.length==3)
					{	
						if(log[2].equals("START"))
						{
							st=log[1].substring(11,19);
							System.out.print(" "+st);
							line=bufferedReader.readLine();
							log = line.split("\\s+");
							if (log.length==3){
								//end
								if(log[2].equals("END")){
									et=log[1].substring(11,19);
									System.out.println(" "+et);
									printwriter.println(key+"     "+st+"    "+et);
								}
							}	
						}
					}
					else{
						continue;
						// skip the steps below
					}
				}
			}
			
			line=bufferedReader.readLine();
		}
			bufferedReader.close();
			reader.close();
			printwriter.flush();
			writer.close();
			
 
        } 
		catch (IOException e)
		   {
            e.printStackTrace();
           }
	}
}