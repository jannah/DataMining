Evaluation Notes
=================

- Use `__future__ import division` at the top as a best practice
- __Median__ for even number of observations is the __average__ of the 2 middle observations after __sorting__.
    - Refer Wikipedia: 
```
If n is odd then Median (M) = value of ((n + 1)/2)th item term.
If n is even then Median (M) = value of [((n)/2)th item term + ((n)/2 + 1)th item term ]/2
```

## Student Exemplary Solution

@morgan_wallace for great error handling of negative contributions. He checks for their __positive counterparts__ , interestingly some still have none and appropriately handles them.


