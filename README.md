# Feathery Server-side SDK for Python

## Feathery Overview

[Feathery](https://www.feathery.tech) helps B2B software companies manage personalized customer configurations. With Feathery, SaaS providers can dynamically configure functionality and appearance for users and organizations in real-time without pushing code.

## Getting started

To get started, install the Feathery SDK from PyPI. 

```bash
pip install feathery-server-sdk
```

Next, import the Feathery client in your application code.

```py
import feathery
```

Once feathery is installed and imported, you'll want to initialize the SDK by calling `set_sdk_key`. You should only ever access the initialized client via the `get` function. This reinforces the singleton pattern, which ensures you only have a single set of Feathery resources at any given point.


```py
feathery.set_sdk_key("YOUR_SDK_KEY")
feathery_client = feathery.get()
```

Using `feathery_client`, you can check which variation a particular user should receive for a given setting. Let's walk through this snippet. The most important attribute is the user key. In this case we've used the key `"user@test.com"`. The key should uniquely identify each user. The same user always has the same key.


The default value is passed in to ensure that even if an error occurs in our application, some value is returned and can be acted on.

```py
dash_color = feathery_client.variation("dash_color", "white", "user@test.com")
```

Lastly, shut down `feathery_client` before your application terminates. This ensures that `feathery` releases any resources it is using. **This is something you only need to do once**.

```py
# shut down the client, since we're about to quit
feathery_client.close()
```
