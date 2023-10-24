![netlasso](https://github.com/rly0nheart/netlasso/assets/74001397/dee2a9b4-bc3a-4876-9ccc-a958bff7ad3d)



**Net Lasso** utilises the [Netlas.io API](https://netlas.io/api) to perform advanced searches for internet-connected (IoT) devices based on user-provided search queries.

# Installation
Net Lasso can be installed from [PyPI](https://pypi.org/project/netlasso) by running the following command
```commandline
pip install netlasso
```

# Authentication
> A valid Netlas.io API key will be required to use Net Lasso. The API key can be obtained by creating a free account on [Netlas.io](https://netlas.io)

Assumming you already have an API key, you can proceed to authenticate Net Lasso with the key by running
```commandline
netlasso --authenticate <api_key>
```
> This will encrypt and write the API key to *.netlas-auth* file in the program's installation directory.
>> It will also write the encryption key *.encryption-key* to the same directory.
>>> This ensures the user's API key is not easily accessible.

# Usage
After authenticating, you can start searching by calling Net Lasso with the required command-line arguments
```commandline
netlasso --query <query_string>
```

# Netlas.io Dorks
A [list of dorks](https://github.com/netlas-io/netlas-dorks) for the Netlas.io search engine, with which you can find millions of objects in the boundless IoE. Contains queries to search for IoT elements, protocols, communication tools, remote access, and more. 
***
[![me](https://github.com/rly0nheart/netlasso/assets/74001397/8f67cb42-8216-4ee4-95d3-1206ad4f8c72)](https://about.me/rly0nheart)

