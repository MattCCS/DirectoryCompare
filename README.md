# DirectoryCompare

## Metrics
- content
- depth
- grouping

## Test Cases
```
{} x {} = 1 (∆0/1)
{A} x {A} = 1 (∆0/1)
{A} x {} = 0 (∆1/1)
{A,B} x {A} = .5 (∆1/2)
{A} x {{A}} = .5 (∆1/2)
{A,B} x {A,{B}} = .67 (∆2/6)
{{A},{B}} x {{B},{A}} = 1 (∆0/6)
```
