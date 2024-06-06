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
public class ParameterBasedEnumerationStrategyCalculator extends EnumerationStrategyCalculator {

    private final int parallelism;

    public ParameterBasedEnumerationStrategyCalculator(Configuration config) {
        super(config);
        this.parallelism =
                config.getInteger(ConfigOptions.key("parallelism").intType().noDefaultValue());
        if (parallelism < 1) {
            throw new IllegalArgumentException(
                    "Defined parallelism for parameter based enumeration strategy must be greater or equal 1");
        }
    }

    @Override
    public void initNewQuery(StreamGraph streamGraph, Graph pgfGraph, String runName) {}

    @Override
    public <T> Integer getParallelismOfOperator(
            StreamGraph streamGraph, Graph pgfGraph, StreamNode node, String runName) {
        StreamOperator<?> op = node.getOperator();
        // set parallelism to 1 for Sources, Sinks and All-Window operators, for all other
        // cases set parallelism based on parallelism strategy
        int p = this.parallelism;
        if (op instanceof StreamSource
                || op instanceof StreamSink
                || (op instanceof WindowOperator
                        && ((WindowOperator<?, ?, ?, ?, ?>) op).getKeySelector()
                                instanceof NullByteKeySelector)) {
            p = 1;
            if (op instanceof StreamSource) {
                // define custom parameter or set default value out of constants
                // Integer confEventRate = pgfGraphNode.getAttribute("confEventRate",
                // Integer.class);
                p =
                        config.getInteger(
                                ConfigOptions.key("sourceParallelism")
                                        .intType()
                                        .defaultValue(Constants.Synthetic.SOURCE_PARALLELISM));
            }
        }
        return p;
    }

    @Override
    public boolean hasNext(String runName) {
        return true;
    }
}
