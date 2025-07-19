---
source_url: https://docs.anthropic.com/en/api/errors
scraped_date: 2025-07-15 19:15:02
scraper: Jina API via AAI Research Bot
category: anthropic_documentation
---

Title: Errors - Anthropic

URL Source: https://docs.anthropic.com/en/api/errors

Markdown Content:
HTTP errors
-----------

Our API follows a predictable HTTP error code format:

*   400 - `invalid_request_error`: There was an issue with the format or content of your request. We may also use this error type for other 4XX status codes not listed below.

*   401 - `authentication_error`: There’s an issue with your API key.

*   403 - `permission_error`: Your API key does not have permission to use the specified resource.

*   404 - `not_found_error`: The requested resource was not found.

*   413 - `request_too_large`: Request exceeds the maximum allowed number of bytes.

*   429 - `rate_limit_error`: Your account has hit a rate limit.

*   500 - `api_error`: An unexpected error has occurred internal to Anthropic’s systems.

*   529 - `overloaded_error`: Anthropic’s API is temporarily overloaded.

When receiving a [streaming](https://docs.anthropic.com/en/api/streaming) response via SSE, it’s possible that an error can occur after returning a 200 response, in which case error handling wouldn’t follow these standard mechanisms.

Error shapes
------------

Errors are always returned as JSON, with a top-level `error` object that always includes a `type` and `message` value. For example:

JSON

In accordance with our [versioning](https://docs.anthropic.com/en/api/versioning) policy, we may expand the values within these objects, and it is possible that the `type` values will grow over time.

Request id
----------

Every API response includes a unique `request-id` header. This header contains a value such as `req_018EeWyXxfu5pfWkrYcMdjWG`. When contacting support about a specific request, please include this ID to help us quickly resolve your issue.

Our official SDKs provide this value as a property on top-level response objects, containing the value of the `request-id` header:

Long requests
-------------

We do not recommend setting a large `max_tokens` values without using our [streaming Messages API](https://docs.anthropic.com/en/api/streaming) or [Message Batches API](https://docs.anthropic.com/en/api/creating-message-batches):

*   Some networks may drop idle connections after a variable period of time, which can cause the request to fail or timeout without receiving a response from Anthropic.
*   Networks differ in reliability; our [Message Batches API](https://docs.anthropic.com/en/api/creating-message-batches) can help you manage the risk of network issues by allowing you to poll for results rather than requiring an uninterrupted network connection.

If you are building a direct API integration, you should be aware that setting a [TCP socket keep-alive](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/programming.html) can reduce the impact of idle connection timeouts on some networks.

Our [SDKs](https://docs.anthropic.com/en/api/client-sdks) will validate that your non-streaming Messages API requests are not expected to exceed a 10 minute timeout and also will set a socket option for TCP keep-alive.
