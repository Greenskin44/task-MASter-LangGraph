# Performance Benchmarks

This document describes the performance benchmarking suite for the LangGraph project and provides baseline metrics for all graphs.

## Overview

Performance benchmarks are implemented using `pytest-benchmark` to measure execution times and detect performance regressions. The benchmark suite covers all graph types:

- **Studio Graphs**: Parallelization, Sub-graphs, Map-reduce, Research Assistant
- **Deployment Graphs**: Task Maistro
- **Email Assistant**: Email triage workflows
- **Research Agent**: Research workflow

## Running Benchmarks

### Basic Benchmark Execution

Run all benchmarks:
```bash
pytest tests/test_benchmarks.py --benchmark-only
```

Run specific benchmark class:
```bash
pytest tests/test_benchmarks.py::TestStudioGraphBenchmarks --benchmark-only
```

Run specific benchmark:
```bash
pytest tests/test_benchmarks.py::TestStudioGraphBenchmarks::test_parallelization_performance --benchmark-only
```

### Benchmark Options

Save benchmark results:
```bash
pytest tests/test_benchmarks.py --benchmark-only --benchmark-save=baseline
```

Compare with previous results:
```bash
pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline
```

Generate histogram:
```bash
pytest tests/test_benchmarks.py --benchmark-only --benchmark-histogram
```

Set minimum rounds:
```bash
pytest tests/test_benchmarks.py --benchmark-only --benchmark-min-rounds=5
```

Disable garbage collection during benchmarks:
```bash
pytest tests/test_benchmarks.py --benchmark-only --benchmark-disable-gc
```

## Baseline Performance Metrics

The following metrics represent baseline performance on a standard development machine. Actual performance will vary based on:
- Hardware specifications (CPU, RAM)
- Network latency to API endpoints
- API response times (OpenAI, Tavily, Wikipedia)
- System load

**Test Environment:**
- Platform: Windows (CPython 3.13, 64-bit)
- Benchmark rounds: 5 minimum per test
- Date: November 2024

### Studio Graphs

| Graph | Mean (ms) | Min (ms) | Max (ms) | StdDev (ms) | Notes |
|-------|-----------|----------|----------|-------------|-------|
| Sub-graphs | 7.43 | 3.80 | 60.20 | 7.17 | Log analysis with sub-graphs (fastest) |
| Map-reduce | 3,667.11 | 3,263.99 | 4,381.23 | 453.23 | Joke generation with map-reduce |
| Parallelization | 4,488.17 | 4,363.81 | 4,749.13 | 166.23 | Parallel web + Wikipedia search |
| Research Assistant | 5,555.93 | 4,206.62 | 6,822.89 | 970.90 | Multi-agent research (2 analysts, creation phase) |

### Deployment Graphs

| Graph | Mean (ms) | Min (ms) | Max (ms) | StdDev (ms) | Notes |
|-------|-----------|----------|----------|-------------|-------|
| Task Maistro | 3,930.57 | 2,901.81 | 5,586.16 | 1,012.53 | Task management with memory |

### Email Assistant

| Graph | Mean (ms) | Min (ms) | Max (ms) | StdDev (ms) | Notes |
|-------|-----------|----------|----------|-------------|-------|
| Email Triage (Respond) | 5,620.74 | 5,213.79 | 6,293.62 | 400.93 | Email classification + response |
| Email Triage (Notify) | 2,796.14 | 2,021.12 | 3,482.76 | 601.30 | Email classification + notification |

### Research Agent

| Graph | Mean (ms) | Min (ms) | Max (ms) | StdDev (ms) | Notes |
|-------|-----------|----------|----------|-------------|-------|
| Research Workflow | N/A | N/A | N/A | N/A | Requires async execution (skipped in sync benchmarks) |

### Performance Summary

**Fastest Graphs** (< 10ms):
- Sub-graphs: 7.43ms - Excellent for high-throughput scenarios

**Fast Graphs** (< 3s):
- Email Triage (Notify): 2.80s - Quick classification without response generation

**Medium Graphs** (3-4s):
- Map-reduce: 3.67s - Balanced performance for joke generation
- Task Maistro: 3.93s - Good performance for memory operations

**Slower Graphs** (4-6s):
- Parallelization: 4.49s - Multiple API calls (web + Wikipedia)
- Research Assistant: 5.56s - Complex multi-agent coordination
- Email Triage (Respond): 5.62s - Full response generation workflow

**Performance Characteristics:**
- Sub-graphs shows excellent consistency (low StdDev: 7.17ms)
- Parallelization shows good consistency (StdDev: 166.23ms)
- Task Maistro shows higher variability (StdDev: 1,012.53ms) due to memory operations
- Research Assistant shows moderate variability (StdDev: 970.90ms) due to LLM calls

## Establishing Baselines

To establish baseline metrics for your environment:

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```bash
   OPENAI_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   LANGSMITH_API_KEY=your_key_here
   ```

3. Run benchmarks and save results:
   ```bash
   pytest tests/test_benchmarks.py --benchmark-only --benchmark-save=baseline
   ```

4. View results:
   ```bash
   pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline
   ```

## Performance Regression Testing

### Continuous Integration

Add benchmark execution to your CI/CD pipeline to detect performance regressions:

```yaml
# Example GitHub Actions workflow
- name: Run performance benchmarks
  run: |
    pytest tests/test_benchmarks.py --benchmark-only --benchmark-save=ci-run
    pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline --benchmark-compare-fail=mean:10%
```

The `--benchmark-compare-fail` option will fail the build if performance degrades by more than the specified threshold (e.g., 10% slower).

### Recommended Regression Thresholds

Based on baseline metrics, here are recommended thresholds for detecting regressions:

**Fast Graphs** (< 10ms):
- Sub-graphs: Fail if > 15ms (100% increase) - Very sensitive to changes

**Medium Graphs** (2-4s):
- Email Triage (Notify): Fail if > 3,500ms (25% increase)
- Map-reduce: Fail if > 4,500ms (23% increase)
- Task Maistro: Fail if > 5,000ms (27% increase)

**Slower Graphs** (4-6s):
- Parallelization: Fail if > 5,500ms (23% increase)
- Research Assistant: Fail if > 7,000ms (26% increase)
- Email Triage (Respond): Fail if > 7,000ms (25% increase)

**Example CI command with specific thresholds:**
```bash
# Fail if any graph is more than 20% slower than baseline
pytest tests/test_benchmarks.py --benchmark-only \
  --benchmark-compare=baseline \
  --benchmark-compare-fail=mean:20%
```

### Local Regression Testing

Before committing changes that might affect performance:

1. Run benchmarks and save as baseline:
   ```bash
   pytest tests/test_benchmarks.py --benchmark-only --benchmark-save=before-changes
   ```

2. Make your changes

3. Run benchmarks again and compare:
   ```bash
   pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=before-changes
   ```

4. Review the comparison output for any significant regressions

## Interpreting Results

### Benchmark Statistics

pytest-benchmark provides several statistics for each benchmark:

- **Min**: Fastest execution time
- **Max**: Slowest execution time
- **Mean**: Average execution time
- **StdDev**: Standard deviation (consistency)
- **Median**: Middle value (50th percentile)
- **IQR**: Interquartile range (spread of middle 50%)
- **Outliers**: Number of outlier measurements
- **Rounds**: Number of benchmark iterations

### What to Look For

**Good Performance**:
- Low mean execution time
- Low standard deviation (consistent)
- Few outliers
- Stable across multiple runs

**Performance Issues**:
- High mean execution time
- High standard deviation (inconsistent)
- Many outliers
- Degradation over time

### Common Performance Factors

**API Latency**:
- Network latency to OpenAI, Tavily, Wikipedia
- API response times vary by load
- Consider using LangSmith tracing to identify slow API calls

**Graph Complexity**:
- Number of nodes and edges
- Parallel vs sequential execution
- Number of LLM calls

**Data Size**:
- Input size (e.g., number of logs, email length)
- Context size for LLM calls
- Number of analysts in research assistant

## Optimization Strategies

### Parallel Execution

Leverage LangGraph's parallel execution capabilities:
- Use `Send()` API for dynamic parallelism
- Identify independent operations that can run concurrently
- Balance parallelism with API rate limits

### Caching

Implement caching for expensive operations:
- Cache LLM responses for repeated queries
- Cache search results for common topics
- Use LangGraph checkpointing for state persistence

### Prompt Optimization

Optimize prompts for efficiency:
- Reduce prompt length where possible
- Use structured outputs to minimize parsing
- Consider using smaller models for simple tasks

### Monitoring

Use LangSmith for detailed performance monitoring:
- Trace individual node execution times
- Identify bottlenecks in graph execution
- Monitor API call patterns and costs

## Benchmark Maintenance

### When to Update Baselines

Update baseline metrics when:
- Upgrading LangGraph or LangChain versions
- Changing graph implementations
- Optimizing performance
- Changing API providers or models

### Benchmark Coverage

Ensure benchmarks cover:
- All graph types (studio, deployment, email, research)
- Representative input scenarios
- Both fast and slow execution paths
- Edge cases that might affect performance

### Best Practices

1. **Run benchmarks in consistent environment**: Same hardware, network conditions
2. **Minimize background processes**: Close unnecessary applications
3. **Use multiple rounds**: Default is usually sufficient, but increase for more accuracy
4. **Save results**: Keep historical data for trend analysis
5. **Document changes**: Note any changes that affect performance
6. **Review regularly**: Check for performance degradation over time

## Troubleshooting

### Benchmarks Taking Too Long

If benchmarks take too long to run:
- Reduce the number of rounds: `--benchmark-min-rounds=3`
- Skip slow benchmarks: Use markers to exclude specific tests
- Use faster test inputs: Smaller data sets for benchmarking

### Inconsistent Results

If benchmark results are inconsistent:
- Check for background processes consuming resources
- Ensure stable network connection
- Increase number of rounds for better statistical accuracy
- Use `--benchmark-disable-gc` to reduce garbage collection impact

### API Rate Limits

If hitting API rate limits during benchmarks:
- Add delays between benchmark runs
- Reduce number of rounds
- Use separate API keys for benchmarking
- Run benchmarks during off-peak hours

## Analyzing Benchmark Results

### Understanding the Output

When you run benchmarks, pytest-benchmark provides detailed statistics:

```
Name (time in ms)                    Min      Max      Mean    StdDev   Median    IQR
test_sub_graphs_performance         3.80    60.20     7.43     7.17     5.92     1.94
```

**Key Metrics:**
- **Min**: Best case performance (fastest run)
- **Max**: Worst case performance (slowest run)
- **Mean**: Average performance across all runs
- **StdDev**: Consistency indicator (lower is better)
- **Median**: Middle value (less affected by outliers)
- **IQR**: Spread of middle 50% of results

### Comparison Output

When comparing with baseline:

```
Name (time in ms)                              Min         Max        Mean
test_sub_graphs_performance (NOW)            2.95 (1.0)   4.07 (1.0)  3.47 (1.0)
test_sub_graphs_performance (baseline)       3.80 (1.29)  60.20 (14.78) 7.43 (2.14)
```

The numbers in parentheses show the ratio compared to the current run:
- `(1.0)` = baseline (current run)
- `(2.14)` = 2.14x slower than current run
- `(0.5)` = 2x faster than current run

### Identifying Performance Issues

**Red Flags:**
1. **High StdDev**: Inconsistent performance, investigate variability
2. **Large Max/Min ratio**: Outliers present, may indicate issues
3. **Increasing Mean over time**: Performance degradation
4. **High comparison ratios**: Significant regression detected

**Example Analysis:**
```
# Good: Consistent performance
Mean: 100ms, StdDev: 5ms (5% variation)

# Concerning: Inconsistent performance
Mean: 100ms, StdDev: 50ms (50% variation)
```

### Benchmark Data Storage

Benchmark results are stored in `.benchmarks/` directory:
```
.benchmarks/
└── Windows-CPython-3.13-64bit/
    ├── 0001_baseline.json
    ├── 0002_baseline.json
    └── 0003_my_test.json
```

Each file contains:
- Benchmark statistics (min, max, mean, etc.)
- System information (platform, Python version)
- Timestamp and commit information
- Full result data for comparison

### Viewing Historical Data

List all saved benchmarks:
```bash
ls .benchmarks/Windows-CPython-3.13-64bit/
```

Compare any two benchmarks:
```bash
pytest tests/test_benchmarks.py --benchmark-only \
  --benchmark-compare=0001_baseline \
  --benchmark-compare=0002_baseline
```

## Using Benchmarks in Development

### Before Making Changes

1. **Establish baseline:**
   ```bash
   python scripts/run_benchmarks.py --save before-changes
   ```

2. **Make your code changes**

3. **Run benchmarks again:**
   ```bash
   python scripts/run_benchmarks.py --compare before-changes
   ```

4. **Review results:**
   - Check if any graphs are significantly slower
   - Investigate any regressions > 20%
   - Consider if performance trade-offs are acceptable

### During Code Review

Include benchmark results in pull requests:
```bash
# Run benchmarks and save results
python scripts/run_benchmarks.py --save pr-123

# Compare with main branch baseline
python scripts/run_benchmarks.py --compare main-baseline
```

Add comparison output to PR description to show performance impact.

### Optimizing Performance

If benchmarks show performance issues:

1. **Profile the code:**
   - Use LangSmith tracing to identify slow nodes
   - Check for unnecessary API calls
   - Look for sequential operations that could be parallel

2. **Test optimizations:**
   - Run benchmarks before and after each optimization
   - Verify improvements are significant (> 10%)
   - Ensure optimizations don't break functionality

3. **Document changes:**
   - Update baseline after confirmed improvements
   - Note optimization techniques in commit messages
   - Update PERFORMANCE_BENCHMARKS.md if needed

## Future Enhancements

Potential improvements to the benchmark suite:

1. **Memory profiling**: Track memory usage patterns with `pytest-memray`
2. **Cost tracking**: Monitor API call costs and token usage
3. **Scalability testing**: Test with varying input sizes (small, medium, large)
4. **Stress testing**: Test under high load conditions with concurrent requests
5. **Comparative benchmarks**: Compare different implementations or models
6. **Automated reporting**: Generate performance reports automatically in CI/CD
7. **Async benchmarks**: Add benchmarks for async graph execution
8. **Network simulation**: Test with simulated network latency
9. **Resource monitoring**: Track CPU and memory usage during execution
10. **Cost per operation**: Calculate API costs per graph execution

## References

- [pytest-benchmark documentation](https://pytest-benchmark.readthedocs.io/)
- [LangSmith tracing](https://docs.smith.langchain.com/)
- [LangGraph performance optimization](https://langchain-ai.github.io/langgraph/)
- [Python profiling guide](https://docs.python.org/3/library/profile.html)
