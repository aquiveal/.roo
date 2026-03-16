@Domain
Python applications involving date, time, timestamp manipulation, serialization, scheduling, event-tracking, and time zone management. These rules are triggered whenever the AI writes, modifies, or reviews code dealing with the `datetime` module or time-based data.

@Vocabulary
- **Unaware datetime (Naive timestamp)**: A `datetime` object missing a `tzinfo` attribute. It provides no useful information for absolute time comparison and is considered irrelevant.
- **Aware datetime**: A `datetime` object that embeds time zone information (`tzinfo`).
- **UTC**: Coordinated Universal Time. The standard reference time zone.
- **dateutil**: An external Python library (`python-dateutil`) that provides robust time zone information mapping to OS or embedded IANA databases.
- **iso8601**: An external Python module used strictly for parsing ISO 8601-formatted datetime strings.
- **Ambiguous time**: A wall-clock time that occurs twice in a single day due to daylight saving time (DST) transitions (e.g., falling back).
- **Fold attribute**: An integer attribute (`0` or `1`) introduced in Python 3.6 (PEP 495) used to disambiguate an ambiguous time. `0` represents the time before the DST transition, and `1` represents the time after the transition.

@Objectives
- Guarantee that absolutely zero time zone-unaware (naive) `datetime` objects are generated, processed, or stored.
- Prevent temporal arithmetic errors by strictly forbidding manual time zone calculations (adding/subtracting hours).
- Standardize all cross-boundary time data serialization to the ISO 8601 format.
- Ensure recurring local events are stored accurately without destructive UTC conversion.
- Safely resolve daylight saving time anomalies using explicit disambiguation techniques.

@Guidelines
- **Strictly prohibit unaware datetimes**: The AI MUST NEVER create or process a `datetime` object without a time zone attached. If no time zone is provided by an input, the AI MUST explicitly raise an error or apply a documented default (typically UTC).
- **Forbid default `utcnow()` and `now()` usage**: The AI MUST NOT use `datetime.datetime.utcnow()` or `datetime.datetime.now()` without arguments, as both return naive/unaware objects.
- **Do not manually calculate time zones**: The AI MUST NOT add or subtract hours to convert between time zones due to unpredictable rules like 15-minute granularities and DST shifts.
- **Mandate `dateutil` for time zones**: The AI MUST use the `dateutil.tz` module to acquire `tzinfo` objects. The AI MUST NOT create custom classes inheriting from `datetime.tzinfo`.
- **Do not convert recurring local events to UTC**: If a timestamp represents a recurring event in a local time zone (e.g., "every Wednesday at 10:00 AM CET"), the AI MUST NOT convert it to UTC prior to storage, as summer/winter time shifts will corrupt the schedule.
- **Mandate ISO 8601 for serialization**: The AI MUST serialize all `datetime` objects for non-Python native points (e.g., HTTP REST APIs) using the `.isoformat()` method.
- **Mandate `iso8601` for parsing**: The AI MUST parse ISO 8601 strings back into `datetime` objects using the `iso8601.parse_date()` function, which gracefully defaults to UTC if timezone data is missing.
- **Handle Ambiguous Times explicitly**: When working with times that may fall into a daylight saving time overlap, the AI MUST disambiguate them using `dateutil.tz.is_ambiguous()` and the `fold` attribute (`fold=0` or `fold=1`). Alternatively, strictly stick to UTC to bypass ambiguity.

@Workflow
1. **Dependency Injection**: Ensure `python-dateutil` and `iso8601` are available in the project environment.
2. **Object Creation**: 
   - To get the current UTC time, use `datetime.datetime.now(tz=dateutil.tz.tzutc())`.
   - To get the current local time, use `datetime.datetime.now(tz=dateutil.tz.gettz())`.
   - To apply a specific timezone, use `dateutil.tz.gettz("Region/City")`.
3. **Applying Time Zones to Existing Objects**: If given a naive `datetime` object from an external source, immediately convert it to an aware object using `.replace(tzinfo=...)`.
4. **Serialization (Output)**: When returning the `datetime` object to an API or database, call `.isoformat()` on the aware object.
5. **Deserialization (Input)**: When receiving a timestamp string, pass it immediately to `iso8601.parse_date()`.
6. **Disambiguation Check**: If calculating local times around a DST transition, verify ambiguity using `is_ambiguous()`. If true, set the `fold` attribute using `.replace(fold=0)` or `.replace(fold=1)` before casting to another timezone via `.astimezone()`.

@Examples (Do's and Don'ts)

**Principle: Current Time Instantiation**
- [DO]:
```python
import datetime
from dateutil import tz

def get_current_utc():
    return datetime.datetime.now(tz=tz.tzutc())

def get_current_local():
    return datetime.datetime.now(tz=tz.gettz())
```
- [DON'T]:
```python
import datetime

# Anti-pattern: Returns a naive datetime object
def get_current_utc():
    return datetime.datetime.utcnow()

# Anti-pattern: Returns a naive datetime object
def get_current_local():
    return datetime.datetime.now()
```

**Principle: Assigning Specific Time Zones**
- [DO]:
```python
import datetime
from dateutil import tz

now = datetime.datetime.now(tz=tz.tzutc())
paris_tz = tz.gettz("Europe/Paris")
paris_time = now.astimezone(paris_tz)
```
- [DON'T]:
```python
import datetime

# Anti-pattern: Building a custom tzinfo class
class CustomTZ(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=1)
    def dst(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "Custom"

now = datetime.datetime.now(tz=CustomTZ())
```

**Principle: Serialization and Deserialization**
- [DO]:
```python
import datetime
import iso8601
from dateutil import tz

def serialize_time(dt_obj):
    return dt_obj.isoformat()

def deserialize_time(dt_string):
    return iso8601.parse_date(dt_string)
```
- [DON'T]:
```python
import datetime

# Anti-pattern: Custom string formatting dropping timezone data
def serialize_time(dt_obj):
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")

# Anti-pattern: Manual parsing without timezone awareness
def deserialize_time(dt_string):
    return datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
```

**Principle: Resolving Ambiguous Times (DST Transitions)**
- [DO]:
```python
import datetime
from dateutil import tz

localtz = tz.gettz("Europe/Paris")
utc = tz.tzutc()

confusing_time = datetime.datetime(2017, 10, 29, 2, 30, tzinfo=localtz)

if localtz.is_ambiguous(confusing_time):
    # fold=0 means before the DST change (summer time)
    first_occurrence = confusing_time.replace(fold=0).astimezone(utc)
    # fold=1 means after the DST change (winter time)
    second_occurrence = confusing_time.replace(fold=1).astimezone(utc)
```
- [DON'T]:
```python
import datetime
from dateutil import tz

localtz = tz.gettz("Europe/Paris")
utc = tz.tzutc()

# Anti-pattern: Ignoring the fold during an ambiguous wall-clock time
confusing_time = datetime.datetime(2017, 10, 29, 2, 30, tzinfo=localtz)
converted = confusing_time.astimezone(utc) # Fails to accurately pinpoint the time
```