# mafia

Benchmark models with adversarial games such as Mafia.

## Intro

Existing LM benchmarks in the format of pre-written input prompts are static and
thus easy to optimize for. In this context growth from hillclimbing does not
necessarily correlate with actual progress towards AGI, which makes benchmarking
ineffective.

On the other hand, adversarial games provide an attractive alternative approach
to benchmarking. In order to win at Mafia, a model needs to engage in multi-turn
dialogue, infer hidden intentions, and provide false information in context.
These abilities are observed from a dynamic environment, which makes it
difficult to optimize over.

Deception as a modeling ability has attracted interest since the Turing Test.
Which model will win the ultimate test of intelligence?

## Run code

```
docker-compose up
```

## Contributing

- Format your code with [black](https://github.com/psf/black) before submitting.
  This helps by producing the smallest possible diff.
- Commit messages should start with tags. E.g. `[model] add Anthropic provider`
