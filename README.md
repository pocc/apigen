# MAD CodeGen
Meraki API Docs Code Generator

## Problem
There are currently 8+ client libraries for 4+ programming languages to
access the Meraki API. Most are out of date and lack a majority of endpoints. 
This project aims to fix this: 

* Create a Meraki API client for $language
* Generate a new client to handle new API calls
* Generate new documentation for using new API calls

### Current API Client libraries
Currently 212 API calls (2019-02-18)

| Language | Calls | Done | Name                                                                                                   | Comments       |
|----------|-------|------|--------------------------------------------------------------------------------------------------------|----------------|
| C#       | 20    | 9%   | [Meraki.Dashboard](https://github.com/DimensionDataCBUSydney/Meraki.Dashboard)                         |                |
| NodeJS   | 32    | 15%  | [merakiapi-node](https://github.com/mchenetz/merakiapi-node)                                           |                |
| NodeJS   | 210   | 99%  | [node-meraki-dashboard](https://github.com/tejashah88/node-meraki-dashboard)                           | Elegant API    |
| NodeJS   | 15    | 7%   | [meraki-cli](https://github.com/CumberlandGroup/meraki-cli)                                            |                |
| Postman  | 172   | 81%  | [Postman Collection](https://documenter.getpostman.com/view/897512/meraki-dashboard-api/2To9xm) | Meraki-Managed |
| Python   | 98    | 46%  | [dashboard-api-python](https://github.com/meraki/dashboard-api-python)                                 | Meraki-Managed |
| Python   | 33    | 16%  | [meraki_api](https://github.com/guzmonne/meraki_api/tree/master/meraki_api)                            |                |
| Ruby     | 57    | 27%  | [dashboardapi](https://github.com/jletizia/dashboardapi)                                               | Meraki-Managed |

> List source: https://github.com/CiscoDevNet/awesome-merakiapis

## Installation
### Optional Requires
* java > v1.8 for code generation
* node > 6 for conversion to Postman collection

### Install
(Until this is uploaded to PyPi)
```
git clone https://github.com/pocc/mad-codegen
python gateway.py
```

## Acknowledgements
@shiyuechengineer, @jletizia: For making API clients that inspired this project.
 
Projects: swagger-codegen, openapi-to-postman for enabling features 