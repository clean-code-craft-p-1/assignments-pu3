# Recap of statistics

The following code returns NaN when the input is empty.

```cpp
	if (values.empty()) {
    double nan = std::numeric_limits<double>::quiet_NaN();
    return Statistics::Stats(nan, nan, nan);
  }
```

It needs `#include <limits>` in Ubuntu. It may be indirectly included in other platforms. How do we make portable code? Do we need to build on all platforms?

Is there an easier way? Use `cpplint` (included in the next assignment)

---

Use of built-in functions [in C#](https://github.com/clean-code-craft-p-1/spring-in-cs-manjunathkgphilips/blob/10bbc153656eb9e27517b55703ba122b1dee7a44/Statistics/Statistics.cs) for statistics.

---

Mistake-proofing [with spans and non-discardable return values](https://github.com/clean-code-craft-p-1/spring-in-cpp-art-pogorelov/blob/fc5a656ed2a90d4b160f491865e40222a817a7eb/stats.h#L15)

---

What else can go wrong, and what should be the behavior? [Add them as tests](https://github.com/code-craft-a1/spring-in-py-priyanja/blob/1181092a7d97deeacdcf583ebbe706064cb67312/statistics.test.py)

## Take-away

Use tests to express the specification.
