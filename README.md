# Feathery Server-side SDK for Python

## Feathery Overview

[Feathery](https://www.feathery.tech) helps B2B software companies manage personalized customer configurations. With Feathery, SaaS providers can dynamically configure functionality and integrations for users and organizations in real-time without pushing code. Both non-technical users and engineers are given control over the customer experience. A company’s configuration needs will evolve with the ever-growing requirements of its customers -- future-proof with Feathery instead of abusing feature flags, config files, or database tables.

## Getting started

To get started, the first step is to install the Feathery SDK as a dependency in your application using your application's dependency manager.

<CodeTabs
  defaultValue="py"
  values={[
    { label: 'Shell', value: 'py', },
  ]
}>
<CodeTabItem value="py">

```bash
pip install feathery-server-sdk
```

</CodeTabItem>
</CodeTabs>

Next you should import the Feathery client in your application code.


<CodeTabs
  defaultValue="py"
  values={[
    { label: 'Python', value: 'py', },
  ]
}>
<CodeTabItem value="py">

```py
import feathery
```

</CodeTabItem>
</CodeTabs>

Once the SDK is installed and imported, you'll want to create a single, shared instance of `feathery`. The `get()` function enforces the singleton pattern; you should only have one instance of the client in your application. You should specify your SDK key here so that your application will be authorized to connect to LaunchDarkly and for your application and environment.

<CodeTabs
  defaultValue="py"
  values={[
    { label: 'Python', value: 'py', },
  ]
}>
<CodeTabItem value="py">

```py
feathery.set_sdk_key("YOUR_SDK_KEY")
feathery_client = feathery.get()
```

</CodeTabItem>
</CodeTabs>

Using `feathery_client`, you can check which variation a particular user should receive for a given setting. Let's walk through this snippet. The most important attribute is the user key. In this case we've used the hash `"user@test.com"`. The key should uniquely identify each user. You can use a primary key, an e-mail address, or a hash, as long as the same user always has the same key.


The default value will only be returned if an error is encountered. For example, the default value returns if the feature flag key doesn't exist or the user doesn't have a key specified.


<CodeTabs
  defaultValue="py"
  values={[
    { label: 'Python', value: 'py', },
  ]
}>
<CodeTabItem value="py">

```py
show_feature = feathery_client.variation("your.flag.key", {"key": "user@test.com"}, False)

if show_feature:
  # application code to show the feature
else:
  # the code to run if the feature is off
```

</CodeTabItem>
</CodeTabs>

Lastly, when your application is about to terminate, shut down `feathery_client`. This ensures that the client releases any resources it is using, and that any pending analytics events are delivered to LaunchDarkly. If your application quits without this shutdown step, you may not see your requests and users on the dashboard, because they are derived from analytics events. **This is something you only need to do once**.

<CodeTabs
  defaultValue="py"
  values={[
    { label: 'Python', value: 'py', },
  ]
}>
<CodeTabItem value="py">

```py
# shut down the client, since we're about to quit
feathery_client.close()
```

</CodeTabItem>
</CodeTabs>
