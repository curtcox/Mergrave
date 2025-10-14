# Mergrave

[![CI](https://github.com/curtcox/Mergrave/actions/workflows/ci.yml/badge.svg)](https://github.com/curtcox/Mergrave/actions/workflows/ci.yml)

AI function calling

The latest coverage and build artifacts are published to GitHub Pages after every
successful run of the CI workflow. You can explore the generated reports at
[https://curtcox.github.io/Mergrave/](https://curtcox.github.io/Mergrave/).

Every AI call is potentially 0 to many AI calls. 

Past calls may indicate that no AI call is needed. 
- Maybe it should be served from cache. 
- Maybe code was generated that needs to be executed instead of a call. 

Or many calls could be needed. 
- to guard against "forbidden" context being used (IP) 
- to determine optimum context (transform input) 
- to reformat output - to generate code 
- to handle errors from running generated code 
- to judge the response quality 
- to fact/quality check the response 
- to decompose into parts 
- to research existing solutions 
- to make new tools 
- to identify appropriate tools 
- to use appropriate tools 
- to determine if it makes sense to try again 
- to pick the best response after doing some of the above multiple times 
- to guard against "forbidden" knowledge coming back 
