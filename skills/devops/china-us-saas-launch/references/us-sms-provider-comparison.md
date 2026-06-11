# US SMS Provider Comparison for Non-US Developers

Sending SMS to US phones from a non-US base. Focus on: non-resident accessibility, US compliance, pricing.

## Provider Comparison

| Provider | Non-US Signup | 10DLC Registration | Pricing (US) | Best For |
|----------|---------------|-------------------|--------------|----------|
| **Telnyx** | ✅ Works with VPN, non-resident friendly | Built-in | ~$0.004/sms + $1/mo/number | **Recommended for non-US founders** |
| **AWS SNS** | ✅ Works with AWS global account | Requires separate registration | ~$0.006/sms | If already on AWS |
| **Twilio** | ⚠️ May flag Chinese IPs, use VPN during signup | Built-in | ~$0.008/sms + $1.15/mo/number | Most features, but trickier registration |
| **Vonage** | ✅ Works | Built-in | ~$0.006/sms | Good alternative |
| **BulkSMS** | ✅ Works | Manual | ~$0.005/sms | Simple, no-frills |

## MVP Recommendation: Skip SMS, Use Email

| Tier | Channel | Tool | Cost | Capacity |
|------|---------|------|------|----------|
| MVP (<100 customers) | Email only | **SendGrid Free** | $0 | 100 emails/day |
| Growth (<500 customers) | Email + SMS | Telnyx | ~$10-30/mo | Pay as you go |
| Scale (500+ customers) | Email + SMS + phone | Telnyx + Twilio | ~$50-200/mo | Volume pricing |

## US SMS Compliance (TCPA)

Required for any SaaS sending SMS to US numbers:

1. ✅ **Opt-in consent** — Store explicit consent in DB (SepticSaver has this: `sms_consent` field)
2. ✅ **Opt-out mechanism** — Reply STOP to opt out (SepticSaver has: unsubscribe webhook)
3. ✅ **Frequency disclosure** — Tell customer how often they'll get messages
4. ✅ **Privacy policy** — Must mention SMS data collection (SepticSaver has: privacy.html)

## Implementation Notes

- Use a US toll-free number (not short code) for MVP — cheaper, faster to provision
- 10DLC registration ($4-15/mo per brand) is required for application-to-person SMS in the US
- Test messages with actual US carriers (Verizon, T-Mobile, AT&T) before launch
