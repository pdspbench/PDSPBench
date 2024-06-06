package plangeneratorflink.enumeration;

import org.apache.flink.api.java.functions.NullByteKeySelector;
import org.apache.flink.configuration.ConfigOptions;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.graph.StreamGraph;
import org.apache.flink.streaming.api.graph.StreamNode;
import org.apache.flink.streaming.api.operators.StreamOperator;
import org.apache.flink.streaming.api.operators.StreamSink;
import org.apache.flink.streaming.api.operators.StreamSource;
import org.apache.flink.streaming.runtime.operators.windowing.WindowOperator;

import org.graphstream.graph.Graph;
import plangeneratorflink.utils.Constants;

/** Applies the random parallelism strategy to operators. * */
public class IncreasingEnumerationStrategyCalculator extends EnumerationStrategyCalculator {

    private final int calculatedQueriesPerParallelism;
    private final int stepSize;
    private int currentParallelism;
    private int queriesDone = 0;

    public IncreasingEnumerationStrategyCalculator(
            Configuration config, int numTopos, int stepSize) {
        super(config);
        this.stepSize = stepSize;
        this.currentParallelism = minParallelism;
        int p = (numTopos * stepSize) / ((maxParallelism - minParallelism) + 1);
        this.calculatedQueriesPerParallelism = p <= 0 ? 1 : p;
    }

    @Override
    public void initNewQuery(StreamGraph streamGraph, Graph pgfGraph, String runName) {
        this.currentParallelism =
                (int)
                        (Math.floor(queriesDone / this.calculatedQueriesPerParallelism)
                                        * this.stepSize
                                + minParallelism);
        this.queriesDone++;
    }

    @Override
    public <T> Integer getParallelismOfOperator(
            StreamGraph streamGraph, Graph pgfGraph, StreamNode node, String runName) {
        StreamOperator<?> op = node.getOperator();
        int parallelism = currentParallelism;
        // set parallelism to 1 for Sources, Sinks and All-Window operators, for all other
        // cases set parallelism based on parallelism strategy
        if (op instanceof StreamSource
                || op instanceof StreamSink
                || (op instanceof WindowOperator
                        && ((WindowOperator<?, ?, ?, ?, ?>) op).getKeySelector()
                                instanceof NullByteKeySelector)) {
            parallelism = 1;
            if (op instanceof StreamSource) {
                // define custom parameter or set default value out of constants
                // Integer confEventRate = pgfGraphNode.getAttribute("confEventRate",
                // Integer.class);
                parallelism =
                        config.getInteger(
                                ConfigOptions.key("sourceParallelism")
                                        .intType()
                                        .defaultValue(Constants.Synthetic.SOURCE_PARALLELISM));
            }
        }
        return parallelism;
    }

    @Override
    public boolean hasNext(String runName) {
        return currentParallelism < maxParallelism;
    }
}
