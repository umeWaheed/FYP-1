public class LogTime
{
private String startTime;
private String endTime;
public LogTime(){
}
public LogTime(String startTime,String endTime)
{
this.startTime=startTime;
this.endTime=endTime;}

public void setStartTime(String startTime)
{this.startTime=startTime;}
public String getStartTime(){
return startTime;}
public void setEndTime(String endTime)
{this.endTime=endTime;}
public String getEndTime(){
return endTime;}
public void Stringto()
{
System.out.println(getStartTime() +getEndTime());
}

}
 
 