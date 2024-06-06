package plangeneratorflink.enumeration;

import org.apache.flink.api.java.functions.NullByteKeySelector;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.ConfigOptions;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.graph.StreamGraph;
import org.apache.flink.streaming.api.graph.StreamNode;
import org.apache.flink.streaming.api.operators.StreamOperator;
import org.apache.flink.streaming.api.operators.StreamSink;
import org.apache.flink.streaming.api.operators.StreamSource;
import org.apache.flink.streaming.runtime.operators.windowing.WindowOperator;
import org.apache.flink.util.InstantiationUtil;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import plangeneratorflink.utils.RanGen;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

/** Applies the exhaustive parallelism strategy to operators. * */
public class ExhaustiveEnumerationStrategyCalculator extends EnumerationStrategyCalculator {

    private final int paraStepSize =
            config.getInteger(
                    ConfigOptions.key("exhaustiveParallelismStepSize").intType().noDefaultValue());
    private final int sourceParallelism;
    HashMap<String, Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer>>
            exhaustiveParallelismStrategy;
    private int numTopos;

    public ExhaustiveEnumerationStrategyCalculator(Configuration config, int numTopos) {
        super(config);
        this.exhaustiveParallelismStrategy = new HashMap<>();
        this.numTopos = numTopos;
        this.sourceParallelism =
                config.getInteger(ConfigOptions.key("sourceParallelism").intType().defaultValue(0));
    }

    @Override
    public <T> Integer getParallelismOfOperator(
            StreamGraph streamGraph, Graph pgfGraph, StreamNode node, String runName) {
        StreamOperator<?> op = node.getOperator();
        Integer parallelism;
        // set parallelism to 1 for Sources, Sinks and All-Window operators, for all other
        // cases set parallelism based on parallelism strategy
        if (op instanceof StreamSink
                || (op instanceof WindowOperator
                        && ((WindowOperator<?, ?, ?, ?, ?>) op).getKeySelector()
                                instanceof NullByteKeySelector)) {
            return 1;
        }
        if (sourceParallelism != 0 && op instanceof StreamSource) {
            return sourceParallelism;
        }
        String opId = node.getOperatorName();
        Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer>
                exhaustiveParallelismStrategy = this.exhaustiveParallelismStrategy.get(runName);
        Integer parallelismStrategyIndex = exhaustiveParallelismStrategy.f1;
        LinkedHashMap<Integer, HashMap<String, Integer>> strategies =
                exhaustiveParallelismStrategy.f0;
        HashMap<String, Integer> strategy = strategies.get(parallelismStrategyIndex);
        parallelism = strategy.get(opId.substring(opId.lastIndexOf('-') + 1));
        if (parallelism == null) {
            addNodeToStrategy(node.getOperatorName(), runName);
            return exhaustiveParallelismStrategy
                    .f0
                    .get(parallelismStrategyIndex)
                    .get(opId.substring(opId.lastIndexOf('-') + 1));
        }

        return parallelism;
    }

    @Override
    public boolean hasNext(String runName) {
        Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer>
                exhaustiveParallelismStrategy = this.exhaustiveParallelismStrategy.get(runName);
        if (exhaustiveParallelismStrategy == null) {
            return true;
        }
        return exhaustiveParallelismStrategy.f1 + 1 < exhaustiveParallelismStrategy.f0.size();
    }

    @Override
    public void initNewQuery(StreamGraph streamGraph, Graph pgfGraph, String runName) {
        Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer> exhaustiveStrategy =
                this.exhaustiveParallelismStrategy.get(runName);

        if (exhaustiveStrategy == null) {
            exhaustiveStrategy = new Tuple2<>();
            exhaustiveStrategy.f0 = new LinkedHashMap<>();
            exhaustiveStrategy.f1 = 0;
            this.exhaustiveParallelismStrategy.put(runName, exhaustiveStrategy);

            int initNodeIndex = 0;
            Node initNode = pgfGraph.getNode(initNodeIndex++);
            while (sourceParallelism != 0
                    && initNode.getAttribute("operatorType").equals("SourceOperator")
                    && pgfGraph.getNodeCount() > initNodeIndex) {
                initNode = pgfGraph.getNode(initNodeIndex++);
            }
            int i = 0;
            for (int para = minParallelism;
                    para <= maxParallelism;
                    para = (para + paraStepSize) / 5 * 5) {
                HashMap<String, Integer> singleInitStrategy = new HashMap<>();
                singleInitStrategy.put(
                        initNode.getId().substring(initNode.getId().lastIndexOf('-') + 1), para);
                exhaustiveStrategy.f0.put(i++, singleInitStrategy);
            }
            for (Node node : pgfGraph) {
                // skip initNode as it is already included
                if (node == initNode) {
                    continue;
                }
                // if we have a defined source parallelism we dont take the sources into account
                if (sourceParallelism != 0 && node.getAttribute("operatorType").equals("SourceOperator")) {
                    continue;
                }
                addNodeToStrategy(node.getId(), runName);
            }
            // downsizeStrategies(runName);
        } else {
            // update index so that in the next getParallelismOfOperator() calls the next strategy
            // is used
            this.exhaustiveParallelismStrategy.get(runName).f1 = ++exhaustiveStrategy.f1;
        }
    }

    private void downsizeStrategies(String runName) {
        LinkedHashMap<Integer, HashMap<String, Integer>> strategies =
                this.exhaustiveParallelismStrategy.get(runName).f0;
        LinkedHashMap<Integer, HashMap<String, Integer>> downsizedStrategies =
                new LinkedHashMap<>();
        int partSize = strategies.size() / numTopos;
        Set<Map.Entry<Integer, HashMap<String, Integer>>> entries = strategies.entrySet();
        Iterator<Map.Entry<Integer, HashMap<String, Integer>>> iterator = entries.iterator();
        LinkedHashMap<Integer, HashMap<String, Integer>> part = new LinkedHashMap<>();
        int i = 0;
        int j = 0;
        while (iterator.hasNext()) {
            Map.Entry<Integer, HashMap<String, Integer>> entry = iterator.next();
            part.put(i++, entry.getValue());
            int currentPartSize = part.size();
            if (currentPartSize >= partSize && downsizedStrategies.size() < numTopos - 1) {
                int randInt = RanGen.randInt(0, currentPartSize - 1);
                downsizedStrategies.put(j++, part.get(randInt));
                part = new LinkedHashMap<>();
                i = 0;
            }
        }
        int currentPartSize = part.size();
        if (currentPartSize > 0) {
            int randInt = RanGen.randInt(0, currentPartSize - 1);
            downsizedStrategies.put(j++, part.get(randInt));
        }
        this.exhaustiveParallelismStrategy.get(runName).f0 = downsizedStrategies;
    }

    private void addNodeToStrategy(String nodeName, String runName) {
        Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer> exhaustiveStrategy =
                this.exhaustiveParallelismStrategy.get(runName);
        LinkedHashMap<Integer, HashMap<String, Integer>> strategies = exhaustiveStrategy.f0;

        LinkedHashMap<Integer, HashMap<String, Integer>> newStrategies = new LinkedHashMap<>();

        int strategyIndex = 0;
        for (int para = minParallelism;
                para <= maxParallelism;
                para = (para + paraStepSize) / 5 * 5) {
            LinkedHashMap<Integer, HashMap<String, Integer>> clone = null;
            try {
                clone = InstantiationUtil.clone(strategies);
            } catch (IOException | ClassNotFoundException e) {
                e.printStackTrace();
            }
            for (int j = 0; j < clone.size(); j++) {
                HashMap<String, Integer> strategy = clone.get(j);
                strategy.put(nodeName.substring(nodeName.lastIndexOf('-') + 1), para);
                newStrategies.put(strategyIndex++, strategy);
            }
        }
        exhaustiveStrategy.f0 = newStrategies;
    }

    // not used anymore
    private void calculateExhaustiveParallelismStrategyIterative(
            StreamGraph streamGraph, Graph pgfGraph, String runName) {
        Stream<Node> nodesStream = pgfGraph.nodes();
        Iterator<Node> nodes = nodesStream.iterator();

        Tuple2<LinkedHashMap<Integer, HashMap<String, Integer>>, Integer> exhaustiveStrategy =
                this.exhaustiveParallelismStrategy.get(runName);

        if (exhaustiveStrategy == null) {
            exhaustiveStrategy = new Tuple2<>();
            exhaustiveStrategy.f0 = new LinkedHashMap<>();
            exhaustiveStrategy.f1 = 0;
            int nParallelisms = (maxParallelism - minParallelism) + 1;
            int combinations = (int) Math.pow(nParallelisms, pgfGraph.getNodeCount());
            int parallelismMultiplicator =
                    0; // defines how often the current parallelism will be added

            while (nodes.hasNext()) {
                Node node = nodes.next();
                if (parallelismMultiplicator == 0) {
                    parallelismMultiplicator = 1;
                } else {
                    parallelismMultiplicator = parallelismMultiplicator * nParallelisms;
                }
                int combinationIndex = 0;
                while (combinationIndex < combinations) {
                    for (int currentParallelism = minParallelism;
                            currentParallelism <= maxParallelism;
                            currentParallelism++) {
                        int startingCombinationIndex = combinationIndex;
                        for (;
                                combinationIndex
                                        < startingCombinationIndex + parallelismMultiplicator;
                                combinationIndex++) {
                            HashMap<String, Integer> currentParallelismMap =
                                    exhaustiveStrategy.f0.computeIfAbsent(
                                            combinationIndex, a -> new HashMap<>());
                            currentParallelismMap.put(
                                    node.getId().substring(node.getId().lastIndexOf('-') + 1),
                                    currentParallelism);
                        }
                    }
                }
            }
            this.exhaustiveParallelismStrategy.put(runName, exhaustiveStrategy);
        }
    }
}
