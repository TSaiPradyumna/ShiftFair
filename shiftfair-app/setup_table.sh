#!/bin/bash
# Run this AFTER localstack is up: ./setup_table.sh
awslocal dynamodb create-table \
    --table-name ShiftFairTable \
    --attribute-definitions AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S \
    --key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST

echo "Table created. Verify with:"
echo "awslocal dynamodb scan --table-name ShiftFairTable"
