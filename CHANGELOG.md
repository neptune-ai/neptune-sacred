## [UNRELEASED] neptune-sacred 0.10.1

### Changes
- Moved `neptune_sacred` package to `src` directory ([#14](https://github.com/neptune-ai/neptune-sacred/pull/14))

## neptune-sacred 0.10.0

### Changes
- Changed integrations utils to be imported from non-internal package ([#12](https://github.com/neptune-ai/neptune-sacred/pull/12))

## neptune-sacred 0.9.7

### Fixes
- Corrected filename parsing for artifacts when running on Windows ([#9](https://github.com/neptune-ai/neptune-sacred/pull/9))
- Added the ability to log artifacts under a different name than the original filename ([#10](https://github.com/neptune-ai/neptune-sacred/pull/10))
- Convert result lists/dictionaries to JSON strings so that they can be logged as metrics ([#11](https://github.com/neptune-ai/neptune-sacred/pull/11))

## neptune-sacred 0.9.6

### Features
- Mechanism to prevent using legacy Experiments in new-API integrations ([#4](https://github.com/neptune-ai/neptune-sacred/pull/4))
