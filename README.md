# Flows

In the UK electricity market [MRASCo](https://www.mrasco.com/) provides governance to manage processes between electricity suppliers and distribution companies. Their solution - the [DTC](https://www.mrasco.com/mra-products/data-transfer-catalogue/) - is file 'flows' which are sent between market participants over the Data Transfer Network. The problem is that these file flows are presented in a nested-CSV format which isn't easily accessible for data engineers who often have to write complex logic to extract the individual data items relating to an MPAN.

This package provides easy transform between DTC flows format into JSON format, which should be much more accessible.

### Example

Original DTC File Flow:

```
GGG|sadfasdf TODO... add example file
```

JSON Output:

```
{
    "GGG": "sadfasdf"  TODO... add example JSON result
}
```

## How to use

Install:
```
pip install flows
```

Use:
```python:
import flows
json_output = flows.transform(file.read())
```

## Licence

Copyright (c) 2015 Ben Pine
Licensed under the GNU GPLv3.