---
source_url: https://docs.anthropic.com/en/api/getting-started
scraped_date: 2025-07-15 19:15:00
scraper: Jina API via AAI Research Bot
category: anthropic_documentation
---

Title: Overview - Anthropic

URL Source: https://docs.anthropic.com/en/api/getting-started

Markdown Content:
Overview - Anthropic

===============

[Anthropic home page![Image 1: light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![Image 2: dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

*   [Research](https://www.anthropic.com/research)
*   [Login](https://console.anthropic.com/login)
*   [Support](https://support.anthropic.com/)
*   [Sign up](https://console.anthropic.com/login)
*   [Sign up](https://console.anthropic.com/login)

Search...

Navigation

Using the APIs

Overview

[Welcome](https://docs.anthropic.com/en/home)[Developer Platform](https://docs.anthropic.com/en/docs/intro)[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)[Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp)[API Reference](https://docs.anthropic.com/en/api/messages)[Resources](https://docs.anthropic.com/en/resources/overview)[Release Notes](https://docs.anthropic.com/en/release-notes/overview)

*   [Developer Guide](https://docs.anthropic.com/en/docs/intro)
*   [API Guide](https://docs.anthropic.com/en/api/overview)

##### Using the APIs

*   [Overview](https://docs.anthropic.com/en/api/overview)
*   [Rate limits](https://docs.anthropic.com/en/api/rate-limits)
*   [Service tiers](https://docs.anthropic.com/en/api/service-tiers)
*   [Errors](https://docs.anthropic.com/en/api/errors)
*   [Handling stop reasons](https://docs.anthropic.com/en/api/handling-stop-reasons)
*   [Beta headers](https://docs.anthropic.com/en/api/beta-headers)

##### API reference

*   Messages  
*   Models  
*   Message Batches  
*   Files  
*   Admin API  
*   Experimental APIs  
*   Text Completions (Legacy)  

##### SDKs

*   [Client SDKs](https://docs.anthropic.com/en/api/client-sdks)
*   [OpenAI SDK compatibility](https://docs.anthropic.com/en/api/openai-sdk)

##### Examples

*   [Messages examples](https://docs.anthropic.com/en/api/messages-examples)
*   [Message Batches examples](https://docs.anthropic.com/en/api/messages-batch-examples)

##### 3rd-party APIs

*   [Amazon Bedrock API](https://docs.anthropic.com/en/api/claude-on-amazon-bedrock)
*   [Vertex AI API](https://docs.anthropic.com/en/api/claude-on-vertex-ai)

##### Support & configuration

*   [Versions](https://docs.anthropic.com/en/api/versioning)
*   [IP addresses](https://docs.anthropic.com/en/api/ip-addresses)
*   [Supported regions](https://docs.anthropic.com/en/api/supported-regions)
*   [Using the Admin API](https://docs.anthropic.com/en/api/administration-api)
*   [Getting help](https://docs.anthropic.com/en/api/getting-help)

Using the APIs

Overview
========

Copy page

[​](https://docs.anthropic.com/en/api/getting-started#accessing-the-api)

Accessing the API
-------------------------------------------------------------------------------------------

The API is made available via our web [Console](https://console.anthropic.com/). You can use the [Workbench](https://console.anthropic.com/workbench/3b57d80a-99f2-4760-8316-d3bb14fbfb1e) to try out the API in the browser and then generate API keys in [Account Settings](https://console.anthropic.com/account/keys). Use [workspaces](https://console.anthropic.com/settings/workspaces) to segment your API keys and [control spend](https://docs.anthropic.com/en/api/rate-limits) by use case.

[​](https://docs.anthropic.com/en/api/getting-started#authentication)

Authentication
-------------------------------------------------------------------------------------

All requests to the Anthropic API must include an `x-api-key` header with your API key. If you are using the Client SDKs, you will set the API when constructing a client, and then the SDK will send the header on your behalf with every request. If integrating directly with the API, you’ll need to send this header yourself.

[​](https://docs.anthropic.com/en/api/getting-started#content-types)

Content types
-----------------------------------------------------------------------------------

The Anthropic API always accepts JSON in request bodies and returns JSON in response bodies. You will need to send the `content-type: application/json` header in requests. If you are using the Client SDKs, this will be taken care of automatically.

[​](https://docs.anthropic.com/en/api/getting-started#response-headers)

Response Headers
-----------------------------------------------------------------------------------------

The Anthropic API includes the following headers in every response:

*   `request-id`: A globally unique identifier for the request.

*   `anthropic-organization-id`: The organization ID associated with the API key used in the request.

[​](https://docs.anthropic.com/en/api/getting-started#examples)

Examples
-------------------------------------------------------------------------

*   curl
*   Python
*   TypeScript

Shell

```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
```

Shell

```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-20250514",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
```

Install via PyPI:

```bash
pip install anthropic
```

Python

```Python
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
message = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content)
```

Install via npm:

```bash
npm install @anthropic-ai/sdk
```

TypeScript

```TypeScript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: 'my_api_key', // defaults to process.env["ANTHROPIC_API_KEY"]
});

const msg = await anthropic.messages.create({
  model: "claude-opus-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(msg);
```

Was this page helpful?

Yes No

[Rate limits](https://docs.anthropic.com/en/api/rate-limits)

[x](https://x.com/AnthropicAI)[linkedin](https://www.linkedin.com/company/anthropicresearch)[discord](https://www.anthropic.com/discord)

On this page

*   [Accessing the API](https://docs.anthropic.com/en/api/getting-started#accessing-the-api)
*   [Authentication](https://docs.anthropic.com/en/api/getting-started#authentication)
*   [Content types](https://docs.anthropic.com/en/api/getting-started#content-types)
*   [Response Headers](https://docs.anthropic.com/en/api/getting-started#response-headers)
*   [Examples](https://docs.anthropic.com/en/api/getting-started#examples)
