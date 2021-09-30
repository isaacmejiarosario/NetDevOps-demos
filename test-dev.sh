#!/bin/bash
cd Test
python3 ospf_test_all_vrfs.py
python3 ldp_test.py
python3 bgp_test_all_vrfs.py
python3 ping_test.py
