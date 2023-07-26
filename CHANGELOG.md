## neptune-sacred 1.0.1

### Fixes
- Fixed file upload if full path is used and file is not in CWD ([#25](https://github.com/neptune-ai/neptune-sacred/pull/25))

## neptune-sacred 1.0.0

### Changes
- Updated integration to be compatible with `neptune` `1.0.0`. ([#20](https://github.com/neptune-ai/neptune-sacred/pull/20))
- Removed `neptune` and `neptune-client` from base requirements  ([#20](https://github.com/neptune-ai/neptune-sacred/pull/20))
- Only files are now uploaded instead of a catch-all `object` ([#20](https://github.com/neptune-ai/neptune-sacred/pull/20))

## neptune-sacred 0.10.1

### Changes
- Moved `neptune_sacred` package to `src` directory ([#14](https://github.com/neptune-ai/neptune-sacred/pull/14))
- Moved to Poetry with package building ([#19](https://github.com/neptune-ai/neptune-sacred/pull/19))

### Fixes
- Fixed NeptuneObserver import error - now possible to directly import with `from neptune_sacred import NeptuneObserver`
  ([#16](https://github.com/neptune-ai/neptune-sacred/pull/16))


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
