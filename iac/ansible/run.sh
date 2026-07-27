#!/bin/bash

ansible vbox -m ping -i inventory.ini -K

ansible-playbook main.yml -K