#!/bin/bash

ansible-playbook -kK inventory/deploy_project.yml --extra-vars '{auth_key: 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}'
