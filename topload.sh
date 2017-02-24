#!/bin/bash
ps -e -o pid,user,pcpu,pmem,command --sort=-pcpu |head
