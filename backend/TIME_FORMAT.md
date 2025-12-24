# Time Format Guide

The `/api/bookings` endpoint expects **ISO 8601 format** datetime strings for `start_time` and `end_time`.

## Format: ISO 8601

The API accepts ISO 8601 datetime strings with or without timezone information.

### Format Pattern

```
YYYY-MM-DDTHH:MM:SS[±HH:MM]
```

Where:
- `YYYY` = 4-digit year
- `MM` = 2-digit month (01-12)
- `DD` = 2-digit day (01-31)
- `T` = literal "T" separator between date and time
- `HH` = 2-digit hour (00-23)
- `MM` = 2-digit minute (00-59)
- `SS` = 2-digit second (00-59, optional)
- `[±HH:MM]` = timezone offset (optional)

## Examples

### With Timezone Offset (Recommended)

**Eastern Time (EST/EDT):**
```json
{
  "start_time": "2024-12-20T14:00:00-05:00",
  "end_time": "2024-12-20T14:30:00-05:00"
}
```

**Pacific Time (PST/PDT):**
```json
{
  "start_time": "2024-12-20T11:00:00-08:00",
  "end_time": "2024-12-20T11:30:00-08:00"
}
```

**UTC (using 'Z' notation):**
```json
{
  "start_time": "2024-12-20T19:00:00Z",
  "end_time": "2024-12-20T19:30:00Z"
}
```

**UTC (using +00:00):**
```json
{
  "start_time": "2024-12-20T19:00:00+00:00",
  "end_time": "2024-12-20T19:30:00+00:00"
}
```

### Without Timezone (Uses Default)

If you don't specify a timezone, the API will assume your configured timezone (default: `America/Toronto`).

```json
{
  "start_time": "2024-12-20T14:00:00",
  "end_time": "2024-12-20T14:30:00"
}
```

**Note**: It's recommended to always include timezone information to avoid ambiguity.

## Valid Examples

✅ **With seconds:**
```
2024-12-20T14:00:00-05:00
```

✅ **Without seconds:**
```
2024-12-20T14:00-05:00
```

✅ **UTC with Z:**
```
2024-12-20T19:00:00Z
```

✅ **UTC with +00:00:**
```
2024-12-20T19:00:00+00:00
```

✅ **No timezone (uses default):**
```
2024-12-20T14:00:00
```

## Invalid Examples

❌ **Wrong separator (space instead of T):**
```
2024-12-20 14:00:00-05:00  # ❌ Invalid
```

❌ **Wrong date format:**
```
12/20/2024 14:00:00  # ❌ Invalid
```

❌ **12-hour format:**
```
2024-12-20T02:00:00 PM-05:00  # ❌ Invalid
```

❌ **Missing T separator:**
```
2024-12-2014:00:00-05:00  # ❌ Invalid
```

## Generating ISO 8601 Strings

### Python

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# With timezone
tz = ZoneInfo("America/Toronto")
start = datetime(2024, 12, 20, 14, 0, 0, tzinfo=tz)
start_iso = start.isoformat()
# Result: "2024-12-20T14:00:00-05:00"

# UTC
start_utc = datetime.now(ZoneInfo("UTC"))
start_utc_iso = start_utc.isoformat()
# Result: "2024-12-20T19:00:00+00:00"
```

### JavaScript

```javascript
// Create a date
const start = new Date('2024-12-20T14:00:00-05:00');

// Convert to ISO 8601
const startISO = start.toISOString();
// Result: "2024-12-20T19:00:00.000Z" (converts to UTC)

// Or format manually with timezone
const startLocal = new Date(2024, 11, 20, 14, 0, 0);
const year = startLocal.getFullYear();
const month = String(startLocal.getMonth() + 1).padStart(2, '0');
const day = String(startLocal.getDate()).padStart(2, '0');
const hours = String(startLocal.getHours()).padStart(2, '0');
const minutes = String(startLocal.getMinutes()).padStart(2, '0');
const tzOffset = -startLocal.getTimezoneOffset() / 60;
const tzSign = tzOffset >= 0 ? '+' : '-';
const tzHours = String(Math.abs(tzOffset)).padStart(2, '0');
const isoString = `${year}-${month}-${day}T${hours}:${minutes}:00${tzSign}${tzHours}:00`;
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "attendee_name": "John Doe",
    "attendee_email": "john@example.com",
    "start_time": "2024-12-20T14:00:00-05:00",
    "end_time": "2024-12-20T14:30:00-05:00"
  }'
```

## Important Notes

1. **Duration**: The time difference between `start_time` and `end_time` must be exactly **30 minutes**.

2. **Timezone Handling**: 
   - The API stores times in UTC in the database
   - Responses return times in the configured timezone (default: `America/Toronto`)
   - Always specify timezone to avoid confusion

3. **Business Rules**:
   - Must be at least 24 hours in the future
   - Must be on a weekday (Monday-Friday)
   - Must be during working hours (9:00 AM - 6:00 PM in local time)

4. **Default Timezone**: If `TIMEZONE` is not set in your `.env` file, it defaults to `America/Toronto`.

## Quick Reference

| Format | Example | Notes |
|--------|---------|-------|
| With timezone offset | `2024-12-20T14:00:00-05:00` | Recommended |
| UTC with Z | `2024-12-20T19:00:00Z` | UTC time |
| UTC with +00:00 | `2024-12-20T19:00:00+00:00` | UTC time |
| No timezone | `2024-12-20T14:00:00` | Uses default timezone |

## Testing

You can test the format by making a request to the API. If the format is invalid, you'll get a 400 error with a message like:

```json
{
  "detail": "Invalid datetime format. Expected ISO 8601 format, got: 2024-12-20 14:00:00"
}
```

