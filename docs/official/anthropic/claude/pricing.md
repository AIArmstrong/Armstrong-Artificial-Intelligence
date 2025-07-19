---
source_url: https://docs.anthropic.com/en/docs/about-claude/pricing
scraped_date: 2025-07-15 19:15:26
scraper: Jina API via AAI Research Bot
category: anthropic_documentation
---

Title: Pricing - Anthropic

URL Source: https://docs.anthropic.com/en/docs/about-claude/pricing

Markdown Content:
This page provides detailed pricing information for Anthropic’s models and features. All prices are in USD.

For the most current pricing information, please visit [anthropic.com/pricing](https://www.anthropic.com/pricing).

Model pricing
-------------

The following table shows pricing for all Claude models across different usage tiers:

| Model | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
| --- | --- | --- | --- | --- | --- |
| Claude Opus 4 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Sonnet 4 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 3.7 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 3.5 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Haiku 3.5 | $0.80 / MTok | $1 / MTok | $1.6 / MTok | $0.08 / MTok | $4 / MTok |
| Claude Opus 3 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Haiku 3 | $0.25 / MTok | $0.30 / MTok | $0.50 / MTok | $0.03 / MTok | $1.25 / MTok |

Feature-specific pricing
------------------------

### Batch processing

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

| Model | Batch input | Batch output |
| --- | --- | --- |
| Claude Opus 4 | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 4 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.7 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.5 | $1.50 / MTok | $7.50 / MTok |
| Claude Haiku 3.5 | $0.40 / MTok | $2 / MTok |
| Claude Opus 3 | $7.50 / MTok | $37.50 / MTok |
| Claude Haiku 3 | $0.125 / MTok | $0.625 / MTok |

For more information about batch processing, see our [batch processing documentation](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing).

### Tool use pricing

Tool use requests are priced based on:

1.   The total number of input tokens sent to the model (including in the `tools` parameter)
2.   The number of output tokens generated
3.   For server-side tools, additional usage-based pricing (e.g., web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, while server-side tools may incur additional charges based on their specific usage.

The additional tokens from tool use come from:

*   The `tools` parameter in API requests (tool names, descriptions, and schemas)
*   `tool_use` content blocks in API requests and responses
*   `tool_result` content blocks in API requests

When you use `tools`, we also automatically include a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of `none` uses 0 additional system prompt tokens.

| Model | Tool choice | Tool use system prompt token count |
| --- | --- | --- |
| Claude Opus 4 | `auto`, `none` * * * `any`, `tool` | 346 tokens * * * 313 tokens |
| Claude Sonnet 4 | `auto`, `none` * * * `any`, `tool` | 346 tokens * * * 313 tokens |
| Claude Sonnet 3.7 | `auto`, `none` * * * `any`, `tool` | 346 tokens * * * 313 tokens |
| Claude Sonnet 3.5 (Oct) | `auto`, `none` * * * `any`, `tool` | 346 tokens * * * 313 tokens |
| Claude Sonnet 3.5 (June) | `auto`, `none` * * * `any`, `tool` | 294 tokens * * * 261 tokens |
| Claude Haiku 3.5 | `auto`, `none` * * * `any`, `tool` | 264 tokens * * * 340 tokens |
| Claude Opus 3 | `auto`, `none` * * * `any`, `tool` | 530 tokens * * * 281 tokens |
| Claude Sonnet 3 | `auto`, `none` * * * `any`, `tool` | 159 tokens * * * 235 tokens |
| Claude Haiku 3 | `auto`, `none` * * * `any`, `tool` | 264 tokens * * * 340 tokens |

These token counts are added to your normal input and output tokens to calculate the total cost of a request.

For current per-model prices, refer to our [model pricing](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/about-claude/pricing#model-pricing) section above.

For more information about tool use implementation and best practices, see our [tool use documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview).

### Specific tool pricing

#### Bash tool

The bash tool adds **245 input tokens** to your API calls.

Additional tokens are consumed by:

*   Command outputs (stdout/stderr)
*   Error messages
*   Large file contents

See [tool use pricing](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/about-claude/pricing#tool-use-pricing) for complete pricing details.

#### Code execution tool

The code execution tool usage is tracked separately from token usage. Execution time is a minimum of 5 minutes. If files are included in the request, execution time is billed even if the tool is not used due to files being preloaded onto the container.

**Pricing**: $0.05 per session-hour.

#### Text editor tool

The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you’re using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

| Tool | Additional input tokens |
| --- | --- |
| `text_editor_20250429` (Claude 4) | 700 tokens |
| `text_editor_20250124` (Claude Sonnet 3.7) | 700 tokens |
| `text_editor_20241022` (Claude Sonnet 3.5) | 700 tokens |

See [tool use pricing](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/about-claude/pricing#tool-use-pricing) for complete pricing details.

#### Web search tool

Web search usage is charged in addition to token usage:

Web search is available on the Anthropic API for **$10 per 1,000 searches**, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

#### Computer use tool

Computer use follows the standard [tool use pricing](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#pricing). When using the computer use tool:

**System prompt overhead**: The computer use beta adds 466-499 tokens to the system prompt

**Computer use tool token usage**:

| Model | Input tokens per tool definition |
| --- | --- |
| Claude 4 / Sonnet 3.7 | 735 tokens |
| Claude Sonnet 3.5 | 683 tokens |

**Additional token consumption**:

*   Screenshot images (see [Vision pricing](https://docs.anthropic.com/en/docs/build-with-claude/vision))
*   Tool execution results returned to Claude

Agent use case pricing examples
-------------------------------

Understanding pricing for agent applications is crucial when building with Claude. These real-world examples can help you estimate costs for different agent patterns.

### Customer support agent example

When building a customer support agent, here’s how costs might break down:

For a detailed walkthrough of this calculation, see our [customer support agent guide](https://docs.anthropic.com/en/docs/about-claude/use-case-guides/customer-support-chat).

### General agent workflow pricing

For more complex agent architectures with multiple steps:

1.   **Initial request processing**

    *   Typical input: 500-1,000 tokens
    *   Processing cost: ~$0.003 per request

2.   **Memory and context retrieval**

    *   Retrieved context: 2,000-5,000 tokens
    *   Cost per retrieval: ~$0.015 per operation

3.   **Action planning and execution**

    *   Planning tokens: 1,000-2,000
    *   Execution feedback: 500-1,000
    *   Combined cost: ~$0.045 per action

For a comprehensive guide on agent pricing patterns, see our [agent use cases guide](https://docs.anthropic.com/en/docs/about-claude/use-case-guides).

### Cost optimization strategies

When building agents with Claude:

1.   **Use appropriate models**: Choose Haiku for simple tasks, Sonnet for complex reasoning
2.   **Implement prompt caching**: Reduce costs for repeated context
3.   **Batch operations**: Use the Batch API for non-time-sensitive tasks
4.   **Monitor usage patterns**: Track token consumption to identify optimization opportunities

Additional pricing considerations
---------------------------------

### Rate limits

Rate limits vary by usage tier and affect how many requests you can make:

*   **Tier 1**: Entry-level usage with basic limits
*   **Tier 2**: Increased limits for growing applications
*   **Tier 3**: Higher limits for established applications
*   **Tier 4**: Maximum standard limits
*   **Enterprise**: Custom limits available

For detailed rate limit information, see our [rate limits documentation](https://docs.anthropic.com/en/api/rate-limits).

### Volume discounts

Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis.

*   Standard tiers use the pricing shown above
*   Enterprise customers can [contact sales](mailto:sales@anthropic.com) for custom pricing
*   Academic and research discounts may be available

### Enterprise pricing

For enterprise customers with specific needs:

*   Custom rate limits
*   Volume discounts
*   Dedicated support
*   Custom terms

Contact our sales team at [sales@anthropic.com](mailto:sales@anthropic.com) or through the [Anthropic Console](https://console.anthropic.com/settings/limits) to discuss enterprise pricing options.

Billing and payment
-------------------

*   Billing is calculated monthly based on actual usage
*   Payments are processed in USD
*   Credit card and invoicing options available
*   Usage tracking available in the [Anthropic Console](https://console.anthropic.com/)

Frequently asked questions
--------------------------

**How is token usage calculated?**

Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

**Are there free tiers or trials?**

New users receive a small amount of free credits to test the API. [Contact sales](mailto:sales@anthropic.com) for information about extended trials for enterprise evaluation.

**How do discounts stack?**

Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls.

**What payment methods are accepted?**

We accept major credit cards for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact [support@anthropic.com](mailto:support@anthropic.com).
