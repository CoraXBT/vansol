## Solana Vanity Address Generator
-----------------------------------------------------------
This Python script generates Solana vanity addresses with specified prefixes or suffixes using 
multiprocessing to enhance performance

## System Requirements
Python 3.7+: This script has been tested with Python 3.7 and newer versions

## Install Dependencies
-----------------------------------------------------------
Install Dependencies
The dependencies are specified in the requirements.txt file:
            pip install -r requirements.txt

## USING THE BOT
-----------------------------------------------------------
Once the setup is complete, you can run this script from the command line:
python bt.py --prefix <XXX> --suffix <XXX> --num_processes <XX>

EXAMPLE
To generate a Solana address ending with "444" using 8 CPU processes:
python bt.py --suffix 444 --num_processes 8

OUTPUT
Wallets: ###,### | Time: #:##:##
Address: 6TfW7ZAbHf7CkB8uNqA2FzK3tJb5QdVtvEnTaCv9q444
Secret key: 3ozXrf6QyN7nTdMQedrngneaC43hqd9JYid6e9s21eb2W5mT4svcoMPmw0CH5kBGt4tsUfnY5VxtkPD6hkXWwy4h6