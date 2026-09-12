\#  ShiftFair



> \*\*Fair Shift Arbitration System for Intelligent and Explainable Shift Swaps\*\*



ShiftFair is a prototype system designed to intelligently evaluate employee shift swap requests and recommend eligible swap partners using transparent and explainable decision logic.



The system evaluates factors such as:



\-  Role Matching

\-  Department Matching

\-  Schedule Availability

\-  Shift Conflict Detection

\-  Explainable Decisions



\---



\#  Version



\## Version 1.0 — Working Prototype



This repository represents the first working version of ShiftFair.



The current system provides a complete local end-to-end workflow:



```text

Frontend

&#x20;   ↓

AWS SAM API

&#x20;   ↓

AWS Lambda Functions

&#x20;   ↓

ShiftFair Arbitration Logic

&#x20;   ↓

DynamoDB

&#x20;   ↓

LocalStack

