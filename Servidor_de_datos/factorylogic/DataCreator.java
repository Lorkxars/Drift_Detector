package factorylogic;

import java.util.List;
import java.util.SortedSet;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author LRK
 */
public class DataCreator implements Runnable {

    private SortedSet data;
    private Thread t;
    private double threadDelay = 30;

    public DataCreator(SortedSet data) {
        this.data = data;
    }

    @Override
    public void run() {
        while (true) {
            try {
                long sleepTime = (long) (Math.random() * threadDelay);
                TimeUnit.SECONDS.sleep(sleepTime);
                DataEntry newData = createNewData();
                synchronized (data) {
                    data.add(newData);
                }
                sleepTime = (long) (Math.random() * threadDelay);
                TimeUnit.SECONDS.sleep(sleepTime);
                synchronized (data) {
                    updateData(newData);
                }
            } catch (InterruptedException ex) {
                Logger.getLogger(DataCreator.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    private DataEntry createNewData() {
        double slope = 20;

        Double xAxis = (Math.random() * 40) - 20; //-20 to 20 range
        Double yAxisPredicted = slope * xAxis;

        return new DataEntry(xAxis, yAxisPredicted);
    }

    private void updateData(DataEntry entryToUpdate) {
        double factor = 5;
        double slope = 20;

        Double xAxis = entryToUpdate.getxAxis();
        Double yAxisObserved = slope * xAxis + (Math.random() * factor);

        entryToUpdate.update(yAxisObserved);
    }

    public void start() {
        System.out.println("Starting ");
        if (t == null) {
            t = new Thread(this);
            t.start();
        }
    }
}
