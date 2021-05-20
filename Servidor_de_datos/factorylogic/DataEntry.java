package factorylogic;

import java.sql.Timestamp;
import java.util.Comparator;

/**
 *
 * @author LRK
 */
public class DataEntry implements Comparable<DataEntry>, Comparator<DataEntry> {

    private Timestamp tsOriginal;
    private Double xAxis;
    private Double yAxisPredicted;
    private Timestamp tsUpdate;
    private Double yAxisObserved;

    public DataEntry(Timestamp tsOriginal, double xAxis, double yAxisPredicted, Timestamp tsUpdate, double yAxisObserved) {
        this.tsOriginal = tsOriginal;
        this.xAxis = xAxis;
        this.yAxisPredicted = yAxisPredicted;
        this.tsUpdate = tsUpdate;
        this.yAxisObserved = yAxisObserved;
    }

    public DataEntry(Double xAxis, Double yAxisPredicted) {
        this.tsOriginal = new Timestamp(System.currentTimeMillis()/1000);
        this.xAxis = xAxis;
        this.yAxisPredicted = yAxisPredicted;
        this.tsUpdate = null;
        this.yAxisObserved = null;
    }

    public void update(double yAxisObserved) {
        this.tsUpdate = new Timestamp(System.currentTimeMillis()/1000);
        this.yAxisObserved = yAxisObserved;
    }

    @Override
    public String toString() {
        if (tsUpdate != null) {
            return "DataEntry{" + "Original=" + tsOriginal + ", xAxis=" + xAxis + ", yAxisPredicted=" + yAxisPredicted + ", tsUpdate=" + tsUpdate + ", yAxisObserved=" + yAxisObserved + '}';

        } else {
            return "DataEntry{" + "Original=" + tsOriginal + ", xAxis=" + xAxis + ", yAxisPredicted=" + yAxisPredicted + '}';
        }
    }
    
     @Override
    public int compareTo(DataEntry comparedEntry) {
        if(tsUpdate != null){
            if(comparedEntry.getTsUpdate() != null){
                return tsUpdate.compareTo(comparedEntry.getTsUpdate());
            }else{
                return tsUpdate.compareTo(comparedEntry.getTsOriginal());
            }
        }else{
           if(comparedEntry.getTsUpdate() != null){
                return tsOriginal.compareTo(comparedEntry.getTsUpdate());
            }else{
                return tsOriginal.compareTo(comparedEntry.getTsOriginal());
            } 
        }
    }
    
    @Override
    public int compare(DataEntry o1, DataEntry o2) {
        return o1.compareTo(o2);
    }

    public Timestamp getTsOriginal() {
        return tsOriginal;
    }

    public Double getxAxis() {
        return xAxis;
    }

    public Double getyAxisPredicted() {
        return yAxisPredicted;
    }

    public Timestamp getTsUpdate() {
        return tsUpdate;
    }

    public Double getyAxisObserved() {
        return yAxisObserved;
    }

    public void setTsOriginal(Timestamp tsOriginal) {
        this.tsOriginal = tsOriginal;
    }

    public void setxAxis(Double xAxis) {
        this.xAxis = xAxis;
    }

    public void setyAxisPredicted(Double yAxisPredicted) {
        this.yAxisPredicted = yAxisPredicted;
    }

    public void setTsUpdate(Timestamp tsUpdate) {
        this.tsUpdate = tsUpdate;
    }

    public void setyAxisObserved(Double yAxisObserved) {
        this.yAxisObserved = yAxisObserved;
    }

    

   

}
